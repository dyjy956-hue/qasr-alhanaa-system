

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# ====================================================
# 🔒 تأمين وإقلاع نظام الحماية (مصحح لتفادي KeyError)
# ====================================================
if 'master_password' not in st.session_state:
    st.session_state['master_password'] = "Samir2026"

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# ====================================================
# 🚌 متن المنظومة الأصلية بالكامل
# ====================================================
def main_system():
    SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

    def load_data_public(sheet_name):
        encoded_sheet = urllib.parse.quote(sheet_name)
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}"
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        
        col_name = next((c for c in data.columns if 'الاسم' in c or 'اسم' in c), None)
        if col_name and sheet_name == 'Form responses 1':
            data = data.sort_values(by=col_name).reset_index(drop=True)
        return data

    def convert_df_to_excel(df_to_export):
        valid_keys = ['الاسم', 'الهاتف', 'رقم', 'العدد', 'أفراد', 'الإقامة', 'فندق', 'انطلاق', 'مكان', 'تكلفة', 'مبلغ', 'قيمة', 'دفع', 'سداد']
        keep_cols = [c for c in df_to_export.columns if any(k in c for k in valid_keys)]
        if not keep_cols:
            keep_cols = df_to_export.columns[:5]
        
        df_clean = df_to_export[keep_cols].copy()
        df_clean.insert(0, '#', range(1, len(df_clean) + 1))
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_clean.to_excel(writer, index=False, sheet_name='الكشف الرسمي')
        return output.getvalue()

    def display_styled_dataframe(dataframe):
        df_display = dataframe.copy()
        df_display.insert(0, '#', range(1, len(df_display) + 1))
        st.dataframe(df_display.set_index('#'), use_container_width=True)

    # 🧭 القائمة الجان
