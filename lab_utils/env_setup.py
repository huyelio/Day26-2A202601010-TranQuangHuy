"""Load cấu hình OpenAI từ project root cho mọi agent trong lab."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"


def load_lab_env() -> None:
    """Nạp OPENAI_API_KEY và biến lab từ .env (idempotent)."""
    load_dotenv(ENV_FILE)
    os.environ.setdefault("OPENAI_MODEL", "openai/gpt-5.4-nano")


def require_api_key() -> None:
    """Raise sớm nếu thiếu API key (tránh lỗi khó hiểu lúc gọi OpenAI)."""
    load_lab_env()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            f"Thiếu OPENAI_API_KEY. Đặt key OpenAI API trong {ENV_FILE}."
        )


def get_lab_model() -> LiteLlm:
    """Tạo model connector dùng chung cho orchestrator và specialist."""
    load_lab_env()
    return LiteLlm(model=os.environ["OPENAI_MODEL"])
