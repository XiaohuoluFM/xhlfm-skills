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


def read_frontmatter_block(skill_md: Path) -> str:
    content = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(content)
    assert match, f"{skill_md} is missing YAML frontmatter"
    return match.group(1)


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


def test_skill_markdown_does_not_assume_repo_root_paths() -> None:
    for skill_dir in list_skill_dirs():
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert (
            f"skills/{skill_dir.name}/" not in content
        ), f"{skill_md} should not hardcode repo-root skill paths; use skill-root paths or {{baseDir}} instead"


def test_openclaw_metadata_is_inline_json_when_present() -> None:
    for skill_dir in list_skill_dirs():
        frontmatter_block = read_frontmatter_block(skill_dir / "SKILL.md")
        metadata_lines = [line for line in frontmatter_block.splitlines() if line.startswith("metadata:")]
        for line in metadata_lines:
            assert "{" in line and "}" in line, (
                f"{skill_dir / 'SKILL.md'} metadata should be inline JSON for OpenClaw compatibility"
            )
