from __future__ import annotations

import argparse

import pytest

from tests.helpers import REPO_ROOT, load_text_fixture, load_module

enrich_xiaoyuzhou = load_module(
    REPO_ROOT / "skills" / "podcast-radar-cn" / "scripts" / "enrich_xiaoyuzhou.py",
    "podcast_radar_cn_enrich_xiaoyuzhou",
)


def test_extract_next_data_from_html_bytes_parses_episode_fixture() -> None:
    html = load_text_fixture("podcast_radar_cn", "xiaoyuzhou_episode_page.html").encode("utf-8")
    payload = enrich_xiaoyuzhou.extract_next_data_from_html_bytes(html)
    assert payload is not None
    episode = payload["props"]["pageProps"]["episode"]
    assert episode["pid"] == "625635587bfca4e73e990703"
    assert episode["title"].startswith("S8E9")


def test_html_to_text_preserves_basic_line_breaks() -> None:
    text = enrich_xiaoyuzhou.html_to_text("<p>第一段</p><ul><li>要点一</li><li>要点二</li></ul>")
    assert text == "第一段\n要点一\n要点二"


def test_enrich_episode_maps_podcast_url_and_shownotes() -> None:
    html = load_text_fixture("podcast_radar_cn", "xiaoyuzhou_episode_page.html").encode("utf-8")
    payload = enrich_xiaoyuzhou.extract_next_data_from_html_bytes(html)
    item = enrich_xiaoyuzhou.enrich_episode(
        "https://www.xiaoyuzhoufm.com/episode/69bf524c2d318777c9169361",
        payload["props"]["pageProps"]["episode"],
    )
    assert item["podcastUrl"] == "https://www.xiaoyuzhoufm.com/podcast/625635587bfca4e73e990703"
    assert "要点一" in item["shownotesText"]
    assert item["podcast"]["subscriptionCount"] == 3457124


def test_enrich_podcast_maps_recent_episodes() -> None:
    html = load_text_fixture("podcast_radar_cn", "xiaoyuzhou_podcast_page.html").encode("utf-8")
    payload = enrich_xiaoyuzhou.extract_next_data_from_html_bytes(html)
    item = enrich_xiaoyuzhou.enrich_podcast(
        "https://www.xiaoyuzhoufm.com/podcast/625635587bfca4e73e990703",
        payload["props"]["pageProps"]["podcast"],
    )
    assert item["pid"] == "625635587bfca4e73e990703"
    assert item["podcasters"][0]["nickname"] == "GIADA迦达"
    assert item["recentEpisodes"][0]["eid"] == "69bf524c2d318777c9169361"


def test_main_refuses_when_requested_urls_exceed_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    args = argparse.Namespace(
        episode_url=["https://example.com/e1", "https://example.com/e2"],
        podcast_url=[],
        from_json=None,
        max_items=1,
        sleep_seconds=0.0,
        jitter_seconds=0.0,
        pretty=False,
    )
    monkeypatch.setattr(enrich_xiaoyuzhou, "parse_args", lambda: args)
    with pytest.raises(SystemExit, match="Refusing to enrich 2 URLs"):
        enrich_xiaoyuzhou.main()
