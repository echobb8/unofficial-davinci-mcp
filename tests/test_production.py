from davinci_mcp.tools_production import production_brief
from davinci_mcp.registry import build_registry

def test_original_story_does_not_require_scripture_source():
    brief = production_brief({"edition": "biblical-period", "story_mode": "original", "era": "Roman period", "region": "Galilee"})
    assert brief["ready_for_review"]
    assert "passage" not in brief["missing_brief_fields"]
    assert all(item["status"] == "pending" for item in brief["manual_review"])

def test_scripture_adaptation_requires_passage_and_translation():
    brief = production_brief({"edition": "biblical-period", "story_mode": "scripture", "era": "Iron Age", "region": "Judah"})
    assert brief["missing_brief_fields"] == ["passage", "translation"]
    assert not brief["ready_for_review"]

def test_production_tool_is_exposed_to_agents_without_resolve():
    registry = build_registry()
    tool = registry.get("production_brief")
    assert tool is not None and tool.tier == "both"
    assert tool.handler({"edition": "kids-3d"})["ok"]

def test_invalid_mode_does_not_fall_through_to_original():
    assert not production_brief({"story_mode": "wrong"})["ok"]
