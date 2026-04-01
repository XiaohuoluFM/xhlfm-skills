from __future__ import annotations

import os
import re
from pathlib import Path

import yaml

from tests.helpers import list_skill_dirs

FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def read_frontmatter(skill_md: Path) -> dict[str, str]:
    content = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(content)
    assert match, f"{skill_md} is missing YAML frontmatter"
    return yaml.safe_load(match.group(1))


def test_every_skill_has_skill_md() -> None:
    for skill_dir in list_skill_dirs():
        assert (skill_dir / "SKILL.md").exists(), f"{skill_dir} is missing SKILL.md"


def test_skill_frontmatter_name_matches_directory() -> None:
    for skill_dir in list_skill_dirs():
        frontmatter = read_frontmatter(skill_dir / "SKILL.md")
        assert frontmatter.get("name") == skill_dir.name, f"{skill_dir} frontmatter name should match directory name"
        assert frontmatter.get("description"), f"{skill_dir} frontmatter is missing description"


def test_agents_openai_yaml_is_valid_when_present() -> None:
    for skill_dir in list_skill_dirs():
        openai_yaml = skill_dir / "agents" / "openai.yaml"
        if not openai_yaml.exists():
            continue
        payload = yaml.safe_load(openai_yaml.read_text(encoding="utf-8"))
        interface = payload.get("interface", {})
        assert interface.get("display_name"), f"{openai_yaml} is missing interface.display_name"
        assert interface.get("short_description"), f"{openai_yaml} is missing interface.short_description"
        assert interface.get("default_prompt"), f"{openai_yaml} is missing interface.default_prompt"


def test_python_and_shell_scripts_are_executable() -> None:
    for skill_dir in list_skill_dirs():
        scripts_dir = skill_dir / "scripts"
        if not scripts_dir.exists():
            continue
        for script in scripts_dir.rglob("*"):
            if not script.is_file():
                continue
            if script.suffix in {".py", ".sh"}:
                assert os.access(script, os.X_OK), f"{script} should be executable"
