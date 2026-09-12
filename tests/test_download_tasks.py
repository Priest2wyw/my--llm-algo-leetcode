import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.download_tasks import (
    download_entry,
    load_manifest,
    validate_local_file,
    validate_notebook_bytes,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "downloads" / "task_manifest.json"


class DownloadTasksTest(unittest.TestCase):
    def test_manifest_entries_are_complete_and_scoped(self):
        entries = load_manifest(MANIFEST)

        self.assertEqual(len(entries), 6)
        for entry in entries:
            self.assertEqual(
                {"task", "kind", "url", "path"},
                set(entry),
            )
            self.assertIn(entry["task"], {"task0", "task1"})
            self.assertIn(entry["kind"], {"notebook", "reference"})
            self.assertTrue(entry["url"].startswith("https://raw.githubusercontent.com/"))
            self.assertTrue(Path(entry["path"]).parts[0] in {"task0", "task1"})

        paths = {entry["path"] for entry in entries}
        self.assertNotIn("task0/notebooks/07_PyTorch_Autograd_and_Backward.ipynb", paths)
        self.assertNotIn("task1/notebooks/04_Attention_MHA_GQA.ipynb", paths)
        self.assertNotIn("task1/notebooks/12_TensorCore_and_Mixed_Precision.ipynb", paths)
        self.assertNotIn("task1/notebooks/14_FlashAttention_Memory_Model.ipynb", paths)

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

    def test_download_entry_does_not_overwrite_existing_homework(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "task0" / "notebooks" / "homework.ipynb"
            destination.parent.mkdir(parents=True)
            original = json.dumps({"cells": [{"cell_type": "code", "outputs": ["answer"]}]}).encode()
            destination.write_bytes(original)
            entry = {
                "task": "task0",
                "kind": "notebook",
                "url": "https://example.com/homework.ipynb",
                "path": "task0/notebooks/homework.ipynb",
            }

            with mock.patch("scripts.download_tasks.REPOSITORY_ROOT", root):
                with mock.patch("scripts.download_tasks.urlopen", side_effect=AssertionError("network called")):
                    result = download_entry(entry)

            self.assertEqual(result, destination)
            self.assertEqual(destination.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
