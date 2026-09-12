# Task Notebook Download Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Download the current Task0/Task1 learning material into stable task folders and provide a repeatable manifest-driven downloader for future tasks.

**Architecture:** A JSON manifest is the single source of truth for upstream URLs and local paths. A standard-library Python script reads that manifest, downloads files atomically, and validates notebooks as non-empty JSON documents. A small unittest suite covers manifest shape and validation without requiring network access.

**Tech Stack:** Python 3.10+, `urllib.request`, `json`, `unittest`, Jupyter notebooks.

---

### Task 1: Add the download manifest and validation tests

**Files:**
- Create: `downloads/task_manifest.json`
- Create: `tests/test_download_tasks.py`

- [ ] **Step 1: Write failing tests for manifest and notebook validation**

  Test that every manifest entry has `task`, `kind`, `url`, and `path`, that local paths stay under `task0/` or `task1/`, and that the validator accepts a notebook with a `cells` list while rejecting malformed JSON and empty/non-notebook JSON.

- [ ] **Step 2: Run the tests to verify they fail**

  Run: `python -m unittest tests/test_download_tasks.py -v`
  Expected: FAIL because the manifest and downloader module do not exist yet.

- [ ] **Step 3: Add all current Task0/Task1 source mappings**

  Include the three Task0 notebooks, Task0's linked reference markdown, the four Task1 core notebooks, four Task1 extension notebooks, and Task1's linked reference markdown. Preserve upstream filenames and map them into `task0/notebooks`, `task0/references`, `task1/notebooks`, and `task1/references`.

### Task 2: Implement the reusable downloader

**Files:**
- Create: `scripts/download_tasks.py`
- Modify: `tests/test_download_tasks.py`

- [ ] **Step 1: Implement manifest loading and validation helpers**

  Expose `load_manifest(path)`, `validate_notebook_bytes(data, path)`, and `validate_local_file(path, kind)`. Use only the standard library so the downloader works before the Conda environment is created.

- [ ] **Step 2: Implement atomic downloads and command-line modes**

  Add a default download mode plus `--check` (validate all local files without network) and `--manifest PATH`. Create parent directories, write to a sibling temporary file, replace the destination only after a successful response, and fail with a useful file-specific error.

- [ ] **Step 3: Run the unit tests to verify the implementation**

  Run: `python -m unittest tests/test_download_tasks.py -v`
  Expected: all tests PASS without requiring internet access.

### Task 3: Download and document usage

**Files:**
- Create: `task0/notebooks/*.ipynb`
- Create: `task0/references/02_training_memory_pressure.md`
- Create: `task1/notebooks/*.ipynb`
- Create: `task1/references/01_vram_ledger_and_metrics.md`
- Modify: `README.md`

- [ ] **Step 1: Run the manifest-driven downloader**

  Run: `python scripts/download_tasks.py`
  Expected: every manifest entry reports a downloaded file and exits with status 0.

- [ ] **Step 2: Run offline structural validation**

  Run: `python scripts/download_tasks.py --check`
  Expected: all manifest entries pass; each notebook parses as JSON and contains at least one cell.

- [ ] **Step 3: Add concise future-task instructions to README.md**

  Document the folder layout, the normal download command, the offline check command, and that future task releases only require adding entries to `downloads/task_manifest.json` before rerunning the script.

- [ ] **Step 4: Review the resulting file set and git diff**

  Run: `git status --short` and `git diff --stat`.
  Expected: only the manifest, downloader/tests/docs, and downloaded Task0/Task1 materials are present.
