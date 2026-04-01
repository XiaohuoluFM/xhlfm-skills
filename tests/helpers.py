from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
FIXTURES_ROOT = REPO_ROOT / "tests" / "fixtures"


def list_skill_dirs() -> list[Path]:
    return sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir() and not path.name.startswith("."))


def load_module(module_path: Path, module_name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json_fixture(*parts: str) -> dict:
    return json.loads((FIXTURES_ROOT.joinpath(*parts)).read_text(encoding="utf-8"))


def load_text_fixture(*parts: str) -> str:
    return FIXTURES_ROOT.joinpath(*parts).read_text(encoding="utf-8")
