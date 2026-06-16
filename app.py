

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

def load_data_from_sheet(sheet_name):
    SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'
    encoded_sheet = urllib.parse.quote(sheet_name)
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

st.sidebar.title("🏢 لوحة تحكم شركة قصر الهناء")
page = st.sidebar.radio("انتقل إلى:", ["📋 إدارة ومراسلة الحجوزات", "💰 التقارير المالية والإيرادات"])

# ----------------------------------------------------
# 📄 الصفحة الأولى: إدارة ومراسلة الحجوزات
# ----------------------------------------------------
if page == "📋 إدارة ومراسلة الحجوزات":
    st.title("🚌 لوحة تحكم حجوزات قصر الهناء")
    st.subheader("رحلة الجبل الأخضر 2026")
    
    if st.button("🔄 تحديث وسحب الحجوزات الحالية"):
        try:
            st.session_state['df_hajj'] = load_data_from_sheet('Form responses 1')
            st.success("تم تحديث كشف الحجوزات بنجاح!")
        except Exception as e:
            st.error(f"تأكد من إعدادات مشاركة شيت الحجوزات: {e}")

    if 'df_hajj' in st.session_state:
        df = st.session_state['df_hajj']
        
        col_name = next((c for c in df.columns if 'الاسم' in c or 'اسم' in c), None)
        col_phone = next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c or 'موبايل' in c), None)
        col_count = next((c for c in df.columns if 'العدد' in c or 'أفراد' in c or 'اشخاص' in c), None)
        col_hotel = next((c for c in df.columns if 'الإقامة' in c or 'فندق' in c or 'محل' in c), None)
        col_region = next((c for c in df.columns if 'انطلاق' in c or 'مكان' in c or 'تسجيل' in c), None)

        if not col_name or not col_phone:
            st.warning("⚠️ للمراسلة: تأكد من وجود عمود الاسم والهاتف
