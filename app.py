import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import date
import db

db.init_db()
st.set_page_config(page_title="记账本", page_icon="💰")
st.title("💰 我的记账本")

CATS = ["餐饮","交通","购物","居住","娱乐","医疗","其他"]
tab1, tab2, tab3 = st.tabs(["记一笔","明细","统计"])

# --- 记一笔 ---
with tab1:
    with st.form("add", clear_on_submit=True):
        d = st.date_input("日期", date.today())
        amount = st.number_input("金额", min_value=0.01, step=1.0)
        cat = st.selectbox("分类", CATS)
        note = st.text_input("备注")
        if st.form_submit_button("保存"):
            db.add_record(str(d), amount, cat, note)
            st.success(f"已记录 {amount} 元 · {cat}")

# --- 明细 ---
with tab2:
    month = st.text_input("月份", date.today().strftime("%Y-%m"), help="格式 2026-11")
    rows = db.list_records(month=month)
    if rows:
        df = pd.DataFrame([dict(r) for r in rows])
        st.dataframe(df[["date","amount","category","note"]], use_container_width=True)
        del_id = st.selectbox("选择要删除的ID", df["id"])
        if st.button("删除该记录"):
            db.delete_record(int(del_id)); st.rerun()
    else:
        st.info("本月还没有记录")

# --- 统计 ---
with tab3:
    month = st.text_input("统计月份", date.today().strftime("%Y-%m"), key="m2")
    st.metric("本月总支出", f"{db.month_total(month):.2f} 元")
    cs = db.category_sum(month)
    if cs:
        df = pd.DataFrame([dict(r) for r in cs])
        fig = px.pie(df, names="category", values="s", title="分类占比")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无数据")