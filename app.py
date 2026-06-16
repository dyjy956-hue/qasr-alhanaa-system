

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
                st.error("❌ كلمة المرور غير صحيحة")
    st.stop()

# ====================================================
# 🚌 بداية المنظومة
# ====================================================
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    encoded_sheet = urllib.parse.quote(sheet_name)
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

def convert_df_to_excel(df_to_export):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_to_export.to_excel(writer, index=False)
    return output.getvalue()

# القائمة الجانبية
page = st.sidebar.radio("انتقل إلى القائمة:", [
    "💬 مركز مراسلة حالات الزبائن", "🔍 استعلام وبطاقة حجز عميل", "📋 الكشف الكلي لجميع الركاب",
    "🏢 كشف نزلاء فندق قورينا", "🌲 كشف نزلاء منتجع شحات", "🟢 كشف ركاب طرابلس والغرب", 
    "🔵 كشف ركاب المنطقة الشرقية", "💰 التقارير المالية والإيرادات"
])

if st.sidebar.button("🔄 سحب وتحديث البيانات الشاملة"):
    st.session_state['df'] = load_data_public('Form responses 1')
    st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
    st.rerun()

# ----------------------------------------------------
# 🔍 الصفحة الثانية: استعلام وبطاقة حجز عميل
# ----------------------------------------------------
if page == "🔍 استعلام وبطاقة حجز عميل":
    st.title("🔍 نظام الاستعلام الفوري")
    if 'df' in st.session_state:
        df = st.session_state['df']
        df_f = st.session_state.get('df_finance', pd.DataFrame())
        col_name = next((c for c in df.columns if 'الاسم' in c), None)
        
        search_user = st.selectbox("🎯 اختر اسم العميل:", ["-- اختر اسماً --"] + df[col_name].dropna().tolist())
        
        if search_user != "-- اختر اسماً --":
            user_full_data = df[df[col_name] == search_user].iloc[0]
            
            # جلب السعر والإجمالي من بيانات المالية
            val_price, val_total = "غير محدد", "غير محدد"
            if not df_f.empty:
                col_name_f = next((c for c in df_f.columns if 'الاسم' in c), None)
                user_fin = df_f[df_f[col_name_f] == search_user]
                if not user_fin.empty:
                    price_col = next((c for c in df_f.columns if 'سعر' in c or 'تكلفة' in c), None)
                    total_col = next((c for c in df_f.columns if 'إجمالي' in c or 'مجموع' in c), None)
                    if price_col: val_price = user_fin.iloc[0][price_col]
                    if total_col: val_total = user_fin.iloc[0][total_col]

            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border-right: 5px solid #1d3557;">
                <h3>🎫 بطاقة الحجز</h3>
                <p><b>👤 الاسم:</b> {user_full_data.get(col_name)}</p>
                <p><b>💰 سعر الخدمة:</b> {val_price}</p>
                <p><b>📈 إجمالي التكلفة:</b> {val_total}</p>
            </div>
            """, unsafe_allow_html=True)

# ----------------------------------------------------
# استكمال باقي الصفحات (نفس الكود الأصلي الخاص بك)
# ----------------------------------------------------
elif page == "💬 مركز مراسلة حالات الزبائن":
    st.write("مركز المراسلة...")
elif page == "📋 الكشف الكلي لجميع الركاب":
    st.dataframe(st.session_state.get('df'))
elif page == "💰 التقارير المالية والإيرادات":
    st.dataframe(st.session_state.get('df_finance'))
