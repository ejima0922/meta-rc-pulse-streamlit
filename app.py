"""Passive quarantine entrypoint for the retired Meta RC Pulse Streamlit preview."""
from __future__ import annotations

import streamlit as st

PREVIEW_AUTHORITY_CLASSIFICATION = "CONFLICTING"
PREVIEW_AUTHORITY_TREATMENT = "LEGACY_QUARANTINE"
CANONICAL_ISSUE = 599

st.set_page_config(page_title="プレビュー終了", page_icon="🔒", layout="centered")
st.markdown(
    """
    <style>
    #MainMenu, footer, header, [data-testid="stToolbar"] {display:none !important;}
    .stApp {background:#020817;color:#fff;}
    .retired {max-width:680px;margin:20vh auto;padding:2rem;border:1px solid #31425f;
      border-radius:24px;background:#071225;text-align:center;}
    .retired h1 {font-size:clamp(1.8rem,6vw,3rem);}
    .retired p {color:#c7d4e8;line-height:1.8;}
    </style>
    <div class="retired">
      <h1>このプレビューは終了しました</h1>
      <p>この公開プレビューは現在の正式版・事実・権限を示しません。</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.stop()
