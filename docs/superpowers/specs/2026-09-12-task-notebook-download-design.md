# Task Notebook Download Design

## Goal

Download the notebooks required by Task0 and Task1 from the upstream
`datawhalechina/llm-algo-leetcode` repository into this repository so they can
be opened, completed, and committed here. Conda environment setup is explicitly
out of scope for this step.

## Layout

```text
task0/
  notebooks/
  references/
task1/
  notebooks/
  references/
```

Task0 contains the three linked notebooks and its linked training-memory
reference. Task1 contains the four required notebooks, the four optional
extension notebooks, and its linked VRAM-ledger reference. Upstream filenames
are preserved so links and notebook metadata remain recognizable.

## Download and validation

Use a small checked-in manifest/script rather than manually copying files. The
source is pinned to the upstream `main` branch URLs listed in the Task0/Task1
issues. The downloader creates parent directories, writes files as UTF-8, and
is idempotent so it can refresh files later. After downloading, validate that
all manifest entries exist, notebooks parse as JSON with `nbformat`, and each
notebook has at least one cell.

The manifest records the upstream URL and local path for every file. No
notebook content is rewritten or normalized, preserving the material users are
expected to study and modify.
