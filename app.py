

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# ====================================================
# 🔒 نظام الحماية والأمان المطور والمضمون (Samir2026)
# ====================================================
if 'master_password' not in st.session_state:
    st.session_state['master_password'] = "Samir2026"

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# شاشة تسجيل الدخول
if not st.session_state['authenticated']:
    st.title("🔒 نظام تسجيل الدخول - شركة قصر الهناء")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3064/3064155.png", width=150)
    with col2:
        st.write("### مرحباً بك في لوحة تحكم الإدارة")
        user_password = st.text_input("الرجاء إدخال كلمة مرور المنظومة للدخول:", type="password")
        
        if st.button("🔓 تسجيل الدخول"):
            if user_password == st.session_state['master_password']:
                st.session_state['authenticated'] = True
                st.success("✅ تم التحقق بنجاح! اضغط على الزر أدناه للدخول:")
                st.button("🚀 دخول المنظومة الآن")
            else:
                st.error("❌ كلمة المرور غير صحيحة، يرجى إعادة المحاولة.")
    st.stop()

# ====================================================
# 🚌 بداية المنظومة الأصلية
# ====================================================
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    encoded_sheet = urllib.parse.quote(sheet_name)
    url = (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
        f"/gviz/tq?tqx=out:csv&sheet={encoded_sheet}"
    )
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    
    col_name = next((c for c in data.columns if 'الاسم' in c or 'اسم' in c), None)
    if col_name and sheet_name == 'Form responses 1':
        data = data.sort_values(by=col_name).reset_index(drop=True)
    return data

def convert_df_to_excel(df_to_export):
    valid_keys = ['الاسم', 'الهاتف', 'رقم', 'العدد', 'أفراد', 'الإقامة', 'فندق', 'انطلاق', 'مكان', 'مبلغ', 'قيمة', 'دفع', 'سداد']
    keep_cols = [c for c in df_to_export.columns if any(k in c for k in valid_keys)]
    if not keep_cols:
        keep
