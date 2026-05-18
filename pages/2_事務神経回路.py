import streamlit as st
from datetime import datetime, date

st.set_page_config(
    page_title="事務神経回路 | Meta RC Pulse",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 事務神経回路 — 経理雑務完全処理システム")
st.caption("案件ID単位で抜け漏れを機械的に検出します")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 案件管理",
    "💰 請求・入金",
    "🏢 施設予約",
    "🔧 修繕管理",
    "📊 月次サマリー"
])with tab1:
    st.subheader("📋 案件一覧")
    cases = [
        {"id": "MRC-202605-0001", "client": "株式会社山田建設", "address": "東京都世田谷区桜新町2-15-1", "status": "IN_PROGRESS", "amount": 580_000_000},
        {"id": "MRC-202605-0002", "client": "佐藤工務店", "address": "神奈川県横浜市中区山手町12-3", "status": "PENDING", "amount": 420_000_000},
        {"id": "MRC-202604-0003", "client": "田中建設株式会社", "address": "大阪府大阪市北区梅田1-2-3", "status": "OVERDUE", "amount": 650_000_000},
        {"id": "MRC-202604-0004", "client": "鈴木ホーム", "address": "愛知県名古屋市中区栄3-1-1", "status": "COMPLETED", "amount": 520_000_000},
    ]
    status_labels = {
        "PENDING": "⏳ 処理待ち",
        "IN_PROGRESS": "🔵 対応中",
        "OVERDUE": "🔴 期限超過",
        "COMPLETED": "✅ 完了",
    }
    overdue = [c for c in cases if c["status"] == "OVERDUE"]
    if overdue:
        st.error(f"🚨 期限超過案件が{len(overdue)}件あります！")
    for c in cases:
        with st.expander(f"{c['id']} | {c['client']} | {status_labels[c['status']]}"):
            col1, col2 = st.columns(2)
            col1.write(f"**住所**: {c['address']}")
            col2.write(f"**契約金額**: ¥{c['amount']:,}")
            checks = ["見積提出","契約書送付","頭金入金","着工確認","中間金入金","竣工確認","最終入金"]
            cols = st.columns(len(checks))
            for i, check in enumerate(checks):
                cols[i].checkbox(check, key=f"{c['id']}_{i}")
    st.divider()
    st.subheader("＋ 新規案件登録")
    with st.form("new_case"):
        col1, col2 = st.columns(2)
        with col1:
            new_client = st.text_input("顧客名・会社名")
            new_address = st.text_input("物件住所")
        with col2:
            new_amount = st.number_input("概算契約金額（万円）", value=58000, step=1000)
        if st.form_submit_button("案件IDを発行して登録", use_container_width=True):
            new_id = f"MRC-{datetime.now().strftime('%Y%m')}-{len(cases)+1:04d}"
            st.success(f"✅ 案件ID発行: **{new_id}**")with tab2:
    st.subheader("💰 請求・入金管理")
    invoices = [
        {"id": "INV-0001", "case_id": "MRC-202605-0001", "client": "山田建設", "amount": 29_000_000, "due": "2026-05-31", "status": "未入金"},
        {"id": "INV-0002", "case_id": "MRC-202604-0003", "client": "田中建設", "amount": 65_000_000, "due": "2026-04-30", "status": "期限超過"},
        {"id": "INV-0003", "case_id": "MRC-202604-0004", "client": "鈴木ホーム", "amount": 52_000_000, "due": "2026-05-10", "status": "入金済"},
    ]
    total_unpaid = sum(i["amount"] for i in invoices if i["status"] in ["未入金","期限超過"])
    total_paid = sum(i["amount"] for i in invoices if i["status"] == "入金済")
    col1, col2, col3 = st.columns(3)
    col1.metric("未入金合計", f"¥{total_unpaid:,}")
    col2.metric("入金済合計", f"¥{total_paid:,}")
    col3.metric("期限超過", f"{len([i for i in invoices if i['status']=='期限超過'])}件")
    st.divider()
    for inv in invoices:
        color = "🔴" if inv["status"] == "期限超過" else "🟡" if inv["status"] == "未入金" else "🟢"
        with st.expander(f"{color} {inv['id']} | {inv['client']} | ¥{inv['amount']:,} | {inv['status']}"):
            col1, col2 = st.columns(2)
            col1.write(f"**案件ID**: {inv['case_id']}")
            col2.write(f"**支払期限**: {inv['due']}")
            if inv["status"] != "入金済":
                if st.button(f"督促メール送信", key=f"remind_{inv['id']}"):
                    st.success("督促メールを送信しました")with tab3:
    st.subheader("🏢 施設予約管理")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🎵 地下ラボ予約（本日）")
        bookings = [
            {"time": "09:00-09:50", "room": "Bタイプ1", "user": "田中太郎", "status": "確定"},
            {"time": "10:00-10:50", "room": "Cタイプ1", "user": "佐藤花子", "status": "確定"},
            {"time": "13:00-13:50", "room": "Bタイプ2", "user": "外部利用者", "status": "確定", "referrer": "102号室 山田"},
            {"time": "15:00-15:50", "room": "Bタイプ1", "user": "（空き）", "status": "空き"},
        ]
        for b in bookings:
            color = "🟢" if b["status"] == "確定" else "⬜"
            ref = f" ← 紹介:{b.get('referrer','')}" if b.get("referrer") else ""
            st.markdown(f"{color} `{b['time']}` {b['room']} | {b['user']}{ref}")
    with col2:
        st.markdown("#### 🥽 VR予約（今週）")
        vr = [
            {"date": "2026-05-19", "time": "14:00", "client": "山田建設 様", "type": "初回提案"},
            {"date": "2026-05-21", "time": "10:00", "client": "田中工務店 様", "type": "再提案"},
            {"date": "2026-05-22", "time": "15:00", "client": "（空き）", "type": "—"},
        ]
        for v in vr:
            color = "🔵" if v["client"] != "（空き）" else "⬜"
            st.markdown(f"{color} {v['date']} {v['time']} | {v['client']}")
    st.divider()
    with st.form("new_booking"):
        st.markdown("#### ➕ 新規予約登録")
        col1, col2, col3 = st.columns(3)
        with col1:
            booking_type = st.selectbox("種別", ["地下ラボ", "VR体験"])
            booking_date = st.date_input("日付", value=date.today())
        with col2:
            booking_time = st.time_input("開始時刻")
            booking_user = st.text_input("利用者名")
        with col3:
            booking_room = st.selectbox("部屋", ["Bタイプ1", "Bタイプ2", "Bタイプ3", "Cタイプ1"])
            referrer_unit = st.text_input("紹介者（入居者番号）", placeholder="例:102")
        if st.form_submit_button("予約を登録", use_container_width=True):
            st.success(f"✅ 予約登録完了 | {booking_date} | {booking_user}")with tab4:
    st.subheader("🔧 破損報告・修繕管理")
    repairs = [
        {"id": "REP-001", "location": "201号室 洗面台", "report": "蛇口から水漏れ", "reported": "2026-05-17", "status": "対応中", "vendor": "水道業者A"},
        {"id": "REP-002", "location": "地下ラボBタイプ2", "report": "LED壁面一部点灯不良", "reported": "2026-05-18", "status": "業者待ち", "vendor": "LED業者B"},
        {"id": "REP-003", "location": "共用部エントランス", "report": "顔認証ドア反応遅延", "reported": "2026-05-15", "status": "完了", "vendor": "セキュリティ業者C"},
    ]
    for r in repairs:
        color = "🔴" if r["status"] == "業者待ち" else "🟡" if r["status"] == "対応中" else "🟢"
        with st.expander(f"{color} {r['id']} | {r['location']} | {r['status']}"):
            col1, col2 = st.columns(2)
            col1.write(f"**報告内容**: {r['report']}")
            col1.write(f"**報告日**: {r['reported']}")
            col2.write(f"**担当業者**: {r['vendor']}")
    st.divider()
    with st.form("new_repair"):
        st.markdown("#### ➕ 破損報告")
        col1, col2 = st.columns(2)
        with col1:
            repair_location = st.text_input("場所（例: 301号室 エアコン）")
            repair_content = st.text_area("破損・不具合内容", height=80)
        with col2:
            repair_vendor = st.text_input("対応業者")
            repair_urgency = st.selectbox("緊急度", ["通常", "急ぎ", "緊急"])
        if st.form_submit_button("報告を登録", use_container_width=True):
            st.success(f"✅ 破損報告登録完了 | 管理者に通知されます")

with tab5:
    st.subheader("📊 月次サマリー — 2026年5月")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("新規案件", "2件")
    col2.metric("請求総額", "¥94,000,000")
    col3.metric("入金済", "¥52,000,000")
    col4.metric("未入金", "¥42,000,000")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 経費サマリー")
        st.markdown("""
| カテゴリ | 金額 |
|---|---|
| 清掃費 | ¥240,000 |
| 修繕費 | ¥85,000 |
| 通信費 | ¥32,000 |
| 消耗品 | ¥18,000 |
| **合計** | **¥375,000** |
""")
    with col2:
        st.markdown("#### 収益サマリー")
        st.markdown("""
| 収益源 | 金額 |
|---|---|
| 地下ラボ時間貸し | ¥2,073,600 |
| ワンルーム賃料 | ¥1,915,200 |
| デリバリー | ¥57,600 |
| 自販機 | ¥15,000 |
| **合計** | **¥4,061,400** |
""")
    st.divider()
    if st.button("📄 月次レポートを生成", use_container_width=True):
        st.success("レポートを生成しました（Zapier連携後に自動化）")
