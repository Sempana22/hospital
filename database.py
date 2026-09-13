"""Supabase database connection and query functions."""

from datetime import datetime, timezone
from urllib.parse import urlparse
from uuid import UUID

import streamlit as st
from supabase import create_client, Client


class DatabaseConfigError(Exception):
    """Raised when Supabase secrets are missing or invalid."""


@st.cache_resource(show_spinner=False)
def get_client() -> Client:
    """Create and cache the Supabase client.

    Raises DatabaseConfigError with a friendly message instead of letting
    a raw KeyError/FileNotFoundError bubble up when secrets.toml is
    missing or incomplete.
    """
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except (KeyError, FileNotFoundError) as exc:
        raise DatabaseConfigError(
            "Konfigurasi Supabase belum lengkap. Pastikan file "
            "`.streamlit/secrets.toml` berisi SUPABASE_URL dan SUPABASE_KEY."
        ) from exc

    parsed_url = urlparse(str(url))
    key_text = str(key).strip()
    placeholder_values = (
        "xxxxxxxxxxxx",
        "project-id-anda",
        "your-anon-public-key",
        "NOMOR-ANDA",
    )
    if (
        not url
        or not key
        or parsed_url.scheme != "https"
        or not parsed_url.hostname
        or not parsed_url.hostname.endswith(".supabase.co")
        or any(value in str(url) or value in key_text for value in placeholder_values)
    ):
        raise DatabaseConfigError(
            "SUPABASE_URL / SUPABASE_KEY masih kosong atau berisi nilai contoh. "
            "Isi dengan Project URL dan anon key dari dashboard Supabase Anda."
        )

    try:
        UUID(key_text)
    except ValueError:
        pass
    else:
        raise DatabaseConfigError(
            "SUPABASE_KEY berisi Project ID, bukan API key. Salin anon/public "
            "key dari Supabase Dashboard > Settings > API."
        )

    try:
        return create_client(url, key)
    except Exception as exc:  # noqa: BLE001 - surface as config error
        raise DatabaseConfigError(f"Gagal terhubung ke Supabase: {exc}") from exc


def insert_response(data: dict) -> dict:
    """Insert a questionnaire response into the 'responses' table."""
    payload = dict(data)
    if "created_at" not in payload or payload["created_at"] is None:
        payload["created_at"] = datetime.now(timezone.utc).isoformat()

    client = get_client()
    try:
        result = client.table("responses").insert(payload).execute()
        return result.data[0] if result.data else {}
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Gagal menyimpan data ke database: {exc}") from exc


def fetch_responses() -> list[dict]:
    """Fetch all responses ordered by created_at descending."""
    client = get_client()
    try:
        result = (
            client.table("responses")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return result.data or []
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Gagal mengambil data responden: {exc}") from exc


def fetch_response_by_code(code: str) -> dict | None:
    """Fetch a single response by respondent_code."""
    client = get_client()
    try:
        result = (
            client.table("responses")
            .select("*")
            .eq("respondent_code", code)
            .limit(1)
            .execute()
        )
        return result.data[0] if result.data else None
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Gagal mengambil data responden: {exc}") from exc


def fetch_feedback() -> list[dict]:
    """Fetch all responses that include feedback/saran."""
    client = get_client()
    try:
        result = (
            client.table("responses")
            .select("respondent_code, created_at, saran")
            .not_.is_("saran", "null")
            .neq("saran", "")
            .order("created_at", desc=True)
            .execute()
        )
        return result.data or []
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Gagal mengambil data saran/kritik: {exc}") from exc


def delete_response_by_code(code: str) -> bool:
    """Delete one respondent record by code."""
    if not code or not code.strip():
        raise ValueError("Kode responden wajib diisi.")

    client = get_client()
    try:
        result = (
            client.table("responses")
            .delete()
            .eq("respondent_code", code.strip())
            .execute()
        )
        return bool(result.data)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Gagal menghapus data responden: {exc}") from exc
