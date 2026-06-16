

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# ====================================================
# 🚌 متن المنظومة الأصلية بالكامل
# ====================================================
def main_system():
    SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

    def load_data_public(sheet_name):
        encoded_sheet = urllib.parse.quote(sheet_name)
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}"
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        
        col_name = next((c for c in data.columns if 'الاسم' in c or 'اسم' in c), None)
        if col_name and sheet_name == 'Form responses 1':
            data = data.sort_values(by=col_name).reset_index(drop=True)
        return data

    def convert_df_to_excel(df_to_export):
        valid_keys = ['الاسم', 'الهاتف', 'رقم', 'العدد', 'أفراد', 'الإقامة', 'فندق', 'انطلاق', 'مكان', 'تكلفة', 'مبلغ', 'قيمة', 'دفع', 'سداد']
        keep_cols = [c for c in df_to_export.columns if any(k in c for k in valid_keys)]
        if not keep_cols:
            keep_cols = df_to_export.columns[:5]
        
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
        "💬 مركز مراسلة حالات الزبائن",
        "🔍 استعلام وبطاقة حجز عميل",
        "📋 الكشف الكلي لجميع الركاب",
        "🏢 كشف نزلاء فندق قورينا",
        "🌲 كشف نزلاء منتجع شحات",
        "🟢 كشف ركاب طرابلس والغرب", 
        "🔵 كشف ركاب المنطقة الشرقية", 
        "💰 التقارير المالية والإيرادات"
    ])

    st.sidebar.markdown("---")

    # 🛠️ مربع تغيير الباسورد الذكي
    st.sidebar.markdown("### ⚙️ إعدادات الأمان")
    with st.sidebar.expander("🔐 تغيير كلمة المرور"):
        current_pass = st.text_input("كلمة المرور الحالية:", type="password", key="cur_pass")
        new_pass = st.text_input("كلمة المرور الجديدة:", type="password", key="new_pass")
        
        if st.button("🔄 تحديث كلمة المرور"):
            if current_pass == st.session_state['master_password']:
                if new_pass.strip() != "":
                    st.session_state['master_password'] = new_pass
                    st.success("✅ تم تغيير كلمة المرور بنجاح!")
                else:
                    st.error("❌ لا يمكن تعيين كلمة مرور فارغة.")
            else:
                st.error("❌ كلمة المرور الحالية غير صحيحة.")

    st.sidebar.markdown("---")
    if st.sidebar.button("🔒 تسجيل الخروج الآمن", use_container_width=True):
        st.session_state['authenticated'] = False
        st.rerun()

    if st.sidebar.button("🔄 سحب وتحديث البيانات الشاملة", use_container_width=True):
        try:
            st.session_state['df'] = load_data_public('Form responses 1')
            st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
            st.sidebar.success("تم تحديث كافة البيانات الماليّة والحجوزات!")
        except Exception as e:
            st.sidebar.error(f"تأكد من إعدادات مشاركة الشيت: {e}")

    if 'df' not in st.session_state:
        try: st.session_state['df'] = load_data_public('Form responses 1')
        except: pass

    if 'df_finance' not in st.session_state:
        try: st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
        except: pass

    # ----------------------------------------------------
    # 💬 الصفحة الأولى: مركز مراسلة حالات الزبائن
    # ----------------------------------------------------
    if page == "💬 مركز مراسلة حالات الزبائن":
        st.title("🚌 لوحة تحكم حجوزات قصر الهناء")
        st.subheader("مركز المراسلات الذكي وحالات الزبائن")
        st.markdown("---")

        if 'df' in st.session_state:
            df = st.session_state['df']
            col_name = next((c for c in df.columns if 'الاسم' in c or 'اسم' in c), None)
            col_phone = next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c or 'موبايل' in c), None)
            col_count = next((c for c in df.columns if 'العدد' in c or 'أفراد' in c or 'اشخاص' in c), None)
            col_hotel = next((c for c in df.columns if 'الإقامة' in c or 'فندق' in c or 'محل' in c), None)
            col_region = next((c for c in df.columns if 'انطلاق' in c or 'مكان' in c or 'تسجيل' in c), None)

            if col_region:
                unique_regions = ["الكل"] + list(df[col_region].dropna().unique())
                region = st.selectbox(f"تصفية سريعة حسب {col_region}:", unique_regions)
                df_filtered = df[df[col_region] == region] if region != "الكل" else df.copy()
            else:
                df_filtered = df.copy()
                
            if not col_name or not col_phone:
                st.warning("⚠️ للمراسلة: تأكد من وجود عمود الاسم وعمود الهاتف في الشيت.")
            else:
                selected_user = st.selectbox("اختر اسم الزبون المراد مراسلته عبر الواتساب:", df_filtered[col_name].dropna().tolist())
                
                if selected_user:
                    user_data = df_filtered
