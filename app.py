

import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

if 'master_password' not in st.session_state:
    st.session_state['master_password'] = "Samir2026"
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🔒 نظام تسجيل الدخول - شركة قصر الهناء")
    user_password = st.text_input("كلمة المرور:", type="password")
    if st.button("🔓 تسجيل الدخول"):
        if user_password == st.session_state['master_password']:
            st.session_state['authenticated'] = True
            st.rerun()
    st.stop()

SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    encoded_sheet = urllib.parse.quote(sheet_name)
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}'
    return pd.read_csv(url)

if 'df' not in st.session_state:
    st.session_state['df'] = load_data_public('Form responses 1')
    st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')

df = st.session_state['df']
st.sidebar.title("🏢 لوحة تحكم شركة قصر الهناء")
page = st.sidebar.radio("انتقل إلى:", ["💬 مركز مراسلة حالات الزبائن", "🔍 استعلام وبطاقة حجز عميل", "📋 الكشف الكلي لجميع الركاب", "💰 التقارير المالية والإيرادات"])

if page == "💬 مركز مراسلة حالات الزبائن":
    st.title("💬 مركز المراسلات")
    col_name = next((c for c in df.columns if 'الاسم' in c), df.columns[0])
    col_phone = next((c for c in df.columns if 'هاتف' in c or 'رقم' in c), df.columns[1])
    
    selected_user = st.selectbox("اختر العميل:", df[col_name].dropna().tolist())
    if selected_user:
        u = df[df[col_name] == selected_user].iloc[0]
        phone_str = str(u[col_phone]).replace('.0', '').replace('+', '').replace(' ', '')
        msg = f"أهلاً أستاذ/ة {selected_user}، تم تأكيد تسجيلكم لرحلة (الجبل الأخضر 2026) بنجاح."
        
        # التعديل هنا: استخدام whatsapp://send بدلاً من wa.me
        url = f"whatsapp://send?phone={phone_str}&text={urllib.parse.quote(msg)}"
        
        st.markdown(f'<a href="{url}" target="_blank"><button style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; border:none; width: 100%; font-weight:bold;">🚀 إرسال عبر تطبيق واتساب</button></a>', unsafe_allow_html=True)

elif page == "🔍 استعلام وبطاقة حجز عميل":
    st.dataframe(df, use_container_width=True)

elif page == "📋 الكشف الكلي لجميع الركاب":
    st.dataframe(df, use_container_width=True)

elif page == "💰 التقارير المالية والإيرادات":
    st.dataframe(st.session_state['df_finance'], use_container_width=True)
