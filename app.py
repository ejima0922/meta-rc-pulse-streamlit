import base64
import os
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

try:
    import requests
except ImportError:
    requests = None

st.set_page_config(
    page_title="Meta RC Pulse | あなたの夢に、確かな一歩を。",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT_DIR = Path(__file__).resolve().parent
EMBEDDED_DIR = ROOT_DIR / "embedded"


def read_embedded_text(name: str) -> str:
    try:
        return (EMBEDDED_DIR / name).read_text(encoding="utf-8").strip()
    except Exception:
        return ""


GUIDE_IMAGE_B64 = read_embedded_text("guide.b64")
FACADE_VIDEO_B64 = "".join(
    read_embedded_text(name)
    for name in ("facade_01.b64", "facade_02.b64", "facade_03.b64")
)


def get_secret(name: str) -> str:
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return str(value or os.environ.get(name, "")).strip()


def send_to_sheet(payload: dict) -> dict:
    url = get_secret("APPS_SCRIPT_WEB_APP_URL")
    if not url:
        return {"ok": None, "message": "受付先の接続を確認中です", "mail_sent": False}
    if requests is None:
        return {"ok": False, "message": "送信機能を確認中です", "mail_sent": False}
    try:
        response = requests.post(url, json=payload, timeout=12)
        try:
            data = response.json()
        except ValueError:
            data = {}
        if response.ok and data.get("ok") is True:
            return data
        return {
            "ok": False,
            "message": data.get("message") or "受付に失敗しました",
            "mail_sent": False,
        }
    except Exception:
        return {"ok": False, "message": "受付に失敗しました", "mail_sent": False}


st.markdown(
    """
<style>
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] {display:none !important;}
html, body, [data-testid="stAppViewContainer"], .stApp {
  background:
    radial-gradient(circle at 16% 10%, rgba(44,104,208,.20), transparent 34%),
    radial-gradient(circle at 84% 8%, rgba(36,166,220,.12), transparent 30%),
    radial-gradient(circle at 50% 72%, rgba(204,151,67,.08), transparent 36%),
    linear-gradient(155deg,#01030a 0%,#040b1a 46%,#01030a 100%) !important;
  color:#fff;
}
.block-container {max-width:1120px; padding:1.1rem 1rem 5rem !important;}
.hero-kicker {text-align:center;color:#d8b879;font-weight:800;letter-spacing:.16em;font-size:.82rem;margin:.5rem 0 .7rem;}
.hero-help {text-align:center;color:rgba(242,248,255,.94);font-size:clamp(1.02rem,2.2vw,1.28rem);font-weight:800;line-height:1.7;margin:0 auto 1rem;}
.hero-help small {display:block;color:rgba(217,230,245,.70);font-size:.78rem;font-weight:650;margin-top:.35rem;}
.guide-stage {position:relative;max-width:920px;margin:0 auto;border-radius:28px;overflow:hidden;border:1px solid rgba(213,176,103,.36);box-shadow:0 30px 90px rgba(0,0,0,.48),0 0 46px rgba(44,125,209,.14);}
.guide-stage img {display:block;width:100%;height:auto;}
.guide-hit {position:absolute;z-index:5;border:1px solid transparent;border-radius:20px;}
.guide-hit:hover {border-color:rgba(255,226,164,.9);box-shadow:0 0 30px rgba(255,205,100,.34);background:rgba(255,255,255,.03);}
.guide-hit.female {left:32.9%;top:32.6%;width:17.5%;height:13.5%;}
.guide-hit.male {left:50.8%;top:32.6%;width:17.5%;height:13.5%;}
.guide-caption {text-align:center;color:rgba(226,238,255,.72);font-size:.79rem;margin:.65rem 0 1rem;}
.selection-note {max-width:760px;margin:1rem auto;text-align:center;padding:.85rem 1rem;border-radius:999px;border:1px solid rgba(214,179,107,.35);background:rgba(20,29,48,.58);color:#fff1ca;font-weight:800;}
section.pulse-section {margin:clamp(3rem,7vw,5.5rem) auto;max-width:1020px;}
.section-eyebrow {color:#d9b26a;font-size:.78rem;letter-spacing:.17em;font-weight:900;text-align:center;margin-bottom:.65rem;}
.section-title {text-align:center;font-size:clamp(2rem,5.2vw,4rem);line-height:1.15;margin:0;color:#fff;font-weight:950;letter-spacing:-.035em;}
.section-copy {max-width:800px;margin:1rem auto 0;text-align:center;color:rgba(225,237,250,.80);line-height:1.9;font-size:clamp(.98rem,1.8vw,1.14rem);}
[data-testid="stVideo"] video {border-radius:24px !important;box-shadow:0 28px 80px rgba(0,0,0,.46),0 0 38px rgba(60,190,255,.11);border:1px solid rgba(213,176,103,.30);}
.form-shell {max-width:840px;margin:2rem auto;padding:clamp(1.1rem,3vw,1.8rem);border-radius:26px;border:1px solid rgba(107,225,244,.24);background:rgba(4,12,28,.78);box-shadow:0 22px 70px rgba(0,0,0,.35);}
div[data-testid="stForm"] label {color:#eaf6ff !important;font-weight:800 !important;}
div[data-testid="stTextInput"] input {background:rgba(250,253,255,.96) !important;color:#061124 !important;border-radius:14px !important;}
.stButton button, div[data-testid="stFormSubmitButton"] button {width:100%;min-height:3.7rem;border-radius:999px !important;font-weight:900 !important;border:1px solid rgba(219,181,108,.55) !important;background:linear-gradient(135deg,#e7c77f,#9a6b25) !important;color:#07101c !important;}
.flow-words {display:flex;flex-wrap:wrap;justify-content:center;gap:.6rem;margin:1.4rem auto;}
.flow-words span {padding:.65rem 1rem;border-radius:999px;border:1px solid rgba(113,225,245,.25);background:rgba(13,42,70,.40);color:#dffaff;font-weight:800;}
.three-grid {display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:1.4rem;}
.value-cell {padding:1.2rem;border-radius:22px;border:1px solid rgba(214,177,104,.26);background:linear-gradient(145deg,rgba(13,22,42,.82),rgba(6,12,26,.80));text-align:center;}
.value-cell strong {display:block;color:#fff2c9;font-size:1.12rem;margin-bottom:.35rem;}
.value-cell span {color:rgba(222,236,250,.72);font-size:.9rem;line-height:1.6;}
.result-box {max-width:840px;margin:1.2rem auto;padding:1.2rem;border-radius:22px;border:1px solid rgba(88,236,184,.32);background:rgba(9,51,43,.42);text-align:center;}
.result-box strong {display:block;font-size:clamp(1.45rem,4vw,2.2rem);color:#e8fff7;}
.result-box span {display:block;margin-top:.45rem;color:rgba(215,241,233,.78);}
.gate-note {max-width:840px;margin:1rem auto;padding:1rem 1.15rem;border-radius:20px;border:1px solid rgba(222,184,111,.25);background:rgba(13,20,37,.72);color:rgba(236,242,250,.80);line-height:1.75;text-align:center;}
.course {padding:clamp(1.4rem,4vw,2.4rem);border-radius:30px;border:1px solid rgba(222,184,111,.38);background:radial-gradient(circle at 50% 0%,rgba(218,166,66,.15),transparent 42%),rgba(5,10,23,.82);text-align:center;}
.course-price {font-size:clamp(2.3rem,6vw,4.4rem);font-weight:950;color:#fff0bd;margin:.5rem 0;}
.course-note {color:rgba(226,238,250,.72);line-height:1.75;}
@media(max-width:640px) {
 .block-container {padding:.6rem .65rem 4rem !important;}
 .guide-stage {border-radius:20px;}
 .guide-hit {border-radius:14px;}
 .three-grid {grid-template-columns:1fr;}
 .section-title {font-size:clamp(1.9rem,10vw,3rem);}
}
</style>
""",
    unsafe_allow_html=True,
)

selected = str(st.query_params.get("guide", "") or "").lower()
if selected not in {"female", "male"}:
    selected = ""

img_uri = f"data:image/webp;base64,{GUIDE_IMAGE_B64}" if GUIDE_IMAGE_B64 else ""
selected_label = "女性パルス" if selected == "female" else "男性パルス" if selected == "male" else ""

st.markdown('<div class="hero-kicker">META RC PULSE</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-help">案内人を選んで、Meta RC Pulseを始めてください。'
    '<small>写真の「女性」「男性」をタップできます。音声は、あなたが開始するまで流れません。</small></div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'''<div class="guide-stage">
      <img src="{img_uri}" alt="Meta RC Pulse 女性・男性パルス案内人">
      <a class="guide-hit female" href="?guide=female" target="_self" aria-label="女性パルスを選ぶ"></a>
      <a class="guide-hit male" href="?guide=male" target="_self" aria-label="男性パルスを選ぶ"></a>
    </div>''',
    unsafe_allow_html=True,
)
st.markdown('<div class="guide-caption">深い宇宙、紺とゴールド。ここから土地の未来へ入ります。</div>', unsafe_allow_html=True)

if selected_label:
    st.markdown(f'<div class="selection-note">{selected_label}を選択しました。中央の光から先へ進みます。</div>', unsafe_allow_html=True)
    if st.button("✦ パルスを呼び出す", key="start_pulse"):
        st.session_state["pulse_started"] = True
    if st.session_state.get("pulse_started"):
        st.info("ようこそ、Meta RC パルスへ。私は、パルスと申します。本日はコンシェルジュとして、お客様をご案内いたします。")
else:
    st.markdown('<div class="selection-note">まず「女性」または「男性」をタップしてください。</div>', unsafe_allow_html=True)

st.markdown(
    '<section class="pulse-section"><div class="section-eyebrow">FIRST IMPRESSION</div>'
    '<h2 class="section-title">想像した建物が、<br>そのまま目の前に現れる。</h2>'
    '<p class="section-copy">昼は街になじみ、夜は街に笑顔を灯す。まずは、その景色をご覧ください。</p></section>',
    unsafe_allow_html=True,
)
if FACADE_VIDEO_B64:
    st.video(base64.b64decode(FACADE_VIDEO_B64), autoplay=True, muted=True, loop=True)
else:
    st.warning("建物イメージ動画を読み込んでいます。")
st.markdown('<p class="section-copy" style="margin-top:.7rem">この建物が、あなたの土地に生まれる可能性があります。</p>', unsafe_allow_html=True)

st.markdown(
    '<section class="pulse-section"><div class="section-eyebrow">YOUR LAND</div>'
    '<h2 class="section-title">この土地の可能性を、<br>パルスに聞く。</h2>'
    '<p class="section-copy">住所ごとの根拠を確認してから、想定月々純利益をご案内します。固定のサンプル金額は使いません。</p></section>',
    unsafe_allow_html=True,
)

st.markdown('<div class="form-shell">', unsafe_allow_html=True)
with st.form("pulse_land_request", clear_on_submit=False):
    address = st.text_input("希望建築地住所", placeholder="例：東京都世田谷区…")
    name = st.text_input("お名前", placeholder="お名前")
    email = st.text_input("メールアドレス", placeholder="name@example.com")
    submitted = st.form_submit_button("この土地の可能性を確認する →")
st.markdown('</div>', unsafe_allow_html=True)

if submitted:
    # 別住所で以前の結果や確認状態を使い回さない。
    st.session_state.pop("verified_monthly_profit_yen", None)
    st.session_state["building_overview_ack"] = False

    if not address.strip():
        st.error("希望建築地住所を入力してください。")
    else:
        payload = {
            "source": "meta-rc-pulse-streamlit-latest-lp",
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "name": name.strip(),
            "email": email.strip(),
            "desired_building_address": address.strip(),
            "希望建築地住所": address.strip(),
            "address": address.strip(),
        }
        result = send_to_sheet(payload)
        if result.get("ok") is True:
            st.success(result.get("message") or "受付しました。")
        elif result.get("ok") is None:
            st.info("住所を受け付けました。公開側の根拠連携を確認後、結果を表示します。")
        else:
            st.warning(result.get("message") or "受付接続を確認中です。")

        candidate_profit = result.get("monthly_profit_yen")
        if (
            result.get("profit_verified") is True
            and isinstance(candidate_profit, int)
            and candidate_profit > 0
        ):
            st.session_state["verified_monthly_profit_yen"] = candidate_profit
        else:
            st.markdown(
                '<div class="result-box"><strong>想定 月々純利益：確認後に表示</strong>'
                '<span>法規・敷地条件・建築費・賃料等の案件根拠が確認できるまで、金額は表示しません。</span></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="gate-note">月々純利益が実際に表示されるまでは、建物概要・三方よし・パルスコース料金を表示しません。</div>',
                unsafe_allow_html=True,
            )

verified_profit = st.session_state.get("verified_monthly_profit_yen")

# Gate 1: 月々純利益が根拠付きで実際に表示済みでなければ、ここより先は出さない。
if isinstance(verified_profit, int) and verified_profit > 0:
    st.markdown(
        f'<div class="result-box"><strong>想定 月々純利益 ¥{verified_profit:,} / 月</strong>'
        '<span>案件根拠に基づく確認済み結果です。保証値ではありません。</span></div>',
        unsafe_allow_html=True,
    )

    # Gate 2: 利益表示後に初めて建物概要を見せる。
    st.markdown(
        '''<section class="pulse-section">
<div class="section-eyebrow">WHY THIS BUILDING</div>
<h2 class="section-title">音楽。映像。配信。SNS。<br>創る人が、住みたくなる場所へ。</h2>
<div class="flow-words"><span>MUSIC</span><span>VIDEO</span><span>STREAMING</span><span>SNS</span><span>CREATOR</span></div>
<p class="section-copy">住む場所と創る場所が近づくことで、建物の価値に新しい理由が生まれます。ここでは建物の考え方だけをご案内し、全貌・詳細3DCG・VRはまだ公開しません。</p>
</section>''',
        unsafe_allow_html=True,
    )

    if st.button("建物概要を確認しました → 続きを見る", key="ack_building_overview"):
        st.session_state["building_overview_ack"] = True

# Gate 3: 建物概要確認後に初めて思想・コース案内・料金を表示する。
if (
    isinstance(verified_profit, int)
    and verified_profit > 0
    and st.session_state.get("building_overview_ack") is True
):
    st.markdown(
        '''<section class="pulse-section">
<div class="section-eyebrow">DAY / NIGHT</div>
<h2 class="section-title">昼は、街になじむ。<br>夜は、街に笑顔を灯す。</h2>
<p class="section-copy">ガラスに季節が映り、夜は静かなラインライトが街へ小さな景色を返す。街の灯りを奪うのではなく、月夜にそっと寄り添う光へ。</p>
</section>
<section class="pulse-section">
<div class="section-eyebrow">THREE-WAY VALUE</div>
<h2 class="section-title">住む人。地域の人。建物を持つ人。<br>三方よし。</h2>
<div class="three-grid"><div class="value-cell"><strong>CREATOR</strong><span>住みながら、創作できる。</span></div><div class="value-cell"><strong>TOWN</strong><span>昼はなじみ、夜は景色を返す。</span></div><div class="value-cell"><strong>OWNER</strong><span>土地を、長く価値を生む建物へ。</span></div></div>
</section>
<section class="pulse-section course">
<div class="section-eyebrow">PULSE COURSE</div>
<h2 class="section-title">あなたが今見たのは、<br>まだ、この土地の可能性の入口です。</h2>
<div class="course-price">月額 9,800円</div>
<p class="course-note">パルスコースでは、詳細3DCG・提案図面・VRなどを通して、この土地に生まれる建物をさらに深く確認していきます。金額・法規・建築可否は案件根拠と有資格者確認に基づいて扱います。</p>
</section>''',
        unsafe_allow_html=True,
    )
