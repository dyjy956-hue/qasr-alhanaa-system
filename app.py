

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

def load_data_from_sheet(sheet_name):
    SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'
    encoded_sheet = urllib.parse.quote(sheet_name)
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

st.sidebar.title("🏢 لوحة تحكم شركة قصر الهناء")
page = st.sidebar.radio("انتقل إلى:", ["📋 إدارة ومراسلة الحجوزات", "💰 التقارير المالية والإيرادات"])

# ----------------------------------------------------
# 📄 الصفحة الأولى: إدارة ومراسلة الحجوزات
# ----------------------------------------------------
if page == "📋 إدارة ومراسلة الحجوزات":
    st.title("🚌 لوحة تحكم حجوزات قصر الهناء")
    st.subheader("رحلة الجبل الأخضر 2026")
    
    if st.button("🔄 تحديث وسحب الحجوزات الحالية"):
        try:
            st.session_state['df_hajj'] = load_data_from_sheet('Form responses 1')
            st.success("تم تحديث كشف الحجوزات بنجاح!")
        except Exception as e:
            st.error(f"تأكد من إعدادات مشاركة شيت الحجوزات: {e}")

    if 'df_hajj' in st.session_state:
        df = st.session_state['df_hajj']
        
        col_name = next((c for c in df.columns if 'الاسم' in c or 'اسم' in c), None)
        col_phone = next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c or 'موبايل' in c), None)
        col_count = next((c for c in df.columns if 'العدد' in c or 'أفراد' in c or 'اشخاص' in c), None)
        col_hotel = next((c for c in df.columns if 'الإقامة' in c or 'فندق' in c or 'محل' in c), None)
        col_region = next((c for c in df.columns if 'انطلاق' in c or 'مكان' in c or 'تسجيل' in c), None)

        if not col_name or not col_phone:
            st.warning("""⚠️ للمراسلة: تأكد من وجود عمود الاسم والهاتف في الشيت.""")
        else:
            tab_tripoli, tab_east = st.tabs(["🟢 كشف باص طرابلس والغرب", "🔵 كشف ركاب المنطقة الشرقية"])
            
            if col_region:
                df_tripoli = df[~df[col_region].astype(str).str.contains("الشرقية")].copy()
                df_east = df[df[col_region].astype(str).str.contains("الشرقية")].copy()
            else:
                df_tripoli = df.copy()
                df_east = pd.DataFrame(columns=df.columns)

            # --- التبويب الأول: طرابلس الغرب ---
            with tab_tripoli:
                st.write(f"### 📊 ركاب طرابلس والمنطقة الغربية ({df_tripoli.shape[0]} مسافر):")
                st.dataframe(df_tripoli, use_container_width=True)
                
                selected_user_t = st.selectbox("اختر اسم الزبون (باص طرابلس):", ["-- اختر اسماً --"] + df_tripoli[col_name].dropna().tolist(), key="tripoli_select")
                if selected_user_t != "-- اختر اسماً --":
                    user_data = df_tripoli[df_tripoli[col_name] == selected_user_t].iloc[0]
                    u_name = user_data[col_name]
                    u_phone = user_data[col_phone]
                    u_count = user_data[col_count] if col_count else "غير محدد"
                    u_hotel = user_data[col_hotel] if col_hotel else "غير محدد"
                    u_reg = str(user_data[col_region]) if col_region else ""
                    phone_str = str(u_phone).replace('.0','') if '.' in str(u_phone) else str(u_phone)
                    
                    msg_confirm = f"""السلام عليكم ورحمة الله وبركاته،

مرحباً بك في عائلة *شركة قصر الهناء للخدمات السياحية* 🌹

تم استلام بيانات تسجيلكم لرحلة (الجبل الأخضر الساحر 2026) بنجاح عبر المنظومة 📊✨

📌 *الاسم:* {u_name}
👥 *العدد:* {u_count} أشخاص
🏨 *الإقامة:* {u_hotel}
📍 *مكان الانطلاق:* {u_reg}

💳 يعتبر الحجز مبدئياً حتى تأكيد السداد المالي.

*شكراً لثقتكم باختيار قصر الهناء!* 🏔️"""

                    msg_remind_pay = f"""مرحباً بك مجدداً وبكل عائلتك الكريمة مع شركة قصر الهناء 👋✨

✅ تم تأكيد حجزكم بنجاح في #الرحلة_العائلية_للجبل_الاخضر 🏔️🚌

💡 الخطوة المتبقية لتثبيت المقاعد نهائياً:
يرجى التكرم بزيارة مقر الشركة لإتمام عملية الدفع وتأكيد الهوية.

📍 عنوان الشركة: طرابلس - الظهرة.
⏰ آخر موعد للاشتراك والدفع: الجمعة 26-06-2026.

📌 ملاحظة: يرجى إحضار إثبات الهوية (الكتيب العائلي أو جوازات السفر) عند الحضور للمقر.

نتطلع لرحلة ممتعة وصناعة ذكريات لا تُنس
