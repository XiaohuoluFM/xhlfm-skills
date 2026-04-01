from __future__ import annotations

import argparse

from tests.helpers import REPO_ROOT, load_json_fixture, load_module

fetch_xyz_rank = load_module(
    REPO_ROOT / "skills" / "podcast-radar-cn" / "scripts" / "fetch_xyz_rank.py",
    "podcast_radar_cn_fetch_xyz_rank",
)


def make_args(**overrides: object) -> argparse.Namespace:
    base = {
        "genre": [],
        "freshness_days_max": None,
        "min_play_count": None,
        "min_comment_count": None,
        "min_subscription": None,
        "query": None,
    }
    base.update(overrides)
    return argparse.Namespace(**base)


def test_make_title_signals_extracts_marker_guest_format_and_topics() -> None:
    signals = fetch_xyz_rank.make_title_signals("S8E9 鲁豫对话李睿｜AI 商业复盘")
    assert signals["episodeMarkers"][0]["season"] == 8
    assert signals["episodeMarkers"][0]["episode"] == 9
    assert any("李睿" in hint for hint in signals["guestHints"])
    assert "对话" in signals["formatHints"]
    assert "AI" in signals["topicKeywords"]
    assert "商业" in signals["topicKeywords"]


def test_normalize_episode_maps_expected_fields() -> None:
    raw = load_json_fixture("podcast_radar_cn", "xyzrank_episode_item.json")
    item = fetch_xyz_rank.normalize_episode(raw, "hot-episodes")
    assert item["kind"] == "episode"
    assert item["podcastExternalId"] == raw["podcastID"]
    assert item["episodeUrl"] == raw["link"]
    assert item["genre"] == "艺术"
    assert item["titleSignals"]["episodeMarkers"][0]["season"] == 8


def test_normalize_podcast_collects_links() -> None:
    raw = load_json_fixture("podcast_radar_cn", "xyzrank_podcast_item.json")
    item = fetch_xyz_rank.normalize_podcast(raw, "hot-podcasts")
    assert item["kind"] == "podcast"
    assert item["xyzUrl"] == "https://www.xiaoyuzhoufm.com/podcast/625635587bfca4e73e990703"
    assert item["appleUrl"].startswith("https://podcasts.apple.com/")
    assert item["rssUrl"] == "https://feed.xyzfm.space/hwen8wf69c6g"


def test_min_subscription_filter_is_ignored_for_podcasts_without_subscription() -> None:
    item = {
        "kind": "podcast",
        "genre": "投资",
        "title": "节目 A",
        "podcastName": "节目 A",
        "authors": "作者",
        "subscriptionCount": None,
        "avgPlayCount": 1000,
        "avgCommentCount": 100,
        "titleSignals": {"guestHints": [], "topicKeywords": [], "formatHints": []},
    }
    assert fetch_xyz_rank.matches_filters(item, make_args(min_subscription=9999))


def test_query_filter_can_match_title_signals() -> None:
    item = {
        "kind": "episode",
        "genre": "科技",
        "title": "普通标题",
        "podcastName": "节目 B",
        "authors": "",
        "subscriptionCount": 10,
        "playCount": 100,
        "commentCount": 20,
        "titleSignals": {
            "guestHints": [],
            "topicKeywords": ["AI"],
            "formatHints": ["复盘"],
        },
    }
    assert fetch_xyz_rank.matches_filters(item, make_args(query="AI"))
    assert fetch_xyz_rank.matches_filters(item, make_args(query="复盘"))
