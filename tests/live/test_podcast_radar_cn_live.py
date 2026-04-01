from __future__ import annotations

import json
import subprocess
import sys

import pytest

from tests.helpers import REPO_ROOT

FETCH_SCRIPT = REPO_ROOT / "skills" / "podcast-radar-cn" / "scripts" / "fetch_xyz_rank.py"
ENRICH_SCRIPT = REPO_ROOT / "skills" / "podcast-radar-cn" / "scripts" / "enrich_xiaoyuzhou.py"


@pytest.mark.live
def test_fetch_xyz_rank_live_smoke() -> None:
    result = subprocess.run(
        [sys.executable, str(FETCH_SCRIPT), "--list", "hot-podcasts", "--limit", "1"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert payload["returnedCount"] == 1
    assert payload["items"][0]["kind"] == "podcast"


@pytest.mark.live
def test_enrich_xiaoyuzhou_live_smoke() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ENRICH_SCRIPT),
            "--podcast-url",
            "https://www.xiaoyuzhoufm.com/podcast/625635587bfca4e73e990703",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert payload["returnedCount"] == 1
    assert payload["items"][0]["kind"] == "podcast"
    assert payload["items"][0]["pid"] == "625635587bfca4e73e990703"
