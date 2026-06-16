

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

def main_system():
    SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

    def load_data_public(sheet_name):
        url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}'
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        return data

    # القائمة الجانبية
    st.sidebar.title("🏢 لوحة تحكم قصر الهناء")
    page = st.sidebar.radio("انتقل إلى:", ["💬 مراسلة الزبائن", "🔍 استعلام وتكلفة", "📋 الكشف الكلي", "💰 التقارير"])

    if 'df' not in st.session_state:
        st.session_state['df'] = load_data_public('Form responses 1')
        st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
    
    df = st.session_state['df']

    # 💬 صفحة مراسلة الزبائن
    if page == "💬 مراسلة الزبائن":
        st.title("💬 مركز المراسلات الذكي")
        name_col = next((c for c in df.columns if 'اسم' in c), df.columns[0])
        phone_col = next((c for c in df.columns if 'هاتف' in c or 'رقم' in c), df.columns[1])
        
        selected = st.selectbox("اختر العميل:", df[name_col].dropna().tolist())
        if selected:
            row = df[df[name_col] == selected].iloc[0]
            phone = str(row[phone_col]).replace('.0', '').replace('+', '').replace(' ', '')
            
            # نص الرسالة الاحترافي والمزخرف
            msg = f"✨ *شركة قصر الهناء للسياحة* 🌹\n\nأهلاً أستاذ/ة *{selected}*،\nتم استلام بيانات تسجيلكم لرحلة الجبل الأخضر 2026 بنجاح 🚌🏔️\n\n📌 *تفاصيل الحجز:* \n👥 العدد: {row.get('العدد', 'غير محدد')}\n🏨 الإقامة: {row.get('الإقامة', 'غير محدد')}\n\n💳 *ملاحظة:* ننتظر زيارتكم للمقر لإتمام الإجراءات.\n\n*دمتم بخير وفي أمان الله!* 🌹"
            
            # التعديل هنا: استخدام whatsapp://send لفتح التطبيق فوراً
            url = f"whatsapp://send?phone={phone}&text={urllib.parse.quote(msg)}"
            
            st.markdown(f'<a href="{url}"><button style="background-color:#25D366; color:white; padding:15px; border-radius:10px; width:100%; border:none; font-weight:bold; cursor:pointer;">🚀 إرسال رسالة من تطبيق واتساب مباشرة</button></a>', unsafe_allow_html=True)

    # 🔍 الاستعلام
    elif page == "🔍 استعلام وتكلفة":
        name_col = next((c for c in df.columns if 'اسم' in c), df.columns[0])
        cost_col = next((c for c in df.columns if 'تكلفة' in c or 'مبلغ' in c), None)
        selected = st.selectbox("اختر العميل:", df[name_col].dropna().tolist())
        if selected:
            row = df[df[name_col] == selected].iloc[0]
            cost = row.get(cost_col, "غير مسجل") if cost_col else "لا يوجد عمود تكلفة"
            st.markdown(f'<div style="background-color:#f0f2f6; padding:20px; border-radius:10px;"><h3>👤 العميل: {selected}</h3><p><b>💰 إجمالي التكلفة:</b> {cost}</p></div>', unsafe_allow_html=True)

    elif page == "📋 الكشف الكلي":
        st.dataframe(df, use_container_width=True)
    
    elif page == "💰 التقارير":
        st.dataframe(st.session_state['df_finance'], use_container_width=True)

# التشغيل
if st.session_state['authenticated']:
    main_system()
else:
    st.title("🔒 تسجيل دخول منظومة قصر الهناء")
    pw = st.text_input("كلمة المرور:", type="password")
    if st.button("دخول"):
