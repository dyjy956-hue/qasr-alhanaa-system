

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")
st.title("🚌 لوحة تحكم حجوزات قصر الهناء")
st.subheader("رحلة الجبل الأخضر 2026")

SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'
SHEET_NAME = 'Form responses 1' 

def load_data_public():
    encoded_sheet = urllib.parse.quote(SHEET_NAME)
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

if st.button("🔄 تحديث وسحب الحجوزات الحالية"):
    try:
        st.session_state['df'] = load_data_public()
        st.success("تم تحديث كشف الحجوزات بنجاح من السحابة!")
    except Exception as e:
        st.error(f"تأكد من إعدادات مشاركة الشيت العام: {e}")

if 'df' in st.session_state:
    df = st.session_state['df']
    
    col_name = next((c for c in df.columns if 'الاسم' in c or 'اسم' in c), None)
    col_phone = next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c or 'موبايل' in c), None)
    col_count = next((c for c in df.columns if 'العدد' in c or 'أفراد' in c or 'اشخاص' in c), None)
    col_hotel = next((c for c in df.columns if 'الإقامة' in c or 'فندق' in c or 'محل' in c), None)
    col_region = next((c for c in df.columns if 'انطلاق' in c or 'مكان' in c or 'تسجيل' in c), None)

    if not col_name or not col_phone:
        st.error("⚠️ خطأ برميجي: لم نتمكن من تحديد عمود 'الاسم' أو 'رقم الهاتف' تلقائياً.")
    else:
        if col_region:
            region = st.selectbox(f"تصفية حسب {col_region}:", ["الكل"] + list(df[col_region].dropna().unique()))
            if region != "الكل":
                df = df[df[col_region] == region]
        
        st.dataframe(df, use_container_width=True)
        st.markdown("---")
        
        selected_user = st.selectbox("اختر اسم الزبون لإرسال التأكيد:", df[col_name].dropna().tolist())
        
        if selected_user:
            user_data = df[df[col_name] == selected_user].iloc[0]
            
            u_name = user_data[col_name]
            u_phone = user_data[col_phone]
            u_count = user_data[col_count] if col_count else "غير محدد"
            u_hotel = user_data[col_hotel] if col_hotel else "غير محدد"
            u_reg = user_data[col_region] if col_region else "غير محدد"
            
            # الرسالة نصية بالكامل بدون أي روابط صور
            msg = (
                f"السلام عليكم ورحمة الله وبركاته،\n\n"
                f"مرحباً بك في عائلة *شركة قصر الهناء للخدمات السياحية* 🌹\n\n"
                f"تم استلام بيانات تسجيلكم لرحلة (الجبل الأخضر الساحر 2026) بنجاح عبر المنظومة 📊✨\n\n"
                f"📌 *الاسم:* {u_name}\n"
                f"👥 *العدد:* {u_count} أشخاص\n"
                f"🏨 *الإقامة:* {u_hotel}\n"
                f"📍 *مكان الانطلاق:* {u_reg}\n\n"
                f"💳 يعتبر الحجز مبدئياً حتى تأكيد السداد المالي.\n\n"
                f"*شكراً لثقتكم باختيار قصر الهناء!* 🏔️"
            )
            
            phone_str = str(u_phone).replace('.0','') if '.' in str(u_phone) else str(u_phone)
            wa_url = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg)}"
            
            # الزر يفتح المحادثة بالنص الصافي مباشرة
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px 24px; border-radius: 5px; font-size: 16px; cursor: pointer; font-weight: bold;">🟢 إرسال التأكيد بالواتساب</button></a>', unsafe_allow_html=True)
