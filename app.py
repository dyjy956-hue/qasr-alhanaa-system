

import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# ====================================================
# 🔒 نظام الحماية والأمان
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
# 🚌 بداية المنظومة
# ====================================================
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

def convert_df_to_excel(df_to_export):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_to_export.to_excel(writer, index=False)
    return output.getvalue()

def display_styled_dataframe(dataframe):
    st.dataframe(dataframe, use_container_width=True)

st.sidebar.title("🏢 لوحة تحكم شركة قصر الهناء")
page = st.sidebar.radio("انتقل إلى القائمة:", [
    "💬 مركز مراسلة حالات الزبائن", "🔍 استعلام وبطاقة حجز عميل", "📋 الكشف الكلي لجميع الركاب",
    "🏢 كشف نزلاء فندق قورينا", "🌲 كشف نزلاء منتجع شحات", "🟢 كشف ركاب طرابلس والغرب", 
    "🔵 كشف ركاب المنطقة الشرقية", "💰 التقارير المالية والإيرادات"
])

if 'df' not in st.session_state:
    st.session_state['df'] = load_data_public('Form responses 1')
    st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')

df = st.session_state['df']

# ----------------------------------------------------
# 💬 مركز مراسلة حالات الزبائن (التعديل هنا)
# ----------------------------------------------------
if page == "💬 مركز مراسلة حالات الزبائن":
    st.title("🚌 لوحة تحكم حجوزات قصر الهناء")
    col_name = next((c for c in df.columns if 'اسم' in c), None)
    col_phone = next((c for c in df.columns if 'هاتف' in c or 'رقم' in c), None)
    
    selected_user = st.selectbox("اختر اسم الزبون:", df[col_name].dropna().tolist())
    if selected_user:
        u_data = df[df[col_name] == selected_user].iloc[0]
        p = str(u_data[col_phone]).replace('.0','').replace('+', '').replace(' ', '')
        
        # نصوص الرسائل
        msg_text = f"أهلاً أستاذ/ة {selected_user}، تم تأكيد تسجيلكم لرحلة الجبل الأخضر 2026."
        
        # التعديل الجوهري: استخدام whatsapp://send لفتح التطبيق مباشرة
        url = f"whatsapp://send?phone={p}&text={urllib.parse.quote(msg_text)}"
        
        st.markdown(f'<a href="{url}" style="text-decoration:none;"><button style="background-color: #25D366; color: white; padding: 15px; border-radius: 8px; border: none; font-weight: bold; width: 100%;">🚀 إرسال عبر تطبيق واتساب</button></a>', unsafe_allow_html=True)

# ----------------------------------------------------
# باقة الصفحات الأخرى (تم اختصارها للتنظيم)
# ----------------------------------------------------
elif page == "📋 الكشف الكلي لجميع الركاب":
    display_styled_dataframe(df)

elif page == "💰 التقارير المالية والإيرادات":
    st.dataframe(st.session_state['df_finance'], use_container_width=True)

# زر الخروج
if st.sidebar.button("🔒 تسجيل الخروج"):
    st.session_state['authenticated'] = False
    st.rerun()
