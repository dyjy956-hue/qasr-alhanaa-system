

# تعليق لحماية السطر الأول من المسافات التلقائية
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
    if st.button("🔓 تسجيل الدخول"):
        if user_password == st.session_state['master_password']:
            st.session_state['authenticated'] = True
            st.rerun()
    st.stop()

# ====================================================
# دوال المنظومة
# ====================================================
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}'
    return pd.read_csv(url).rename(columns=lambda x: x.strip())

# دالة تنظيف الرقم الليبي وفتح التطبيق
def get_wa_intent(phone, text):
    raw_p = str(phone).replace('.0','').replace(' ','').replace('+','').replace('-','')
    if len(raw_p) == 9 and raw_p.startswith('9'): clean_p = "218" + raw_p
    elif len(raw_p) == 10 and raw_p.startswith('09'): clean_p = "218" + raw_p[1:]
    else: clean_p = raw_p
    return f"intent://send?phone={clean_p}&text={urllib.parse.quote(text)}#Intent;scheme=smsto;package=com.whatsapp;action=android.intent.action.SENDTO;end"

# ====================================================
# الصفحة الأولى: مركز المراسلات
# ====================================================
if 'df' not in st.session_state: st.session_state['df'] = load_data_public('Form responses 1')
df = st.session_state['df']

# (صفحات الكشوفات كما هي في كودك...)

# 🔍 الصفحة الثانية: بطاقة العميل مع التكلفة
# (استخدم هذا الجزء لضمان عرض التكلفة)
col_name = next((c for c in df.columns if 'الاسم' in c), None)
col_cost = next((c for c in df.columns if 'تكلفة' in c or 'مبلغ' in c or 'سعر' in c), None)

if col_name:
    search_user = st.selectbox("🎯 اختر العميل:", ["-- اختر --"] + df[col_name].dropna().tolist())
    if search_user != "-- اختر --":
        u_data = df[df[col_name] == search_user].iloc[0]
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border-right: 5px solid #1d3557;">
            <h3>🎫 بطاقة بيانات الحجز</h3>
            <p><b>👤 الاسم:</b> {u_data.get(col_name)}</p>
            <div style="background-color: #fff3cd; padding: 10px; border-radius: 5px;">
                <p style="font-size: 18px; color: #856404;"><b>💰 إجمالي التكلفة: {u_data.get(col_cost, 'غير محدد')}</b></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
