"""Edition-aware production briefs and human review plans. No Resolve mutation."""
from __future__ import annotations

DEFAULT_EDITION = "biblical-period"

def production_brief(args):
    edition = args.get("edition", DEFAULT_EDITION)
    mode = args.get("story_mode", "original")
    if edition not in ("kids-3d", "biblical-period"):
        return {"ok": False, "error": "edition must be kids-3d or biblical-period"}
    if mode not in ("original", "scripture"):
        return {"ok": False, "error": "story_mode must be original or scripture"}
    if edition == "kids-3d":
        direction = "Original stylized 3D animation for ages 5–8; consistent model sheets, readable poses, gentle conflict and a reassuring resolution."
        review = ["Adult editor approves story and emotional intensity for ages 5–8.",
                  "Compare model, proportions, materials, wardrobe and face against approved turnarounds.",
                  "Hold reactions and important actions long enough for comprehension.",
                  "Review flashes, sudden volume peaks, music masking and clear dialogue."]
        edit = {"pacing": "story and comprehension led; preserve reaction and learning beats", "dialogue": "preserve meaningful pauses; audition tighten_dialogue dry-run before applying", "color": "match approved 3D look-development reference, protect palette and materials"}
    else:
        direction = "Realistic historical drama in a specific biblical-era region and period; natural skin, believable weight, practical materials and motivated daylight/firelight."
        review = ["Research and record the exact period and community; flag disputed reconstructions.",
                  "Check wardrobe, tools, buildings, writing, food and sounds for anachronisms.",
                  "Review casting, pronunciation, interpretation and intensity with human editors."]
        if mode == "scripture":
            review.append("Verify passage and translation; distinguish quotation, paraphrase, historical inference and invention.")
        else:
            review.append("Label the story as original historical fiction; never present invented words or events as Scripture.")
        edit = {"pacing": "preserve spatial geography, restrained performances and meaningful silences", "dialogue": "preserve pronunciation and breath; audition tighten_dialogue dry-run", "color": "match the approved naturalistic reference; preserve skin and material detail"}
    missing = []
    if edition == "biblical-period":
        missing = [key for key in ("era", "region") if not str(args.get(key, "")).strip()]
        if mode == "scripture":
            missing += [key for key in ("passage", "translation") if not str(args.get(key, "")).strip()]
    return {"ok": True, "edition": edition, "story_mode": mode, "direction": direction,
            "context": {k: args.get(k, "") for k in ("era", "region", "passage", "translation")},
            "missing_brief_fields": missing, "ready_for_review": not missing,
            "edit_plan": edit, "manual_review": [{"criterion": item, "status": "pending"} for item in review],
            "review_note": "These are editorial criteria, not automated safety, historical or theological verdicts. Loudness targets must follow the chosen delivery specification."}

def register(add_tool):
    add_tool(name="production_brief", schema={"type": "object", "properties": {
        "edition": {"type": "string", "enum": ["kids-3d", "biblical-period"]},
        "story_mode": {"type": "string", "enum": ["original", "scripture"]},
        "era": {"type": "string"}, "region": {"type": "string"},
        "passage": {"type": "string"}, "translation": {"type": "string"}
    }, "additionalProperties": False}, handler=production_brief, tier="both",
    description="Get an edition-specific production brief, finishing plan and pending manual-review criteria for children's 3D animation (ages 5–8) or realistic biblical cinema. Supports original period fiction and Scripture adaptations. Read-only, works without Resolve; does not certify finished footage.")
