---
name: harbor-transfer
description: Move data between on-premise servers and cloud storage using the internal harbor library. Use when uploading query results or files to the cloud, downloading cloud data to on-premise, or scheduling a transfer step inside a Python pipeline.
argument-hint: "<what to move> <from> <to>"
---

# /harbor-transfer - On-premise ↔ Cloud Transfers

All data movement between on-premise and cloud goes through `harbor`. Never write ad-hoc copy scripts, never call cloud SDKs directly for this.

API cheat sheet: `references/harbor-api.md`. Read it before writing transfer code.

## Workflow

1. **Identify** source, destination, format and size of the data.
2. **Configure** source/destination identifiers as constants in the project's constants module, never inline.
3. **Implement** the transfer as a method of a pipeline class (e.g. `Loader.upload()`), following `module_template.py`.
4. **Validate** after the transfer: row count / file size at destination matches the source.
5. **Log** what moved, where and how much with `logging`.

<!-- TODO(content): add the canonical harbor snippet, supported formats, size limits, naming conventions for cloud paths, and data classification rules (what may / may not leave on-premise). -->
