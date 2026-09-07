import json
from pathlib import Path


def test_vercel_function_includes_the_application_package() -> None:
    """The FastAPI wrapper is useless if Vercel omits ``oslo_api``."""

    api_root = Path(__file__).resolve().parents[1]
    config = json.loads((api_root / "vercel.json").read_text(encoding="utf-8"))

    assert config["functions"]["src/main.py"]["includeFiles"] == "src/oslo_api/**"
