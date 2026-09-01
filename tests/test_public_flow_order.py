from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[1] / "app_core.py").read_text(encoding="utf-8")


def test_public_flow_starts_with_microphone_then_guide_choice() -> None:
    microphone_gate = SOURCE.index('if entry_stage != "guide" and not selected:')
    microphone_stop = SOURCE.index("st.stop()", microphone_gate)
    guide_stage = SOURCE.index('class="guide-stage"')

    assert microphone_gate < microphone_stop < guide_stage
    assert 'href="?entry=guide"' in SOURCE
    assert '?entry=guide&amp;guide=female' in SOURCE
    assert '?entry=guide&amp;guide=male' in SOURCE
    assert "マイクを自動では開始しません" in SOURCE


def test_approved_video_is_motion_first_and_local() -> None:
    assert "st.video(base64.b64decode(FACADE_VIDEO_B64), autoplay=True, muted=True, loop=True)" in SOURCE
    assert "FACADE_VIDEO_B64" in SOURCE


def test_course_price_remains_behind_the_last_evidence_gates() -> None:
    profit_gate = SOURCE.index("if isinstance(verified_profit, int) and verified_profit > 0:")
    overview_gate = SOURCE.index('st.session_state.get("building_overview_ack") is True')
    course_price = SOURCE.index('<div class="course-price">月額 9,800円</div>')

    assert profit_gate < overview_gate < course_price
    assert "Gate 3: 建物概要確認後に初めて思想・コース案内・料金を表示する" in SOURCE
