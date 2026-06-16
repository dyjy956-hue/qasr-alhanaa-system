

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
        user_password = st.text_input("الرجاء إدخال كلمة مرور المنظومة للدخول:", type="password")
        if st.button("🔓 تسجيل الدخول"):
            if user_password == st.session_state['master_password']:
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("❌ كلمة المرور غير صحيحة.")
    st.stop()

# ====================================================
# الدوال الأساسية
# ====================================================
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    encoded_sheet = urllib.parse.quote(sheet_name)
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

# دالة لفتح تطبيق الواتساب مباشرة على الموبايل
def get_wa_intent(phone, text):
    encoded_text = urllib.parse.quote(text)
    return f"intent://send?phone={phone}&text={encoded_text}#Intent;scheme=smsto;package=com.whatsapp;action=android.intent.action.SENDTO;end"

def convert_df_to_excel(df_to_export):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_to_export.to_excel(writer, index=False)
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

# [تحديث البيانات وتسجيل الخروج كما في كودك الأصلي...]
if st.sidebar.button("🔄 سحب وتحديث البيانات الشاملة", use_container_width=True):
    st.session_state['df'] = load_data_public('Form responses 1')
    st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
    st.rerun()

if 'df' not in st.session_state: st.session_state['df'] = load_data_public('Form responses 1')
if 'df_finance' not in st.session_state: st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')

# ----------------------------------------------------
# 💬 الصفحة الأولى: مركز مراسلة حالات الزبائن (مع دالة التطبيق)
# ----------------------------------------------------
if page == "💬 مركز مراسلة حالات الزبائن":
    st.title("🚌 لوحة تحكم حجوزات قصر الهناء")
    df = st.session_state['df']
    # [أضف منطق اختيار العميل هنا...]
    # عند إرسال أي رابط، استخدم:
    # url_confirm = get_wa_intent(phone_str, msg_confirm)

# ----------------------------------------------------
# 🔍 الصفحة الثانية: استعلام وبطاقة حجز عميل (مع التكلفة)
# ----------------------------------------------------
elif page == "🔍 استعلام وبطاقة حجز عميل":
    st.title("🔍 نظام الاستعلام الفوري")
    search_user = st.selectbox("اختر اسم العميل:", ["-- اختر --"] + st.session_state['df']['الاسم'].dropna().tolist())
    if search_user != "-- اختر --":
        user_full_data = st.session_state['df'][st.session_state['df']['الاسم'] == search_user].iloc[0]
        # إيجاد عمود التكلفة
        col_cost = next((c for c in st.session_state['df'].columns if 'تكلفة' in c or 'مبلغ' in c), 'غير مسجل')
        cost_val = user_full_data.get(col_cost, 'غير محدد')
        
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px;">
            <h3>🎫 بطاقة الحجز</h3>
            <p><b>👤 الاسم:</b> {user_full_data['الاسم']}</p>
            <div style="background-color: #fff3cd; padding: 10px; border-radius: 5px;">
                <p style="font-size: 18px; color: #856404;"><b>💰 إجمالي التكلفة:</b> {cost_val}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# [أكمل باقي الصفحات بنفس منطق كودك السابق...]
