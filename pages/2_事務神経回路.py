"""Passive quarantine for the retired public operations preview route."""
from __future__ import annotations

import streamlit as st

PREVIEW_AUTHORITY_CLASSIFICATION = "CONFLICTING"
PREVIEW_AUTHORITY_TREATMENT = "LEGACY_QUARANTINE"
CANONICAL_ISSUE = 599

st.set_page_config(page_title="プレビュー終了", page_icon="🔒", layout="centered")
st.title("🔒 このプレビューは終了しました")
st.info("このページは現在の案件・請求・予約・通知・運用状態を示す権限を持ちません。")
st.stop()
