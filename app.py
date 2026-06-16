

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
    user_password = st.text_input("كلمة المرور:", type="password")
    if st.button("دخول"):
        if user_password == st.session_state['master_password']:
            st.session_state['authenticated'] = True
            st.rerun()
    st.stop()

# ====================================================
# ⚙️ وظائف البيانات
# ====================================================
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    encoded_sheet = urllib.parse.quote(sheet_name)
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

# ====================================================
# 🛠️ تهيئة البيانات
# ====================================================
if 'df' not in st.session_state:
    try:
        st.session_state['df'] = load_data_public('Form responses 1')
        st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
        # تنظيف الأسماء للربط
        st.session_state['df'][st.session_state['df'].columns[0]] = st.session_state['df'].iloc[:, 0].astype(str).str.strip()
        st.session_state['df_finance'][st.session_state['df_finance'].columns[0]] = st.session_state['df_finance'].iloc[:, 0].astype(str).str.strip()
    except: pass

# ====================================================
# 🧭 القائمة الجانبية
# ====================================================
page = st.sidebar.radio("القائمة:", ["🔍 استعلام وبطاقة حجز عميل", "📋 الكشف الكلي", "💰 التقارير المالية"])

# ====================================================
# 🔍 الصفحة الثانية: الاستعلام مع إجمالي التكلفة
# ====================================================
if page == "🔍 استعلام وبطاقة حجز عميل":
    st.title("🔍 استعلام وبطاقة حجز عميل")
    
    if 'df' in st.session_state and 'df_finance' in st.session_state:
        df = st.session_state['df']
        df_finance = st.session_state['df_finance']
        
        col_name = next((c for c in df.columns if 'الاسم' in c), df.columns[0])
        col_cost = next((c for c in df_finance.columns if 'إجمالي' in c and 'تكلفة' in c), df_finance.columns[-1])
        
        search_user = st.selectbox("اختر اسم العميل:", ["-- اختر --"] + df[col_name].tolist())
        
        if search_user != "-- اختر --":
            user_data = df[df[col_name] == search_user].iloc[0]
            # جلب التكلفة بالربط عبر الاسم
            cost_data = df_finance[df_finance.iloc[:, 0] == search_user]
            user_cost = cost_data.iloc[0][col_cost] if not cost_data.empty else "غير متوفر"

            st.markdown(f"""
            <div style="padding: 20px; border: 2px solid #2b5c8f; border-radius: 10px;">
                <h3>🎫 بطاقة الحجز</h3>
                <p><b>👤 الاسم:</b> {user_data[col_name]}</p>
                <p><b>💰 إجمالي التكلفة:</b> {user_cost}</p>
            </div>
            """, unsafe_allow_html=True)

# باقي الصفحات كما كانت في كودك الأصلي...
elif page == "📋 الكشف الكلي":
    st.dataframe(st.session_state['df'])

elif page == "💰 التقارير المالية":
    st.dataframe(st.session_state['df_finance'])
