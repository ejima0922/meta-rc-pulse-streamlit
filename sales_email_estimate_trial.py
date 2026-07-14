import datetime
import math
import re
from zoneinfo import ZoneInfo

import streamlit as st

st.set_page_config(
    page_title="Meta-RC Pulse 営業メール下書き・試算システム",
    layout="wide",
)

st.markdown(
    """
<style>
html, body, [class*="css"] {
    font-size: 14px !important;
    font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", sans-serif;
}
.important-value {
    font-size: 24px !important;
    font-weight: bold;
    color: #FF4B4B;
    margin: 5px 0;
}
.warning-text {
    color: #FF4B4B;
    font-weight: bold;
    border: 1px solid #FF4B4B;
    padding: 10px;
    border-radius: 5px;
    background-color: #FFF0F0;
    margin: 10px 0;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("Meta-RC Pulse 営業メール下書き・試算システム")
st.write("スマートフォン対応UI。入力条件に基づき、営業メールの下書き生成と事業試算を行います。")

st.subheader("📋 基本情報の入力")
company_name = st.text_input("元付け不動産会社名", value="")
contact_name = st.text_input("ご担当者名", value="")
property_name = st.text_input("対象物件名", value="")
email_address = st.text_input("送信先メールアドレス", value="")

st.subheader("📐 地上階：敷地・建物プラン（上限チェック用）")
col_land1, col_land2 = st.columns(2)
with col_land1:
    site_area = st.number_input("敷地面積（㎡）", min_value=1.0, value=1206.0, step=10.0)
    floor_area_ratio = st.number_input("容積率（％）", min_value=10.0, value=800.0, step=10.0)
    ratio_of_common_area = st.number_input("共用部率（％）", min_value=0.0, max_value=90.0, value=20.0, step=1.0)
with col_land2:
    total_floor_area_for_far = site_area * (floor_area_ratio / 100.0)
    st.write(f"想定容積対象延床面積（自動）： **{total_floor_area_for_far:,.2f} ㎡**")
    average_private_area = st.number_input("平均専有面積（㎡/室）", min_value=1.0, value=18.0, step=0.5)

allowable_units = int(
    total_floor_area_for_far
    * (1.0 - ratio_of_common_area / 100.0)
    / average_private_area
)

st.subheader("📐 地下階：敷地・建物プラン（上限チェック用）")
st.write("地下室数は面積式による一次試算です。正式な室数は構造、避難経路、設備、防音仕様、有資格者確認後に確定します。")
col_under_land1, col_under_land2 = st.columns(2)
with col_under_land1:
    underground_floors = st.number_input("地下階数（階）", min_value=1, value=4, step=1)
    underground_floor_area = st.number_input("地下1フロアあたり想定床面積（㎡）", min_value=1.0, value=1206.0, step=10.0)
with col_under_land2:
    underground_common_ratio = st.number_input("地下共用部・設備部率（％）", min_value=0.0, max_value=90.0, value=30.0, step=1.0)
    underground_room_average_area = st.number_input("地下ラボ1室あたり平均面積（㎡/室）", min_value=1.0, value=18.5, step=0.5)

allowable_underground_units = int(
    underground_floors
    * underground_floor_area
    * (1.0 - underground_common_ratio / 100.0)
    / underground_room_average_area
)

st.subheader("💰 資金計画・ローン計算（単位：億円）")
col_param1, col_param2, col_param3 = st.columns(3)
with col_param1:
    total_project_cost_okurui = st.number_input("総事業費（億円）", min_value=0.01, value=190.0, step=1.0)
with col_param2:
    loan_amount_okurui = st.number_input("借入金（億円）", min_value=0.0, value=128.0, step=1.0)
with col_param3:
    annual_interest_rate = st.number_input("ローン年利（％）", min_value=0.0, value=2.0, step=0.1, format="%.2f")

total_project_cost = total_project_cost_okurui * 100_000_000.0
loan_amount = loan_amount_okurui * 100_000_000.0
equity_amount_okurui = total_project_cost_okurui - loan_amount_okurui

st.subheader("🏢 地上住戸プラン＆経費率設定")
col_rev1, col_exp1 = st.columns(2)
with col_rev1:
    above_ground_units = st.number_input("地上階 部屋数（室）※初期値はデモ用数です", min_value=0, value=420, step=10)
    above_ground_rent = st.number_input("地上階 1室あたり月額想定賃料（円）", min_value=0, value=180000, step=1000)
with col_exp1:
    vacant_rate = st.number_input("地上：想定空室率（％）", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
    management_fee_rate = st.number_input("地上：管理費率（％）", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
    maintenance_fee_rate = st.number_input("地上：修繕費率（％）", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
    tax_utility_rate = st.number_input("地上：固定資産税・保険・共用光熱費率（％）", min_value=0.0, max_value=100.0, value=5.0, step=0.5)

total_above_expense_rate = management_fee_rate + maintenance_fee_rate + tax_utility_rate

st.subheader("🎵 地下ラボプラン＆経費率設定（1予約50分固定枠）")
col_rev2, col_exp2 = st.columns(2)
with col_rev2:
    underground_units = st.number_input("地下階 部屋数（室）", min_value=0, value=144, step=10)
    underground_slot_price = st.number_input("地下：1予約枠あたり料金（円）", min_value=0, value=3000, step=100)
    st.write("**枠運用ベース時間計算（自動）**")
    slot_cycle_minutes = st.number_input("1枠の運用周期（分：50分利用＋入替時間）", min_value=50, value=60, step=5)
    hours_per_day = st.number_input("1日営業可能時間（時間）", min_value=1, max_value=24, value=24, step=1)
    days_per_month = st.number_input("月間基準日数（日）", min_value=1, max_value=31, value=30, step=1)
    underground_occupancy_rate = st.number_input("想定稼働率（％）", min_value=0.0, max_value=100.0, value=70.0, step=1.0)

    slots_per_day = math.floor(hours_per_day * 60 / slot_cycle_minutes)
    slots_per_month_possible = slots_per_day * days_per_month
    slots_per_month_actual = slots_per_month_possible * (underground_occupancy_rate / 100.0)

    st.write(f"1日利用可能枠数： **{slots_per_day} 枠**")
    st.write(f"月間予約可能枠数： **{slots_per_month_possible} 枠**")
    st.write(f"想定月間予約枠数： **{slots_per_month_actual:.1f} 枠**")
with col_exp2:
    under_cleaning_rate = 20.0
    under_maintenance_rate = 10.0
    under_operation_rate = 20.0
    total_under_expense_rate = under_cleaning_rate + under_maintenance_rate + under_operation_rate
    st.write("**地下：標準経費率（固定仕様）**")
    st.write(f"・清掃費率：{under_cleaning_rate:.0f} ％")
    st.write(f"・修繕費率：{under_maintenance_rate:.0f} ％")
    st.write(f"・運営費率：{under_operation_rate:.0f} ％")
    st.write(f"・**地下経費率合計：{total_under_expense_rate:.0f} ％**")

st.subheader("🪙 その他雑収入設定")
col_extra1, col_extra2 = st.columns(2)
with col_extra1:
    extra_annual_income_manrui = st.number_input("その他想定雑収入（年間・万円）", min_value=0.0, value=2400.0, step=100.0)
    extra_annual_income = extra_annual_income_manrui * 10_000.0
with col_extra2:
    extra_expense_rate = st.number_input("その他雑収入の経費率（％）", min_value=0.0, max_value=100.0, value=50.0, step=1.0)

is_above_limit_exceeded = above_ground_units > allowable_units
is_under_limit_exceeded = underground_units > allowable_underground_units
is_equity_negative = equity_amount_okurui < 0.0
is_above_expense_invalid = total_above_expense_rate >= 100.0
is_under_expense_invalid = total_under_expense_rate >= 100.0

if is_above_limit_exceeded:
    st.markdown(f"<div class='warning-text'>⚠️ 地上室数が概算上限（{allowable_units}室）を超えています。</div>", unsafe_allow_html=True)
if is_under_limit_exceeded:
    st.markdown(f"<div class='warning-text'>⚠️ 地下室数が概算上限（{allowable_underground_units}室）を超えています。</div>", unsafe_allow_html=True)
if is_equity_negative:
    st.markdown("<div class='warning-text'>⚠️ 借入金額が総事業費を超えています。</div>", unsafe_allow_html=True)
if is_above_expense_invalid:
    st.markdown("<div class='warning-text'>⚠️ 地上経費率の合計が100％以上です。</div>", unsafe_allow_html=True)
if is_under_expense_invalid:
    st.markdown("<div class='warning-text'>⚠️ 地下経費率の合計が100％以上です。</div>", unsafe_allow_html=True)

above_ground_full_gross = above_ground_units * above_ground_rent * 12
above_ground_vacant_loss = above_ground_full_gross * (vacant_rate / 100.0)
above_ground_effective_gross = above_ground_full_gross - above_ground_vacant_loss
above_management_cost = above_ground_effective_gross * (management_fee_rate / 100.0)
above_maintenance_cost = above_ground_effective_gross * (maintenance_fee_rate / 100.0)
above_tax_utility_cost = above_ground_effective_gross * (tax_utility_rate / 100.0)
above_ground_noi = above_ground_effective_gross - (
    above_management_cost + above_maintenance_cost + above_tax_utility_cost
)

annual_underground_capacity_gross = (
    underground_units * underground_slot_price * slots_per_month_possible * 12
)
annual_underground_gross = (
    underground_units * underground_slot_price * slots_per_month_actual * 12
)
underground_occupancy_loss = annual_underground_capacity_gross - annual_underground_gross
underground_noi = annual_underground_gross * (1.0 - total_under_expense_rate / 100.0)

extra_noi = extra_annual_income * (1.0 - extra_expense_rate / 100.0)

potential_gross_income = (
    above_ground_full_gross + annual_underground_capacity_gross + extra_annual_income
)
total_effective_income = (
    above_ground_effective_gross + annual_underground_gross + extra_annual_income
)
total_operating_expenses = (
    above_management_cost
    + above_maintenance_cost
    + above_tax_utility_cost
    + (annual_underground_gross - underground_noi)
    + (extra_annual_income - extra_noi)
)
noi = above_ground_noi + underground_noi + extra_noi
calculated_noi_from_totals = total_effective_income - total_operating_expenses
is_calculation_consistent = math.isclose(
    noi,
    calculated_noi_from_totals,
    rel_tol=1e-9,
    abs_tol=1.0,
)

loan_term_years = 45
total_payments = loan_term_years * 12
monthly_interest_rate = annual_interest_rate / 100.0 / 12
if loan_amount > 0 and monthly_interest_rate > 0:
    factor = (1 + monthly_interest_rate) ** total_payments
    monthly_loan_payment = loan_amount * monthly_interest_rate * factor / (factor - 1)
elif loan_amount > 0:
    monthly_loan_payment = loan_amount / total_payments
else:
    monthly_loan_payment = 0.0
annual_loan_payment = monthly_loan_payment * 12
annual_cash_flow = noi - annual_loan_payment
monthly_cash_flow = annual_cash_flow / 12
net_yield_percent = noi / total_project_cost * 100
cash_flow_yield_percent = annual_cash_flow / total_project_cost * 100
is_cash_flow_negative = annual_cash_flow < 0.0

if not is_calculation_consistent:
    st.markdown("<div class='warning-text'>⚠️ 内部計算の整合性エラーを検出しました。メール下書きには使用できません。</div>", unsafe_allow_html=True)
if is_cash_flow_negative:
    st.markdown("<div class='warning-text'>⚠️ 返済後キャッシュフローがマイナスです。</div>", unsafe_allow_html=True)

st.subheader("📊 試算結果（条件連動）")
col_res1, col_res2, col_res3 = st.columns(3)
with col_res1:
    st.write("■ 年間潜在総収入")
    st.markdown(f"<p class='important-value'>{potential_gross_income:,.0f} 円</p>", unsafe_allow_html=True)
    st.write("■ 地上空室損失")
    st.markdown(f"<p class='important-value'>{above_ground_vacant_loss:,.0f} 円</p>", unsafe_allow_html=True)
    st.write("■ 地下未稼働損失")
    st.markdown(f"<p class='important-value'>{underground_occupancy_loss:,.0f} 円</p>", unsafe_allow_html=True)
    st.write("■ 年間実効総収入")
    st.markdown(f"<p class='important-value'>{total_effective_income:,.0f} 円</p>", unsafe_allow_html=True)
with col_res2:
    st.write("■ 年間運営費合計")
    st.markdown(f"<p class='important-value'>{total_operating_expenses:,.0f} 円</p>", unsafe_allow_html=True)
    st.write("■ NOI（営業純収益）")
    st.markdown(f"<p class='important-value'>{noi:,.0f} 円</p>", unsafe_allow_html=True)
    st.write("■ 地上住戸NOI")
    st.markdown(f"<p class='important-value'>{above_ground_noi:,.0f} 円</p>", unsafe_allow_html=True)
with col_res3:
    st.write("■ 地下ラボNOI（清掃・修繕・運営控除後）")
    st.markdown(f"<p class='important-value'>{underground_noi:,.0f} 円</p>", unsafe_allow_html=True)
    st.write("■ 年間ローン返済額（45年）")
    st.markdown(f"<p class='important-value'>{annual_loan_payment:,.0f} 円</p>", unsafe_allow_html=True)
    st.write("■ 返済後月々キャッシュフロー（税引前試算）")
    st.markdown(f"<p class='important-value'>{monthly_cash_flow:,.0f} 円</p>", unsafe_allow_html=True)

col_res4, col_res5, col_res6 = st.columns(3)
with col_res4:
    st.metric("NET利回り", f"{net_yield_percent:.2f} ％")
with col_res5:
    st.metric("返済後キャッシュフロー率", f"{cash_flow_yield_percent:.2f} ％")
with col_res6:
    st.metric("自己資金想定額", f"{equity_amount_okurui:.2f} 億円")

current_params = {
    "company_name": company_name,
    "contact_name": contact_name,
    "property_name": property_name,
    "email_address": email_address,
    "site_area": site_area,
    "floor_area_ratio": floor_area_ratio,
    "ratio_of_common_area": ratio_of_common_area,
    "average_private_area": average_private_area,
    "underground_floors": underground_floors,
    "underground_floor_area": underground_floor_area,
    "underground_common_ratio": underground_common_ratio,
    "underground_room_average_area": underground_room_average_area,
    "total_project_cost_okurui": total_project_cost_okurui,
    "loan_amount_okurui": loan_amount_okurui,
    "annual_interest_rate": annual_interest_rate,
    "above_ground_units": above_ground_units,
    "above_ground_rent": above_ground_rent,
    "vacant_rate": vacant_rate,
    "management_fee_rate": management_fee_rate,
    "maintenance_fee_rate": maintenance_fee_rate,
    "tax_utility_rate": tax_utility_rate,
    "underground_units": underground_units,
    "underground_slot_price": underground_slot_price,
    "slot_cycle_minutes": slot_cycle_minutes,
    "hours_per_day": hours_per_day,
    "days_per_month": days_per_month,
    "underground_occupancy_rate": underground_occupancy_rate,
    "under_cleaning_rate": under_cleaning_rate,
    "under_maintenance_rate": under_maintenance_rate,
    "under_operation_rate": under_operation_rate,
    "extra_annual_income_manrui": extra_annual_income_manrui,
    "extra_expense_rate": extra_expense_rate,
}

if "generated_parameters" not in st.session_state:
    st.session_state.generated_parameters = None

is_parameter_changed = (
    st.session_state.generated_parameters is not None
    and st.session_state.generated_parameters != current_params
)

st.markdown("---")
st.subheader("📋 メール下書き生成前の必須確認事項")
check_1 = st.checkbox("対象物件が実際に売り出されていることを確認済みである。")
check_2 = st.checkbox("送信先が元付け不動産会社であることを確認済みである。")
check_3 = st.checkbox("入力した想定賃料および時間貸し収益条件の算出根拠を確認済みである。")
check_4 = st.checkbox("この計画は現段階の事業構想案であり、建築の可否は法規調査や行政協議、有資格者の確認後に確定することを理解している。")

email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
is_email_valid = bool(re.fullmatch(email_pattern, email_address.strip()))
is_base_info_filled = bool(
    company_name.strip()
    and contact_name.strip()
    and property_name.strip()
    and email_address.strip()
)
all_checked = check_1 and check_2 and check_3 and check_4

is_generation_disabled = (
    not all_checked
    or is_above_limit_exceeded
    or is_under_limit_exceeded
    or is_equity_negative
    or is_above_expense_invalid
    or is_under_expense_invalid
    or is_cash_flow_negative
    or not is_calculation_consistent
    or not is_email_valid
    or not is_base_info_filled
)

st.subheader("✉️ メール生成")
if st.button("提案メール下書きを生成", disabled=is_generation_disabled):
    subject = f"【事業構想打診】{property_name}に関するお伺い"
    body = f"""{company_name}
ご担当者 {contact_name} 様

いつも大変お世話になっております。
Meta-RC 独自の解析エンジンを用いた資産開発を行っております、江島 利之と申します。

貴社が売り出しを担当されております「{property_name}」につきまして、現在、建て替えを前提とした再開発スキームを検討しております。

本計画は、地主様、投資会社様、および建設会社様の全員が『三方よしの笑顔』で握手できる計画を目指しております。

【新築時想定収益シミュレーション（税引前試算）】
■ 対象物件名：{property_name}
■ 総事業費：{total_project_cost_okurui:.2f} 億円
■ 借入金額：{loan_amount_okurui:.2f} 億円
■ 自己資金想定額：{equity_amount_okurui:.2f} 億円
■ ローン年利：{annual_interest_rate:.2f} ％
■ 返済期間：45年（元利均等返済）
※地下ラボは50分固定予約による試算です。

■ 年間潜在総収入：約 {potential_gross_income:,.0f} 円
■ 地上空室損失：約 {above_ground_vacant_loss:,.0f} 円
■ 地下未稼働損失：約 {underground_occupancy_loss:,.0f} 円
■ 年間実効総収入：約 {total_effective_income:,.0f} 円
■ 年間運営費合計：約 {total_operating_expenses:,.0f} 円
■ NOI（営業純収益）：約 {noi:,.0f} 円
■ 年間ローン返済額：約 {annual_loan_payment:,.0f} 円
■ 返済後年間キャッシュフロー：約 {annual_cash_flow:,.0f} 円
■ 返済後月々キャッシュフロー（税引前試算）：約 {monthly_cash_flow:,.0f} 円／月
■ NET利回り：{net_yield_percent:.2f} ％
■ 返済後キャッシュフロー率：{cash_flow_yield_percent:.2f} ％

※本数値は、入力条件に基づく現段階の事業構想試算値です。
※実際の建築可能性は、法規調査、行政協議、有資格者による確認を経て確定します。

まずは、既存建物の詳細な図面や仕様など、開示可能な範囲で情報共有をいただくことは可能でしょうか。

何卒よろしくお願い申し上げます。

──────────────────────
江島 利之
Meta-RC 独自の解析エンジン・開発チーム
──────────────────────"""
    st.session_state.generated_parameters = current_params.copy()
    st.session_state.edit_subject = subject
    st.session_state.edit_body = body
    st.success("下書きの生成に成功しました。")

if st.session_state.generated_parameters is not None:
    if is_parameter_changed:
        st.warning("⚠️ 入力条件が変更されました。メール下書きを再生成してください。")
    else:
        st.markdown("---")
        st.subheader("✉️ 生成メール下書きプレビュー")
        edit_subject_val = st.text_input("件名（調整可能）", key="edit_subject")
        edit_body_val = st.text_area("本文（調整可能）", key="edit_body", height=400)
        is_edited_mail_valid = bool(edit_subject_val.strip() and edit_body_val.strip())
        if not is_edited_mail_valid:
            st.info("件名と本文を入力してください。")

        confirm_send = st.checkbox("送信シミュレーションの内容を確認しました。")
        is_sim_disabled = (
            not all_checked
            or not is_base_info_filled
            or not is_email_valid
            or is_above_limit_exceeded
            or is_under_limit_exceeded
            or is_equity_negative
            or is_above_expense_invalid
            or is_under_expense_invalid
            or is_cash_flow_negative
            or not is_calculation_consistent
            or is_parameter_changed
            or not is_edited_mail_valid
            or not confirm_send
        )

        if st.button("送信シミュレーションを実行", disabled=is_sim_disabled):
            now_jst = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
            st.markdown("### 📢 送信シミュレーション結果")
            st.warning("外部には送信されていません。")
            log_text = f"""[SIMULATION_RESULT]
シミュレーション実行日時（JST）: {now_jst.strftime('%Y-%m-%d %H:%M:%S')}

【送信先候補】
{company_name}
{contact_name} 様
{email_address}

対象物件名: {property_name}
最終編集後の件名: {edit_subject_val}

※このアプリのコード上では、外部送信およびアプリ内データベースへの永続保存処理を実行していません。"""
            st.code(log_text, language=None)
