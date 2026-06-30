from __future__ import annotations

BLOCKED_WORDS = {
    "hack",
    "bypass",
    "exploit",
    "malware",
    "breach",
    "attack",
    "unauthorized",
}


def input_shield(text: str) -> str:
    """Raise an error if the text contains blocked input terms."""
    if not text:
        return text

    normalized = text.lower()
    matches = [word for word in BLOCKED_WORDS if word in normalized]
    if matches:
        raise ValueError(
            f"Blocked input detected: {', '.join(sorted(matches))}."
        )
    return text


def truncate_text(text: str, max_chars: int = 2500) -> str:
    """Truncate the text to a safe maximum character length."""
    if max_chars < 0:
        raise ValueError("max_chars must be non-negative.")
    return text if len(text) <= max_chars else text[:max_chars]
