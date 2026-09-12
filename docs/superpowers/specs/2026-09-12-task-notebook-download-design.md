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

Task0 contains only the two notebooks that require local assignment work
(`17` and `18`); its `07` notebook and training-memory material are read from
upstream links in `task0/README.md`. Task1 contains the four core notebooks that
require local calculation; its extension notebooks and VRAM-ledger material are
read from upstream links in `task1/README.md`. Upstream filenames are preserved
for every local notebook.

## Download and validation

Use a small checked-in manifest/script rather than manually copying files. The
manifest lists only local calculation notebooks; README files hold original
links for reading-only materials. The downloader creates parent directories,
writes files as UTF-8, and skips existing local files by default so completed
answers are safe. An explicit `--force` is required to refresh a local file.
After downloading, validate that all manifest entries exist, notebooks parse as
JSON, and each notebook has at least one cell.

The manifest records the upstream URL and local path for every file. No
notebook content is rewritten or normalized, preserving the material users are
expected to study and modify.
