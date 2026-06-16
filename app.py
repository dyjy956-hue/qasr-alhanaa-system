

import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# SHEET_ID الثابت العام للمنظومة
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    encoded_sheet = urllib.parse.quote(sheet_name)
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

# 🧭 القائمة الجانبية
st.sidebar.title("🏢 لوحة تحكم شركة قصر الهناء")
page = st.sidebar.radio("انتقل إلى القائمة:", [
    "💬 مركز مراسلة حالات الزبائن",
    "🔍 استعلام وبطاقة حجز عميل",
    "📋 الكشف الكلي لجميع الركاب",
    "🏢 كشف نزلاء فندق قورينا",
    "🌲 كشف نزلاء منتجع شحات",
    "🟢 كشف ركاب طرابلس والغرب", 
    "🔵 كشف ركاب المنطقة الشرقية", 
    "💰 التقارير المالية والإيرادات"
])

# زر التحديث العام
if st.sidebar.button("🔄 سحب وتحديث البيانات الشاملة"):
    try:
        st.session_state['df'] = load_data_public('Form responses 1')
        st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
        st.sidebar.success("تم التحديث بنجاح!")
    except Exception as e:
        st.sidebar.error(f"خطأ في الاتصال: {e}")

# التأكد من تحميل البيانات
if 'df' not in st.session_state:
    try: st.session_state['df'] = load_data_public('Form responses 1')
    except: pass
if 'df_finance' not in st.session_state:
    try: st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
    except: pass

# ----------------------------------------------------
# 💬 الصفحة الأولى: مركز المراسلة
# ----------------------------------------------------
if page == "💬 مركز مراسلة حالات الزبائن":
    st.title("🚌 لوحة تحكم حجوزات قصر الهناء")
    st.markdown("---")
    if 'df' in st.session_state:
        df = st.session_state['df']
        col_name = next((c for c in df.columns if 'الاسم' in c), None)
        if col_name:
            selected_user = st.selectbox("اختر العميل للمراسلة:", df[col_name].dropna().tolist())
            st.write("مركز المراسلات مفعّل.")

# ----------------------------------------------------
# 🔍 الصفحة الثانية: استعلام وبطاقة حجز عميل
# ----------------------------------------------------
elif page == "🔍 استعلام وبطاقة حجز عميل":
    st.title("🔍 نظام الاستعلام الفوري وعرض بيانات الحجز")
    st.markdown("---")
    
    if 'df' in st.session_state:
        df = st.session_state['df']
        col_name = next((c for c in df.columns if 'الاسم' in c or 'اسم' in c), None)
        col_cost = next((c for c in df.columns if 'تكلفة' in c or 'السعر' in c), None)
        
        if col_name:
            search_user = st.selectbox("🎯 اختر اسم العميل للبحث:", ["-- اختر اسماً --"] + df[col_name].dropna().tolist())
            
            if search_user != "-- اختر اسماً --":
                user_full_data = df[df[col_name] == search_user].iloc[0]
                cost_value = user_full_data.get(col_cost, 'غير محدد') if col_cost else "غير متوفر"
                
                card_html = f"""
<div style="background-color: #f8f9fa; border-right: 5px solid #25D366; padding: 20px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
    <h3 style="color: #1d3557; margin-top: 0;">🎫 بطاقة البيانات التفصيلية للحجز</h3>
    <hr style="margin: 10px 0;">
    <p style="font-size: 16px;"><b>👤 الاسم:</b> {user_full_data.get(col_name, 'غير مسجل')}</p>
    <p style="font-size: 16px;"><b>📞 الهاتف:</b> {str(user_full_data.get(next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c), 'الهاتف'), 'غير مسجل')).replace('.0','')}</p>
    <p style="font-size: 16px;"><b>👥 العدد:</b> {user_full_data.get(next((c for c in df.columns if 'العدد' in c or 'أفراد' in c), 'العدد'), 'غير محدد')}</p>
    <p style="font-size: 16px;"><b>🏨 الإقامة:</b> {user_full_data.get(next((c for c in df.columns if 'الإقامة' in c or 'فندق' in c), 'الإقامة'), 'غير محدد')}</p>
    <p style="font-size: 16px;"><b>📍 الانطلاق:</b> {user_full_data.get(next((c for c in df.columns if 'انطلاق' in c or 'مكان' in c), 'مكان الانطلاق'), 'غير محدد')}</p>
    <div style="background-color: #e8f5e9; padding: 10px; border-radius: 5px; margin-top: 10px;">
        <p style="font-size: 18px; color: #2e7d32; margin: 0;"><b>💰 إجمالي التكلفة:</b> {cost_value} د.ل</p>
    </div>
</div>
"""
                st.markdown(card_html, unsafe_allow_html=True)
                st.dataframe(pd.DataFrame([user_full_data]), use_container_width=True)

# ----------------------------------------------------
# بقية الصفحات (الكشف الكلي والتقارير)
# ----------------------------------------------------
elif page == "📋 الكشف الكلي لجميع الركاب":
    st.dataframe(st.session_state['df'], use_container_width=True)

elif page == "💰 التقارير المالية والإيرادات":
    if 'df_finance' in st.session_state:
        st.dataframe(st.session_state['df_finance'], use_container_width=True)
