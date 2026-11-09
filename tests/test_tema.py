"""Regressão: manter tema consistente em execuções locais e Docker."""
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def test_tema_claro_definido_no_streamlit():
    config = tomllib.loads((ROOT / ".streamlit" / "config.toml").read_text(encoding="utf-8"))
    tema = config["theme"]
    assert tema["base"] == "light"
    assert tema["backgroundColor"] == "#ffffff"
    assert tema["secondaryBackgroundColor"] == "#f8fafc"
    assert tema["textColor"] == "#0f172a"


def test_docker_inclui_o_mesmo_tema():
    dockerfile = (ROOT / "frontend" / "Dockerfile").read_text(encoding="utf-8")
    assert "COPY .streamlit /code/.streamlit" in dockerfile
