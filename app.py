

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
    col1, col2 = st.columns([1, 2])
    with col1: st.image("https://cdn-icons-png.flaticon.com/512/3064/3064155.png", width=150)
    with col2:
        user_password = st.text_input("كلمة المرور:", type="password")
        if st.button("🔓 دخول"):
            if user_password == st.session_state['master_password']:
                st.session_state['authenticated'] = True
                st.rerun()
            else: st.error("❌ كلمة مرور غير صحيحة")
    st.stop()

# ====================================================
# 🚌 المنظومة الأصلية
# ====================================================
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

# تعديل دوال المراسلة لاستخدام whatsapp://send
def get_whatsapp_url(phone, msg):
    # استخدام whatsapp://send يفتح التطبيق مباشرة في الهاتف أو الكمبيوتر
    return f"whatsapp://send?phone={phone}&text={urllib.parse.quote(msg)}"

# التحميل المبدئي
if 'df' not in st.session_state:
    st.session_state['df'] = load_data_public('Form responses 1')
    st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')

df = st.session_state['df']
page = st.sidebar.radio("القائمة:", ["💬 مركز المراسلات", "🔍 استعلام عميل", "📋 الكشف الكلي", "💰 المالية"])

if page == "💬 مركز المراسلات":
    st.title("🚌 مركز المراسلات الذكي")
    col_name = next((c for c in df.columns if 'اسم' in c), None)
    col_phone = next((c for c in df.columns if 'هاتف' in c or 'رقم' in c), None)
    
    selected = st.selectbox("اختر العميل:", df[col_name].dropna().tolist())
    if selected:
        u = df[df[col_name] == selected].iloc[0]
        p = str(u[col_phone]).replace('.0', '').replace('+', '').replace(' ', '')
        
        # رسائل مزخرفة
        msg = f"✨ *شركة قصر الهناء للسياحة* 🌹\n\nأهلاً أستاذ/ة *{selected}*،\nتم استلام تسجيلكم لرحلة (الجبل الأخضر 2026) بنجاح 📊✨\n\n📌 *تفاصيلكم:* \n👥 العدد: {u.get('العدد', 'غير محدد')}\n🏨 الإقامة: {u.get('الإقامة', 'غير محدد')}\n\n💳 *ملاحظة:* ننتظر زيارتكم للمقر لإتمام الإجراءات.\n\n*شكراً لثقتكم!* 🏔️"
        
        url = get_whatsapp_url(p, msg)
        st.markdown(f'<a href="{url}" style="text-decoration:none;"><button style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; border: none; font-weight: bold; width: 100%;">🚀 إرسال عبر تطبيق واتساب</button></a>', unsafe_allow_html=True)

elif page == "🔍 استعلام عميل":
    st.title("🔍 استعلام عن العميل")
    col_name = next((c for c in df.columns if 'اسم' in c), None)
    selected = st.selectbox("اختر العميل:", df[col_name].dropna().tolist())
    if selected:
        st.write(df[df[col_name] == selected].T)

elif page == "📋 الكشف الكلي":
    st.dataframe(df, use_container_width=True)

elif page == "💰 المالية":
    st.dataframe(st.session_state['df_finance'], use_container_width=True)

if st.sidebar.button("🔒 تسجيل الخروج"):
    st.session_state['authenticated'] = False
    st.rerun()
