import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")
st.title("🚌 لوحة تحكم حجوزات قصر الهناء")
st.subheader("رحلة الجبل الأخضر 2026")

SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'
SHEET_NAME = 'Sheet1' 

def load_data_public():
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    return pd.read_csv(url)

# زر تحديث وسحب البيانات
if st.button("🔄 تحديث وسحب الحجوزات الحالية"):
    try:
        st.session_state['df'] = load_data_public()
        st.success("تم تحديث كشف الحجوزات بنجاح من السحابة!")
    except Exception as e:
        st.error(f"تأكد من إعدادات مشاركة الشيت العام: {e}")

if 'df' in st.session_state:
    df = st.session_state['df']
    
    # تصفية المناطق
    region = st.selectbox("تصفية حسب نقطة الانطلاق:", ["الكل"] + list(df['نقطة الانطلاق'].dropna().unique()))
    if region != "الكل":
        df = df[df['نقطة الانطلاق'] == region]
        
    st.dataframe(df, use_container_width=True)
    
    st.markdown("---")
    
    # قسم المراسلة والتأكيد بنقرة واحدة
    selected_user = st.selectbox("اختر اسم الزبون لإرسال التأكيد:", df['الاسم'].dropna().tolist())
    
    if selected_user:
        user_data = df[df['الاسم'] == selected_user].iloc[0]
        
        # رسالة التأكيد المدمج بها رابط صورة مسار الجبل الأخضر
        msg = (
            f"السلام عليكم ورحمة الله وبركاته،\n\n"
            f"مرحباً بك في عائلة *شركة قصر الهناء للخدمات السياحية* 🌹\n\n"
            f"تم استلام بيانات تسجيلكم لرحلة (الجبل الأخضر الساحر 2026) بنجاح عبر المنظومة 📊✨\n\n"
            f"📌 *الاسم:* {user_data['الاسم']}\n"
            f"👥 *العدد:* {user_data['عدد الأفراد']} أشخاص\n"
            f"🏨 *الإقامة:* {user_data['محل الإقامة']}\n"
            f"📍 *الانطلاق:* {user_data['نقطة الانطلاق']}\n\n"
            f"💳 يعتبر الحجز مبدئياً حتى تأكيد السداد المالي.\n\n"
            f"📸 *لمحة مشوّقة من طبيعة مسارات الجبل الأخضر التي تنتظركم:*\n"
            f"https://images.squarespace-cdn.com/content/v1/660dae564d262963351f7bb5/c209861f-9da3-42e5-ad24-4f59e984f49b/1000150093.jpg\n\n"
            f"*شكراً لثقتكم باختيار قصر الهناء!* 🏔️"
        )
        
        phone_str = str(user_data['رقم الهاتف']).replace('.0','') if '.' in str(user_data['رقم الهاتف']) else str(user_data['رقم الهاتف'])
        wa_url = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg)}"
        
        # عرض صورة الجبل الأخضر للموظف
        st.image("https://images.squarespace-cdn.com/content/v1/660dae564d262963351f7bb5/c209861f-9da3-42e5-ad24-4f59e984f49b/1000150093.jpg", width=350, caption="صورة مسار الجبل الأخضر المرفقة بالرسالة")
        
        # زر الإرسال بالواتساب
        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px 24px; border-radius: 5px; font-size: 16px; cursor: pointer; font-weight: bold;">🟢 إرسال التأكيد + الصورة بالواتساب</button></a>', unsafe_allow_html=True)
