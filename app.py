

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# ====================================================
# 🔒 نظام الحماية والأمان المطور
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
        st.write("### مرحباً بك في لوحة تحكم الإدارة")
        user_password = st.text_input("الرجاء إدخال كلمة مرور المنظومة للدخول:", type="password")
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

def get_wa_intent(phone, text):
    # تنظيف وتجهيز الرقم الليبي
    p = str(phone).replace('.0','').replace(' ','').replace('+','').replace('-','')
    if len(p) == 9 and p.startswith('9'): p = "218" + p
    elif len(p) == 10 and p.startswith('09'): p = "218" + p[1:]
    encoded_text = urllib.parse.quote(text)
    return f"intent://send?phone={p}&text={encoded_text}#Intent;scheme=smsto;package=com.whatsapp;action=android.intent.action.SENDTO;end"

def convert_df_to_excel(df_to_export):
    keep_cols = [c for c in df_to_export.columns if any(k in c for k in ['الاسم', 'الهاتف', 'رقم', 'العدد', 'أفراد', 'الإقامة', 'فندق', 'انطلاق', 'مكان'])]
    if not keep_cols: keep_cols = df_to_export.columns[:5]
    df_clean = df_to_export[keep_cols].copy()
    df_clean.insert(0, '#', range(1, len(df_clean) + 1))
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_clean.to_excel(writer, index=False)
    return output.getvalue()

def display_styled_dataframe(dataframe):
    df_display = dataframe.copy()
    df_display.insert(0, '#', range(1, len(df_display) + 1))
    st.dataframe(df_display.set_index('#'), use_container_width=True)

# 🧭 القائمة الجانبية
st.sidebar.title("🏢 لوحة تحكم شركة قصر الهناء")
page = st.sidebar.radio("انتقل إلى القائمة:", [
    "💬 مركز مراسلة حالات الزبائن", "🔍 استعلام وبطاقة حجز عميل", "📋 الكشف الكلي لجميع الركاب",
    "🏢 كشف نزلاء فندق قورينا", "🌲 كشف نزلاء منتجع شحات", "🟢 كشف ركاب طرابلس والغرب", 
    "🔵 كشف ركاب المنطقة الشرقية", "💰 التقارير المالية والإيرادات"
])

# الأمان والتحديث
if st.sidebar.button("🔄 سحب وتحديث البيانات الشاملة", use_container_width=True):
    st.session_state['df'] = load_data_public('Form responses 1')
    st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
    st.rerun()

if 'df' not in st.session_state: st.session_state['df'] = load_data_public('Form responses 1')
if 'df_finance' not in st.session_state: st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')

# ----------------------------------------------------
# 💬 الصفحة الأولى: مركز مراسلة حالات الزبائن
# ----------------------------------------------------
if page == "💬 مركز مراسلة حالات الزبائن":
    st.title("🚌 لوحة تحكم حجوزات قصر الهناء")
    df = st.session_state['df']
    col_name = next((c for c in df.columns if 'الاسم' in c), None)
    col_phone = next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c), None)
    
    if col_name and col_phone:
        selected_user = st.selectbox("اختر الزبون:", df[col_name].dropna().tolist())
        u_data = df[df[col_name] == selected_user].iloc[0]
        
        msg = f"السلام عليكم،\nمرحباً بك *{u_data[col_name]}* 🌹\nتم استلام بياناتكم بنجاح في شركة قصر الهناء."
        url = get_wa_intent(u_data[col_phone], msg)
        st.markdown(f'<a href="{url}" target="_blank"><button style="background-color: #25D366; color: white; padding: 12px; width: 100%;">📲 إرسال رسالة واتساب</button></a>', unsafe_allow_html=True)

# ----------------------------------------------------
# 🔍 الصفحة الثانية: استعلام وبطاقة حجز عميل (مع التكلفة)
# ----------------------------------------------------
elif page == "🔍 استعلام وبطاقة حجز عميل":
    st.title("🔍 نظام الاستعلام الفوري")
    df = st.session_state['df']
    col_name = next((c for c in df.columns if 'الاسم' in c), None)
    col_cost = next((c for c in df.columns if 'تكلفة' in c or 'مبلغ' in c or 'سعر' in c), None)
    
    if col_name:
        search_user = st.selectbox("🎯 اختر العميل:", ["-- اختر --"] + df[col_name].dropna().tolist())
        if search_user != "-- اختر --":
            u = df[df[col_name] == search_user].iloc[0]
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border-right: 5px solid #1d3557;">
                <h3>🎫 بطاقة الحجز</h3>
                <p><b>👤 الاسم:</b> {u.get(col_name)}</p>
                <div style="background-color: #fff3cd; padding: 10px; border-radius: 5px;">
                    <p style="font-size: 18px; color: #856404;"><b>💰 إجمالي التكلفة: {u.get(col_cost, 'غير مسجل')}</b></p>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ----------------------------------------------------
# الصفحات الأخرى (عرض البيانات)
# ----------------------------------------------------
elif "كشف" in page or "الكشف" in page or "التقارير" in page:
    if page == "💰 التقارير المالية والإيرادات": st.dataframe(st.session_state['df_finance'], use_container_width=True)
    else: display_styled_dataframe(st.session_state['df'])

if st.sidebar.button("🔒 تسجيل الخروج الآمن"):
    st.session_state['authenticated'] = False
    st.rerun()
