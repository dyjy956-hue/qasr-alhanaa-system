

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

if not st.session_state['authenticated']:
    st.title("🔒 نظام تسجيل الدخول - شركة قصر الهناء")
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3064/3064155.png", width=150)
    with col2:
        user_password = st.text_input("الرجاء إدخال كلمة مرور المنظومة:", type="password")
        if st.button("🔓 تسجيل الدخول"):
            if user_password == st.session_state['master_password']:
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("❌ كلمة المرور غير صحيحة.")
    st.stop()

# ====================================================
# دوال المنظومة
# ====================================================
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    encoded_sheet = urllib.parse.quote(sheet_name)
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

def get_wa_link(phone, text):
    # دالة ذكية لتشفير الرسائل لضمان التنسيق في الواتساب
    return f"https://wa.me/{phone}?text={urllib.parse.quote(text)}"

def convert_df_to_excel(df_to_export):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_to_export.to_excel(writer, index=False)
    return output.getvalue()

def display_styled_dataframe(dataframe):
    df_display = dataframe.copy()
    df_display.insert(0, '#', range(1, len(df_display) + 1))
    st.dataframe(df_display.set_index('#'), use_container_width=True)

# ====================================================
# الواجهة الجانبية
# ====================================================
st.sidebar.title("🏢 لوحة تحكم قصر الهناء")
page = st.sidebar.radio("انتقل إلى القائمة:", [
    "💬 مركز مراسلة حالات الزبائن", "🔍 استعلام وبطاقة حجز عميل",
    "📋 الكشف الكلي للركاب", "🏢 كشف نزلاء فندق قورينا",
    "🌲 كشف نزلاء منتجع شحات", "🟢 كشف ركاب طرابلس والغرب", 
    "🔵 كشف ركاب المنطقة الشرقية", "💰 التقارير المالية"
])

if st.sidebar.button("🔄 تحديث البيانات الشاملة"):
    st.session_state['df'] = load_data_public('Form responses 1')
    st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
    st.rerun()

if 'df' not in st.session_state: st.session_state['df'] = load_data_public('Form responses 1')
if 'df_finance' not in st.session_state: st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')

# ====================================================
# الصفحات
# ====================================================
if page == "💬 مركز مراسلة حالات الزبائن":
    st.title("💬 مركز المراسلات الذكي")
    df = st.session_state['df']
    col_name = next((c for c in df.columns if 'الاسم' in c), None)
    col_phone = next((c for c in df.columns if 'الهاتف' in c), None)
    
    if col_name and col_phone:
        selected_user = st.selectbox("اختر اسم الزبون:", df[col_name].dropna().tolist())
        user_data = df[df[col_name] == selected_user].iloc[0]
        
        # تنسيق الرسائل (استخدام \n للأسطر و * للخط العريض)
        msg_confirm = f"السلام عليكم،\n\nمرحباً بك *{user_data[col_name]}* 🌹\nتم استلام بيانات تسجيلكم بنجاح 📊✨\n\nشكراً لثقتكم بقصر الهناء! 🏔️"
        
        st.write("### 📲 خيارات المراسلة:")
        url = get_wa_link(str(user_data[col_phone]), msg_confirm)
        st.markdown(f'<a href="{url}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 10px; border-radius: 5px;">ارسال رسالة واتساب</button></a>', unsafe_allow_html=True)

elif page == "🔍 استعلام وبطاقة حجز عميل":
    st.title("🔍 نظام الاستعلام الف
