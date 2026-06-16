

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# ====================================================
# 🔒 نظام الحماية والأمان المطور
# ====================================================
if 'master_password' not in st.session_state: st.session_state['master_password'] = "Samir2026"
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🔒 نظام تسجيل الدخول - شركة قصر الهناء")
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1: st.image("https://cdn-icons-png.flaticon.com/512/3064/3064155.png", width=150)
    with col2:
        st.write("### مرحباً بك في لوحة تحكم الإدارة")
        user_password = st.text_input("الرجاء إدخال كلمة مرور المنظومة للدخول:", type="password")
        if st.button("🔓 تسجيل الدخول"):
            if user_password == st.session_state['master_password']:
                st.session_state['authenticated'] = True
                st.rerun()
            else: st.error("❌ كلمة المرور غير صحيحة.")
    st.stop()

# ====================================================
# الدوال الأساسية
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
        df_to_export.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def display_styled_dataframe(df):
    st.dataframe(df, use_container_width=True)

# ====================================================
# إدارة البيانات في الجلسة
# ====================================================
if 'df' not in st.session_state: st.session_state['df'] = load_data_public('Form responses 1')
if 'df_finance' not in st.session_state: st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')

# ====================================================
# القائمة الجانبية
# ====================================================
st.sidebar.title("🏢 لوحة تحكم شركة قصر الهناء")
page = st.sidebar.radio("انتقل إلى القائمة:", [
    "💬 مركز مراسلة حالات الزبائن", "🔍 استعلام وبطاقة حجز عميل", "📋 الكشف الكلي لجميع الركاب",
    "🏢 كشف نزلاء فندق قورينا", "🌲 كشف نزلاء منتجع شحات", "🟢 كشف ركاب طرابلس والغرب", 
    "🔵 كشف ركاب المنطقة الشرقية", "💰 التقارير المالية والإيرادات"
])

# إعدادات الأمان الجانبية
with st.sidebar.expander("🔐 تغيير كلمة المرور"):
    curr = st.text_input("الحالية:", type="password")
    new_p = st.text_input("الجديدة:", type="password")
    if st.button("🔄 تحديث"):
        if curr == st.session_state['master_password']: st.session_state['master_password'] = new_p; st.success("✅")
        else: st.error("❌")

if st.sidebar.button("🔒 تسجيل الخروج"): st.session_state['authenticated'] = False; st.rerun()

# ====================================================
# منطق الصفحات
# ====================================================
if page == "💬 مركز مراسلة حالات الزبائن":
    df = st.session_state['df']
    col_name = next((c for c in df.columns if 'الاسم' in c), None)
    col_phone = next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c), None)
    
    if col_name and col_phone:
        user = st.selectbox("اختر الزبون:", df[col_name].dropna().tolist())
        u = df[df[col_name] == user].iloc[0]
        phone = str(u[col_phone]).replace('.0','')
        
        def get_url(txt): return f"intent://send?phone={phone}&text={urllib.parse.quote(txt)}#Intent;scheme=smsto;package=com.whatsapp;action=android.intent.action.SENDTO;end"
        
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.markdown(f'<a href="{get_url("تم استلام طلبكم")}" target="_blank"><button style="width:100%">🔵 استلام</button></a>', unsafe_allow_html=True)
        with c2: st.markdown(f'<a href="{get_url("تم التأكيد")}" target="_blank"><button style="width:100%">🏁 تأكيد</button></a>', unsafe_allow_html=True)
        with c3: st.markdown(f'<a href="{get_url("تم السداد")}" target="_blank"><button style="width:100%">🟢 سداد</button></a>', unsafe_allow_html=True)
        with c4: st.markdown(f'<a href="{get_url("بيانات الباص")}" target="_blank"><button style="width:100%">🚌 باص</button></a>', unsafe_allow_html=True)
        with c5: st.markdown(f'<a href="{get_url("تم الإلغاء")}" target="_blank"><button style="width:100%">🔴 إلغاء</button></a>', unsafe_allow_html=True)

elif page == "🔍 استعلام وبطاقة حجز عميل":
    df = st.session_state['df']
    col_name = next((c for c in df.columns if 'الاسم' in c), None)
    col_cost = next((c for c in df.columns if 'تكلفة' in c or 'مبلغ' in c), None)
    user = st.selectbox("🎯 اختر العميل:", ["--"] + df[col_name].dropna().tolist())
    if user != "--":
        u = df[df[col_name] == user].iloc[0]
        st.write(f"### 💰 التكلفة: {u.get(col_cost, 'غير محدد')}")

elif "كشف" in page:
    df = st.session_state['df']
    if "قورينا" in page: df = df[df.astype(str).apply(lambda x: x.str.contains("قورينا")).any(axis=1)]
    elif "شحات" in page: df = df[df.astype(str).apply(lambda x: x.str.contains("شحات")).any(axis=1)]
    st.download_button("📥 تحميل Excel", convert_df_to_excel(df), "data.xlsx")
    display_styled_dataframe(df)

elif page == "💰 التقارير المالية والإيرادات":
    st.dataframe(st.session_state['df_finance'])
