

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
                st.success("تم التحقق بنجاح! جاري تحميل المنظومة...")
                st.rerun()
            else:
                st.error("❌ كلمة المرور غير صحيحة، يرجى إعادة المحاولة.")
    st.stop()

# ====================================================
# 🚌 بداية المنظومة الأصلية بعد تخطي جدار الحماية
# ====================================================
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    encoded_sheet = urllib.parse.quote(sheet_name)
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    col_name = next((c for c in data.columns if 'الاسم' in c or 'اسم' in c), None)
    if col_name and sheet_name == 'Form responses 1':
        data = data.sort_values(by=col_name).reset_index(drop=True)
    return data

def get_wa_url(phone, text):
    return f"https://wa.me/{phone}?text={urllib.parse.quote(text)}"

def convert_df_to_excel(df_to_export):
    keep_cols = [c for c in df_to_export.columns if any(k in c for k in ['الاسم', 'الهاتف', 'رقم', 'العدد', 'أفراد', 'الإقامة', 'فندق', 'انطلاق', 'مكان'])]
    if not keep_cols: keep_cols = df_to_export.columns[:5]
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

# 🧭 القائمة الجانبية
st.sidebar.title("🏢 لوحة تحكم شركة قصر الهناء")
page = st.sidebar.radio("انتقل إلى القائمة:", [
    "💬 مركز مراسلة حالات الزبائن", "🔍 استعلام وبطاقة حجز عميل", "📋 الكشف الكلي لجميع الركاب",
    "🏢 كشف نزلاء فندق قورينا", "🌲 كشف نزلاء منتجع شحات", "🟢 كشف ركاب طرابلس والغرب", 
    "🔵 كشف ركاب المنطقة الشرقية", "💰 التقارير المالية والإيرادات"
])

# إعدادات الأمان
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ إعدادات الأمان")
with st.sidebar.expander("🔐 تغيير كلمة المرور"):
    current_pass = st.text_input("كلمة المرور الحالية:", type="password", key="cur_pass")
    new_pass = st.text_input("كلمة المرور الجديدة:", type="password", key="new_pass")
    if st.button("🔄 تحديث كلمة المرور"):
        if current_pass == st.session_state['master_password']:
            if new_pass.strip() != "":
                st.session_state['master_password'] = new_pass
                st.success("✅ تم تغيير كلمة المرور بنجاح!")
            else: st.error("❌ لا يمكن تعيين كلمة مرور فارغة.")
        else: st.error("❌ كلمة المرور الحالية غير صحيحة.")

if st.sidebar.button("🔒 تسجيل الخروج الآمن", use_container_width=True):
    st.session_state['authenticated'] = False
    st.rerun()

if st.sidebar.button("🔄 سحب وتحديث البيانات الشاملة", use_container_width=True):
    try:
        st.session_state['df'] = load_data_public('Form responses 1')
        st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
        st.sidebar.success("تم تحديث كافة البيانات!")
    except Exception as e: st.sidebar.error(f"تأكد من إعدادات مشاركة الشيت: {e}")

if 'df' not in st.session_state: st.session_state['df'] = load_data_public('Form responses 1')
if 'df_finance' not in st.session_state: st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')

# ----------------------------------------------------
# 💬 الصفحة الأولى: مركز مراسلة حالات الزبائن
# ----------------------------------------------------
if page == "💬 مركز مراسلة حالات الزبائن":
    st.title("🚌 لوحة تحكم حجوزات قصر الهناء")
    df = st.session_state['df']
    col_name = next((c for c in df.columns if 'الاسم' in c), None)
    col_phone = next((c for c in df.columns if 'الهاتف' in c), None)
    
    if col_name and col_phone:
        selected_user = st.selectbox("اختر اسم الزبون:", df[col_name].dropna().tolist())
        user_data = df[df[col_name] == selected_user].iloc[0]
        u_phone = str(user_data[col_phone]).replace('.0','')
        
        # رسائل منظمة مع التنسيق (الأموجيات والخط العريض)
        msg_confirm = f"السلام عليكم ورحمة الله وبركاته،\n\nمرحباً بك في عائلة *شركة قصر الهناء للخدمات السياحية* 🌹\n\nتم استلام بيانات تسجيلكم لرحلة (الجبل الأخضر الساحر 2026) بنجاح 📊✨\n\n📌 *الاسم:* {user_data[col_name]}\n💳 يعتبر الحجز مبدئياً حتى تأكيد السداد المالي.\n\n*شكراً لثقتكم باختيار قصر الهناء!* 🏔️"
        
        url_confirm = get_wa_url(u_phone, msg_confirm)
        st.markdown(f'<a href="{url_confirm}" target="_blank"><button style="background-color: #2b5c8f; color: white; padding: 12px; width: 100%;">🔵 1. إرسال تأكيد الاستلام</button></a>', unsafe_allow_html=True)

# ----------------------------------------------------
# باقي الصفحات (نفس منطقك الأصلي)
# ----------------------------------------------------
elif page == "🔍 استعلام وبطاقة حجز عميل":
    st.title("🔍 نظام الاستعلام الفوري")
    # ... (بقية كودك الخاص بالاستعلام)
