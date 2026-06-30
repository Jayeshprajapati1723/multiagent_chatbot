import json


def validate_layout_json(json_text: str) -> dict:
    """Parse and validate a layout JSON string against the required schema."""
    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc.msg}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("Parsed JSON must be an object at the top level.")

    required_keys = {"detected_sentiment", "theme", "layout_style"}
    theme_required_keys = {
        "background_color",
        "primary_text",
        "accent_color",
        "font_family_heading",
        "font_family_body",
    }

    missing = [key for key in required_keys if key not in parsed]
    extra = [key for key in parsed if key not in required_keys]

    if missing or extra:
        problems = []
        if missing:
            problems.append(f"missing top-level keys: {', '.join(sorted(missing))}")
        if extra:
            problems.append(f"unexpected top-level keys: {', '.join(sorted(extra))}")
        raise ValueError("JSON schema validation failed: " + "; ".join(problems))

    theme = parsed["theme"]
    if not isinstance(theme, dict):
        raise ValueError("The 'theme' field must be an object.")

    theme_missing = [key for key in theme_required_keys if key not in theme]
    theme_extra = [key for key in theme if key not in theme_required_keys]
    if theme_missing or theme_extra:
        problems = []
        if theme_missing:
            problems.append(f"missing theme keys: {', '.join(sorted(theme_missing))}")
        if theme_extra:
            problems.append(f"unexpected theme keys: {', '.join(sorted(theme_extra))}")
        raise ValueError("Theme schema validation failed: " + "; ".join(problems))

    return parsed
