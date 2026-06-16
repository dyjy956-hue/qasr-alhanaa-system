

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
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}"
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        return data

    def convert_df_to_excel(df_to_export):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_to_export.to_excel(writer, index=False)
        return output.getvalue()

    # القائمة الجانبية
    st.sidebar.title("🏢 لوحة تحكم قصر الهناء")
    page = st.sidebar.radio("انتقل إلى:", ["💬 مركز مراسلة حالات الزبائن", "🔍 استعلام وبطاقة حجز عميل", "📋 الكشف الكلي", "💰 التقارير المالية"])

    if 'df' not in st.session_state:
        st.session_state['df'] = load_data_public('Form responses 1')
        st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')

    # 💬 مركز المراسلات (الرابط يفتح التطبيق مباشرة)
    if page == "💬 مركز مراسلة حالات الزبائن":
        st.title("💬 مركز المراسلات الذكي")
        df = st.session_state['df']
        col_name = next((c for c in df.columns if 'اسم' in c), None)
        col_phone = next((c for c in df.columns if 'هاتف' in c or 'رقم' in c), None)
        
        selected = st.selectbox("اختر العميل:", df[col_name].dropna().tolist())
        if selected:
            u = df[df[col_name] == selected].iloc[0]
            p = str(u[col_phone]).replace('.0','').replace('+', '').replace(' ', '')
            msg = f"✨ *شركة قصر الهناء للخدمات السياحية* 🌹\n\nأهلاً أستاذ/ة *{u[col_name]}*،\nتم استلام بيانات تسجيلكم لرحلة (الجبل الأخضر 2026) بنجاح 📊✨\n\n📌 *تفاصيل الحجز:* \n👥 العدد: {u.get('العدد', 'غير محدد')}\n🏨 الإقامة: {u.get('الإقامة', 'غير محدد')}\n\n💳 *ملاحظة:* ننتظر زيارتكم للمقر لإتمام الإجراءات.\n\n*شكراً لثقتكم!* 🏔️"
            url = f"whatsapp://send?phone={p}&text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{url}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 15px; border-radius: 10px; font-weight: bold; width: 100%;">🚀 إرسال رسالة من تطبيق واتساب</button></a>', unsafe_allow_html=True)

    # 🔍 استعلام وبطاقة عميل (مع إجمالي التكلفة)
    elif page == "🔍 استعلام وبطاقة حجز عميل":
        df = st.session_state['df']
        col_name = next((c for c in df.columns
