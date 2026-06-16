

import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# ====================================================
# 🔒 الحماية
# ====================================================
if 'master_password' not in st.session_state: st.session_state['master_password'] = "Samir2026"
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False

def load_full_data():
    # هذا الرابط يسحب الشيت الأساسي
    sheet_id = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'
    # سحب ورقة "Form responses 1"
    url1 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Form%20responses%201"
    # سحب ورقة "التقرير المالي"
    url2 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=%F0%9F%93%8A%20%D8%A7%D9%84%D8%AA%D9%82%D8%B1%D9%8A%D8%B1%20%D8%A7%D9%84%D9%85%D8%A7%D9%84%D9%8A%20%D9%88%D8%A7%D9%84%D8%A5%D9%8A%D8%B1%D8%A7%D8%AF%D8%A7%D8%AA"
    
    df = pd.read_csv(url1)
    df_fin = pd.read_csv(url2)
    return df, df_fin

if not st.session_state['authenticated']:
    st.title("🔒 تسجيل دخول منظومة قصر الهناء")
    pw = st.text_input("كلمة المرور:", type="password")
    if st.button("دخول"):
        if pw == st.session_state['master_password']:
            st.session_state['authenticated'] = True
            st.rerun()
    st.stop()

# المنظومة
st.sidebar.title("🏢 لوحة التحكم")
page = st.sidebar.radio("اختر القسم:", ["💬 المراسلات", "🔍 استعلام", "📋 الكشف الكلي", "💰 المالية"])

if 'df' not in st.session_state:
    st.session_state['df'], st.session_state['df_finance'] = load_full_data()

df = st.session_state['df']

if page == "💬 المراسلات":
    st.title("💬 مركز المراسلات")
    name_col = df.columns[0] # العمود الأول
    phone_col = df.columns[1] # العمود الثاني
    selected = st.selectbox("اختر العميل:", df[name_col].dropna().tolist())
    if selected:
        row = df[df[name_col] == selected].iloc[0]
        phone = str(row[phone_col]).replace('.0', '').replace('+', '').replace(' ', '')
        msg = f"أهلاً أستاذ {selected}، تم تأكيد حجزكم مع شركة قصر الهناء."
        url = f"whatsapp://send?phone={phone}&text={urllib.parse.quote(msg)}"
        st.markdown(f'<a href="{url}" style="text-decoration:none;"><button style="background-color:#25D366; color:white; padding:15px; border-radius:10px; width:100%; border:none;">🚀 إرسال عبر واتساب</button></a>', unsafe_allow_html=True)

elif page == "🔍 استعلام":
    st.dataframe(df, use_container_width=True)

elif page == "📋 الكشف الكلي":
    st.dataframe(df, use_container_width=True)

elif page == "💰 المالية":
    st.dataframe(st.session_state['df_finance'], use_container_width=True)
