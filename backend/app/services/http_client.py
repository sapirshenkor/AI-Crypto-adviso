from typing import Any

import httpx

from app.core.config import settings


def _build_client() -> httpx.Client:
    return httpx.Client(timeout=settings.external_api_timeout_seconds)


def get_json(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    try:
        with _build_client() as client:
            response = client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict):
                return data
    except (httpx.HTTPError, ValueError):
        return None
    return None


def post_json(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    json_body: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    try:
        with _build_client() as client:
            response = client.post(url, headers=headers, json=json_body)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict):
                return data
    except (httpx.HTTPError, ValueError):
        return None
    return None
