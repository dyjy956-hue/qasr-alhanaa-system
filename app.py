

# تعليق لحماية السطر الأول من المسافات التلقائية
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
    # SHEET_ID الثابت العام للمنظومة
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

    def convert_df_to_excel(df_to_export):
        valid_keys = ['الاسم', 'الهاتف', 'رقم', 'العدد', 'أفراد', 'الإقامة', 'فندق', 'انطلاق', 'مكان', 'تكلفة', 'مبلغ', 'قيمة', 'دفع', 'سداد']
        keep_cols = [c for c in df_to_export.columns if any(k in c for k in valid_keys)]
        if not keep_cols: keep_cols = df_to_export.columns[:5]
        df_clean = df_to_export[keep_cols].copy()
        df_clean.insert(0, '#', range(1, len(df_clean) + 1))
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_clean.to_excel(writer, index=False, sheet_name='الكشف الرسمي')
        return output.getvalue()

    # 🧭 القائمة الجانبية
    st.sidebar.title("🏢 لوحة تحكم شركة قصر الهناء")
    page = st.sidebar.radio("انتقل إلى القائمة:", [
        "💬 مركز مراسلة حالات الزبائن", "🔍 استعلام وبطاقة حجز عميل", "📋 الكشف الكلي لجميع الركاب",
        "🏢 كشف نزلاء فندق قورينا", "🌲 كشف نزلاء منتجع شحات", "🟢 كشف ركاب طرابلس والغرب", 
        "🔵 كشف ركاب المنطقة الشرقية", "💰 التقارير المالية والإيرادات"
    ])

    if 'df' not in st.session_state:
        try: st.session_state['df'] = load_data_public('Form responses 1')
        except: pass

    # ----------------------------------------------------
    # 💬 مركز مراسلة حالات الزبائن (هنا تم تعديل الروابط)
    # ----------------------------------------------------
    if page == "💬 مركز مراسلة حالات الزبائن":
        st.title("🚌 مركز المراسلات الذكي")
        if 'df' in st.session_state:
            df = st.session_state['df']
            col_name = next((c for c in df.columns if 'الاسم' in c or 'اسم' in c), None)
            col_phone = next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c), None)
            
            selected_user = st.selectbox("اختر العميل:", df[col_name].dropna().tolist())
            if selected_user:
                u = df[df[col_name] == selected_user].iloc[0]
                p = str(u[col_phone]).replace('.0','').replace('+', '').replace(' ', '')
                
                # نصوص ملونة ومنظمة
                msg = f"✨ *شركة قصر الهناء للخدمات السياحية* 🌹\n\nأهلاً أستاذ/ة *{u[col_name]}*،\nتم تأكيد تسجيلكم لرحلة (الجبل الأخضر 2026) بنجاح 📊✨\n\n📌 *تفاصيل الحجز:* \n👥 العدد: {u.get('العدد', 'غير محدد')}\n🏨 الإقامة: {u.get('الإقامة', 'غير محدد')}\n\n💳 *ملاحظة:* ننتظر زيارتكم للمقر لإتمام الإجراءات.\n\n*شكراً لثقتكم!* 🏔️"
                
                # استخدام رابط التطبيق المباشر
                url = f"whatsapp://send?phone={p}&text={urllib.parse.quote(msg)}"
                
                st.markdown(f'<a href="{url}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 15px; border-radius: 10px; font-weight: bold; width: 100%;">🚀 إرسال رسالة من تطبيق واتساب</button></a>', unsafe_allow_html=True)

    # 🔍 استعلام (مع عمود التكلفة)
    elif page == "🔍 استعلام وبطاقة حجز عميل":
        df = st.session_state['df']
        col_money = next((c for c in df.columns if 'تكلفة' in c or 'مبلغ' in c), None)
        # (باقي كود الاستعلام كما هو)
        st.info(f"إجمالي التكلفة: {df[col_money].iloc[0] if col_money else 'غير موجود'}")

# التشغيل الآمن
if st.session_state['authenticated']:
    main_system()
else:
    # (كود الدخول كما هو)
    if st.button("🔓 تسجيل الدخول"): st.session_state['authenticated'] = True; st.rerun()
