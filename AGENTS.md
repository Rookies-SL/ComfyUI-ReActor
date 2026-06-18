# Repository Guidelines

## Project Structure & Module Organization

This repository is a ComfyUI custom node package for ReActor face swapping. `__init__.py` exposes ComfyUI node mappings from `nodes.py`, which is the main node entry point and UI contract. Core face analysis and swap logic lives in `reactor_core/` and `scripts/`. Compatibility shims for ComfyUI/SD-style processing are in `r_modules/`. Bundled helper libraries are vendored under `r_basicsr/`, `r_facelib/`, and `r_chainner/`; avoid broad refactors there unless updating that subsystem. Metadata and registry publishing settings are in `pyproject.toml`, while user-facing install and model guidance belongs in `README.md` and `README_RU.md`.

## Build, Test, and Development Commands

- `python -m pip install -r requirements.txt`: install Python dependencies in the same environment used by ComfyUI.
- `python install.py`: run the extension installer on Linux/macOS; Windows users can run `install.bat`.
- `python -m compileall __init__.py nodes.py reactor_core scripts r_modules`: syntax-check edited Python files without launching ComfyUI.
- Start ComfyUI from the parent ComfyUI checkout and confirm ReActor nodes appear under the `ReActor` category.

## Coding Style & Naming Conventions

Use Python with 4-space indentation and keep imports grouped as standard library, third-party, then local modules. Follow existing ComfyUI node conventions: class attributes such as `INPUT_TYPES`, `RETURN_TYPES`, `FUNCTION`, and `CATEGORY` are part of the public node API. Preserve node class/display names and mapping keys unless the change is intentionally breaking. Prefer descriptive snake_case for functions and variables; keep model path constants uppercase.

## Testing Guidelines

There is no dedicated pytest suite in this repository. For small changes, run `compileall` and import or launch the node inside a ComfyUI environment. For behavior changes, validate a minimal workflow covering the edited node, face model loading, and any affected model directory such as `ComfyUI/models/reactor`, `facerestore_models`, `ultralytics`, or `sams`. Do not commit generated models, downloaded weights, or local workflow outputs.

## Commit & Pull Request Guidelines

Recent history uses short imperative prefixes such as `ADD:`, `FIX:`, `UPD:`, `DEL:`, plus `VersionUP`. Keep commits focused, for example `FIX: Face restore model selection`. Pull requests should describe the user-visible change, list validation performed, link related issues, and include screenshots or workflow notes when UI nodes or image output change.

## Security & Configuration Tips

Respect the project’s SFW-friendly scope and do not weaken NSFW detection or safety checks. Keep external model downloads documented rather than checked in. When changing dependencies, update both `requirements.txt` and `pyproject.toml` if runtime requirements change.
