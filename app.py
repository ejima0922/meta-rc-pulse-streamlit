import os
from datetime import datetime, timezone

import streamlit as st

try:
    import requests
except ImportError:
    requests = None

st.set_page_config(
    page_title="Meta RC Pulse | 宇宙型ランディングページ",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
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
        return {"ok": None, "message": "外部保存URLが未接続です", "mail_sent": False}
    if requests is None:
        return {"ok": False, "message": "送信ライブラリを確認中です", "mail_sent": False}
    try:
        response = requests.post(url, json=payload, timeout=12)
        try:
            data = response.json()
        except ValueError:
            data = {}
        if response.ok and data.get("ok") is True:
            return data
        return {"ok": False, "message": data.get("message") or "外部保存に失敗しました", "mail_sent": False}
    except Exception:
        return {"ok": False, "message": "外部保存に失敗しました", "mail_sent": False}


st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {max-width: 100% !important; padding: 0 0 4rem !important;}
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 80% 10%, rgba(84,216,255,.16), transparent 30%),
                    radial-gradient(circle at 50% 110%, rgba(49,132,255,.22), transparent 34%),
                    linear-gradient(180deg,#02040b 0%,#06101f 52%,#02040b 100%);
        color: white;
    }
    .hero {min-height: 86vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 88px 18px 50px;}
    .pill {border: 1px solid rgba(95,255,210,.32); background: rgba(95,255,210,.10); color: #c8fff3; border-radius: 999px; padding: 8px 16px; font-weight: 900;}
    .hero h1 {font-size: clamp(44px, 9vw, 92px); line-height: 1.04; letter-spacing: -.06em; margin: 22px 0 0; font-weight: 1000;}
    .grad {background: linear-gradient(90deg,#fff,#5fffd2,#54d8ff,#fff); -webkit-background-clip: text; background-clip: text; color: transparent;}
    .lead {max-width: 880px; color: #cbd6e4; line-height: 2; font-size: clamp(15px,2.4vw,19px); margin: 24px auto 0;}
    .card {width: min(980px, calc(100% - 32px)); margin: 28px auto; border: 1px solid rgba(84,216,255,.24); background: rgba(3,8,20,.76); border-radius: 30px; padding: clamp(22px,4vw,34px); box-shadow: 0 0 60px rgba(84,216,255,.10);}
    .card h2 {font-size: clamp(30px,5vw,52px); margin: 0 0 14px; letter-spacing: -.04em;}
    .card p {color: rgba(226,238,255,.82); line-height: 1.9;}
    .flow {display: grid; grid-template-columns: repeat(auto-fit, minmax(145px,1fr)); gap: 12px; margin-top: 20px;}
    .flow div {border: 1px solid rgba(95,255,210,.22); background: rgba(95,255,210,.08); border-radius: 18px; padding: 16px; text-align: center; font-weight: 900;}
    .form-card {width: min(780px, calc(100% - 32px)); margin: 30px auto 80px; border: 1px solid rgba(84,216,255,.28); background: rgba(3,8,20,.86); border-radius: 30px; padding: 28px; box-shadow: 0 0 70px rgba(84,216,255,.16);}
    div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label, div[data-testid="stCheckbox"] label {color: #eaffff !important; font-weight: 850 !important;}
    div[data-testid="stCheckbox"] {border: 1px solid rgba(95,255,210,.30); background: rgba(95,255,210,.07); border-radius: 16px; padding: 8px 12px; margin: 8px 0;}
    .stButton button {width: 100%; border: 0 !important; border-radius: 999px !important; padding: .95rem 1.2rem !important; font-weight: 950 !important; color: #00131d !important; background: linear-gradient(135deg,#5fffd2,#54d8ff,#337dff) !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
      <div class="pill">契約決定までをパルスコースで完結</div>
      <h1>住所を聞いた瞬間、<br><span class="grad">商談が動き出す。</span></h1>
      <p class="lead">建設会社の営業マンが、住所を聞いたその場から法規・最大ボリューム・3DCG没入体験・提案平面図・立面図・概算積算・収益提案までを組み立てるためのAI営業支援システム。</p>
    </section>
    <section class="card">
      <h2>営業マンの初期提案力を、<span class="grad">建築士へ渡せるレベルへ。</span></h2>
      <p>公的情報優先、5点照合、安全型の緩和採用。まずは投資家と土地オーナー様に、可能性と完成イメージを前向きに届けます。</p>
      <div class="flow"><div>住所</div><div>法規</div><div>最大ボリューム</div><div>3DCG没入体験</div><div>概算積算</div><div>収益提案</div></div>
    </section>
    <section class="form-card">
      <h2>本物送信用フォーム</h2>
      <p>希望建築地住所を入れると、Googleスプレッドシート保存ルートへ送信します。</p>
    """,
    unsafe_allow_html=True,
)

with st.form("agp_real_registration_form", clear_on_submit=False):
    name = st.text_input("お名前", value="テスト 太郎")
    email = st.text_input("メールアドレス", value="test@example.com")
    address = st.text_input("希望建築地住所", value="東京都港区六本木1丁目1-1")
    country = st.text_input("国", value="日本")
    company = st.text_input("会社名", value="テスト建設")
    language = st.selectbox("希望言語", ["日本語", "English", "中文", "한국어", "Español"])
    is_builder_sales = st.checkbox("建築営業マンですか？", value=True)
    wants_demo = st.checkbox("デモ予約も希望する", value=True)
    submitted = st.form_submit_button("希望建築地住所を入れて、商談を動かす →")

if submitted:
    sales_value = "はい" if is_builder_sales else "いいえ"
    demo_value = "はい" if wants_demo else "いいえ"
    payload = {
        "source": "meta-rc-pulse-streamlit-cosmic-lp",
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "name": name.strip(),
        "email": email.strip(),
        "desired_building_address": address.strip(),
        "希望建築地住所": address.strip(),
        "address": address.strip(),
        "phone": address.strip(),
        "country": country.strip(),
        "company": company.strip(),
        "company_name": company.strip(),
        "preferred_language": language,
        "preferredLanguage": language,
        "is_sales_person": sales_value,
        "isSalesPerson": sales_value,
        "is_builder_sales": sales_value,
        "builder_sales": sales_value,
        "建築営業マン": sales_value,
        "wants_demo": demo_value,
        "wantsDemo": demo_value,
        "demo_requested": demo_value,
        "デモ予約希望": demo_value,
    }
    result = send_to_sheet(payload)
    if result.get("ok") is True:
        st.success(result.get("message") or "Googleスプレッドシートへ保存しました")
        if result.get("mail_sent"):
            st.info("自動返信メールを送信しました")
        if result.get("admin_mail_sent"):
            st.info("管理者通知メールを送信しました")
    elif result.get("ok") is None:
        st.warning(result.get("message") or "外部保存URLが未接続です")
    else:
        st.error(result.get("message") or "外部保存に失敗しました")

st.markdown("</section>", unsafe_allow_html=True)
