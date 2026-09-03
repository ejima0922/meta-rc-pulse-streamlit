from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROUTES = (
    ROOT / "app.py",
    ROOT / "pages" / "1_積算エンジン.py",
    ROOT / "pages" / "2_事務神経回路.py",
)

FORBIDDEN_EXECUTABLE_TOKENS = (
    "exec(compile(",
    "run_17steps(",
    "form_submit_button(",
    "st.button(",
    "st.success(",
    "sendEmail",
    "MailApp",
    "GmailApp",
    "requests.",
    "urlopen(",
)


def test_retired_public_routes_are_passive_quarantine() -> None:
    for path in PUBLIC_ROUTES:
        source = path.read_text(encoding="utf-8")
        assert 'PREVIEW_AUTHORITY_TREATMENT = "LEGACY_QUARANTINE"' in source
        assert "CANONICAL_ISSUE = 599" in source
        assert "st.stop()" in source
        for token in FORBIDDEN_EXECUTABLE_TOKENS:
            assert token not in source, f"{path}: forbidden executable token {token!r}"
