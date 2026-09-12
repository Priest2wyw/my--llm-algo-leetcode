import json
import tempfile
import unittest
from pathlib import Path

from scripts.download_tasks import (
    load_manifest,
    validate_local_file,
    validate_notebook_bytes,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "downloads" / "task_manifest.json"


class DownloadTasksTest(unittest.TestCase):
    def test_manifest_entries_are_complete_and_scoped(self):
        entries = load_manifest(MANIFEST)

        self.assertEqual(len(entries), 12)
        for entry in entries:
            self.assertEqual(
                {"task", "kind", "url", "path"},
                set(entry),
            )
            self.assertIn(entry["task"], {"task0", "task1"})
            self.assertIn(entry["kind"], {"notebook", "reference"})
            self.assertTrue(entry["url"].startswith("https://raw.githubusercontent.com/"))
            self.assertTrue(Path(entry["path"]).parts[0] in {"task0", "task1"})

    def test_validate_notebook_bytes_accepts_non_empty_notebook(self):
        data = json.dumps({"cells": [{"cell_type": "markdown"}]}).encode()
        validate_notebook_bytes(data, "example.ipynb")

    def test_validate_notebook_bytes_rejects_invalid_content(self):
        with self.assertRaises(ValueError):
            validate_notebook_bytes(b"not json", "example.ipynb")
        with self.assertRaises(ValueError):
            validate_notebook_bytes(b"{}", "example.ipynb")
        with self.assertRaises(ValueError):
            validate_notebook_bytes(json.dumps({"cells": []}).encode(), "example.ipynb")

    def test_validate_local_file_checks_references_and_notebooks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = root / "example.ipynb"
            notebook.write_text(json.dumps({"cells": [{"cell_type": "code"}]}), encoding="utf-8")
            reference = root / "reference.md"
            reference.write_text("# Reference\n", encoding="utf-8")

            validate_local_file(notebook, "notebook")
            validate_local_file(reference, "reference")

            reference.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError):
                validate_local_file(reference, "reference")


if __name__ == "__main__":
    unittest.main()
