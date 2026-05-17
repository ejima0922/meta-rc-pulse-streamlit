import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from engine_17steps import run_17steps

st.set_page_config(page_title="17工程積算エンジン", page_icon="🏗️", layout="wide")

st.title("🏗️ Meta RC Pulse — 17工程積算エンジン")
st.caption("住所情報を入力すると自動で積算・収益シミュレーションを行います")

with st.form("input_form"):
    st.subheader("📍 敷地情報")
    col1, col2 = st.columns(2)
    with col1:
        site_area = st.number_input("敷地面積（m²）", value=100.0)
        site_width = st.number_input("間口（m）", value=10.0)
        site_depth = st.number_input("奥行（m）", value=10.0)
        road_width = st.number_input("前面道路幅（m）", value=4.0)
    with col2:
        coverage_ratio = st.number_input("建蔽率（%）", value=60.0)
        far = st.number_input("容積率（%）", value=200.0)
        market_studio = st.number_input("スタジオ相場（円/h）", value=3000)
        market_room = st.number_input("ワンルーム相場（円/月）", value=70000)

    st.subheader("💰 融資情報")
    col3, col4 = st.columns(2)
    with col3:
        loan_amount = st.number_input("借入額（万円）", value=50000) * 10000
        loan_rate = st.number_input("金利（%）", value=1.5) / 100
    with col4:
        loan_years = st.number_input("返済年数", value=30)

    submitted = st.form_submit_button("⚡ 積算実行", use_container_width=True)

if submitted:
    r = run_17steps(
        site_area, site_width, site_depth,
        coverage_ratio, far, road_width,
        market_studio, market_room,
        loan_amount, loan_rate, loan_years
    )

    st.success("✅ 積算完了")

    st.subheader("🏢 建物概要")
    col1, col2, col3 = st.columns(3)
    col1.metric("住戸数", f"{r['unit_count']}戸")
    col2.metric("スタジオ料金", f"¥{r['studio_rate']:,}/h")
    col3.metric("賃料設定", f"¥{r['room_rent']:,}/月")

    st.subheader("💴 建築費概算")
    st.metric("総事業費", f"¥{r['total_cost']:,}")

    st.subheader("📈 月間収益")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("スタジオ収益", f"¥{r['studio_monthly']:,}")
    col2.metric("賃料収益", f"¥{r['room_monthly']:,}")
    col3.metric("デリバリー", f"¥{r['delivery_owner']:,}")
    col4.metric("自販機", f"¥{r['vending_owner']:,}")

    st.subheader("🏆 オーナー収益")
    col1, col2, col3 = st.columns(3)
    col1.metric("月間手取り合計", f"¥{r['owner_total']:,}")
    col2.metric("ローン返済", f"¥{r['loan_monthly']:,}")
    col3.metric("純利益（月）", f"¥{r['net_monthly']:,}")

    st.subheader("📊 利回り")
    col1, col2 = st.columns(2)
    col1.metric("表面利回り", f"{r['gross_yield']}%")
    col2.metric("実質利回り", f"{r['net_yield']}%")
