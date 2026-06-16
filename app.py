

import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# إعداد الحالة الأولية
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'master_password' not in st.session_state:
    st.session_state['master_password'] = "Samir2026"

# دالة تحميل البيانات
def load_data():
    sheet_id = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Form%20responses%201"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

# واجهة تسجيل الدخول
if not st.session_state['authenticated']:
    st.title("🔒 تسجيل دخول منظومة قصر الهناء")
    pw = st.text_input("كلمة المرور:", type="password")
    if st.button("دخول"):
        if pw == st.session_state['master_password']:
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("كلمة المرور خاطئة")
else:
    # المنظومة الأساسية
    st.sidebar.title("🏢 لوحة التحكم")
    page = st.sidebar.radio("اختر القسم:", ["💬 مراسلة الزبائن", "🔍 استعلام وتكلفة", "📋 الكشف الكلي"])
    
    if 'df' not in st.session_state:
        st.session_state['df'] = load_data()
    
    df = st.session_state['df']
    
    # 1. المراسلة
    if page == "💬 مراسلة الزبائن":
        st.title("💬 مركز المراسلات")
        name_col = next((c for c in df.columns if 'اسم' in c), df.columns[0])
        phone_col = next((c for c in df.columns if 'هاتف' in c or 'رقم' in c), df.columns[1])
        
        selected = st.selectbox("اختر العميل:", df[name_col].dropna().tolist())
        if selected:
            row = df[df[name_col] == selected].iloc[0]
            phone = str(row[phone_col]).replace('.0', '').replace('+', '').replace(' ', '')
            msg = f"أهلاً أستاذ {selected}، تم تأكيد حجزكم مع شركة قصر الهناء."
            url = f"whatsapp://send?phone={phone}&text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{url}" target="_blank"><button style="background-color:#25D366; color:white; padding:15px; border-radius:10px; width:100%; border:none;">🚀 إرسال عبر واتساب</button></a>', unsafe_allow_html=True)

    # 2. الاستعلام والتكلفة
    elif page == "🔍 استعلام وتكلفة":
        st.title("🔍 استعلام عن العميل")
        name_col = next((c for c in df.columns if 'اسم' in c), df.columns[0])
        cost_col = next((c for c in df.columns if 'تكلفة' in c), None)
        
        selected = st.selectbox("اختر العميل:", df[name_col].dropna().tolist())
        if selected:
            row = df[df[name_col] == selected].iloc[0]
            cost = row.get(cost_col, "غير مسجل") if cost_col else "لا يوجد عمود تكلفة"
            st.success(f"👤 العميل: {selected} | 💰 إجمالي التكلفة: {cost}")

    # 3. الكشف الكلي
    elif page == "📋 الكشف الكلي":
        st.dataframe(df, use_container_width=True)

    if st.sidebar.button("خروج"):
        st.session_state['authenticated'] = False
        st.rerun()
