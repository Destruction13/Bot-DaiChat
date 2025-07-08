import re

MDV2_SPECIAL_CHARS = r"_ * [ ] ( ) ~ ` > # + - = | { } . !"
MDV2_SPECIAL_CHARS = MDV2_SPECIAL_CHARS.replace(" ", "")
_escape_re = re.compile(f"([{re.escape(MDV2_SPECIAL_CHARS)}])")

def escape_md(text: str) -> str:
    """Escape text for Telegram MarkdownV2."""
    return _escape_re.sub(r"\\\1", text)

