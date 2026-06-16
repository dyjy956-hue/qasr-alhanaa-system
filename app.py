

import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# ====================================================
# 🔒 نظام الحماية
# ====================================================
if 'master_password' not in st.session_state:
    st.session_state['master_password'] = "Samir2026"

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def main_system():
    SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

    def load_data_public(sheet_name):
        encoded_sheet = urllib.parse.quote(sheet_name)
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}"
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        
        # تم تصحيح سطر البحث عن الاسم هنا
        col_name = next((c for c in data.columns if 'الاسم' in c or 'اسم' in c), None)
        
        if col_name and sheet_name == 'Form responses 1':
            data = data.sort_values(by=col_name).reset_index(drop=True)
        return data

    # 🧭 القائمة الجانبية
    st.sidebar.title("🏢 لوحة تحكم قصر الهناء")
    page = st.sidebar.radio("انتقل إلى:", ["💬 مركز مراسلة حالات الزبائن", "🔍 استعلام وبطاقة حجز عميل", "📋 الكشف الكلي", "💰 التقارير المالية"])

    if 'df' not in st.session_state:
        st.session_state['df'] = load_data_public('Form responses 1')
        st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')

    # 💬 مركز المراسلات
    if page == "💬 مركز مراسلة حالات الزبائن":
        st.title("💬 مركز المراسلات الذكي")
        df = st.session_state['df']
        col_name = next((c for c in df.columns if 'اسم' in c), None)
        col_phone = next((c for c in df.columns if 'هاتف' in c or 'رقم' in c), None)
        
        selected = st.selectbox("اختر العميل:", df[col_name].dropna().tolist())
        if selected:
            u = df[df[col_name] == selected].iloc[0]
            p = str(u[col_phone]).replace('.0','').replace('+', '').replace(' ', '')
            msg = f"✨ *شركة قصر الهناء للسياحة* 🌹\n\nأهلاً *{u[col_name]}*، تم تأكيد تسجيلكم للرحلة بنجاح 📊✨"
            url = f"whatsapp://send?phone={p}&text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{url}" target="_blank"><button style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; width: 100%;">🚀 إرسال رسالة من تطبيق واتساب</button></a>', unsafe_allow_html=True)

    # 🔍 استعلام وبطاقة عميل
    elif page == "🔍 استعلام وبطاقة حجز عميل":
        df = st.session_state['df']
        col_name = next((c for c in df.columns if 'اسم' in c), None)
        col_money = next((c for c in df.columns if 'اجمالي التكلفة' in c or 'إجمالي التكلفة' in c), None)
        
        selected = st.selectbox("اختر العميل:", df[col_name].dropna().tolist())
        if selected:
            u = df[df[col_name] == selected].iloc[0]
            cost = u.get(col_money, 'غير مسجل') if col_money else 'غير موجود'
            st.markdown(f"""<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-right: 5px solid #1d3557;"><h3>👤 العميل: {selected}</h3><p><b>💰 إجمالي التكلفة:</b> {cost}</p></div>""", unsafe_allow_html=True)

    elif page == "📋 الكشف الكلي":
        st.dataframe(st.session_state['df'], use_container_width=True)
    
    elif page == "💰 التقارير المالية":
        st.dataframe(st.session_state['df_finance'], use_container_width=True)

# تشغيل النظام
if st.session_state['authenticated']:
    main_system()
else:
    st.title("🔒 نظام تسجيل الدخول")
    pw = st.text_input("كلمة المرور:", type="password")
    if st.button("دخول"):
        if pw == st.session_state['master_password']:
            st.session_state['authenticated'] = True
            st.rerun()
