import random
from pathlib import Path

from app.core.config import BACKEND_DIR, settings
from app.data.dashboard_fallbacks import DEFAULT_MEME
from app.schemas.dashboard import MemeItem
from app.schemas.dashboard_context import DashboardContext

MEME_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MEMES_DIR = BACKEND_DIR / "static" / "memes"


def _list_meme_files() -> list[Path]:
    if not MEMES_DIR.is_dir():
        return []
    return sorted(
        path
        for path in MEMES_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in MEME_EXTENSIONS
    )


def _build_title(filename: str) -> str:
    stem = Path(filename).stem
    number = stem.replace("meme", "").strip()
    if number.isdigit():
        return f"Crypto Meme #{number}"
    return "Crypto Meme of the Day"


def get_meme(context: DashboardContext) -> MemeItem:
    meme_files = _list_meme_files()
    if not meme_files:
        return DEFAULT_MEME

    selected = random.choice(meme_files)
    base_url = settings.backend_public_url.rstrip("/")
    tags = ["fun", "crypto"] if "fun" in context.content_types else ["crypto"]

    return MemeItem(
        id=f"meme_{selected.stem}",
        title=_build_title(selected.name),
        image_url=f"{base_url}/static/memes/{selected.name}",
        tags=tags,
    )
