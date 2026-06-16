

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse
import numpy as np
try:
    import cv2
except ImportError:
    pass

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# SHEET_ID الثابت العام للمنظومة
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    encoded_sheet = urllib.parse.quote(sheet_name)
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

# 🧭 القائمة الجانبية الشاملة للأقسام التسعة الكاملة
st.sidebar.title("🏢 لوحة تحكم شركة قصر الهناء")
page = st.sidebar.radio("انتقل إلى القائمة:", [
    "💬 - مركز مراسلة حالات الزبائن",
    "🔍 استعلام وبطاقة حجز عميل",
    "📋 الكشف الكلي لجميع الركاب",
    "🏢 كشف نزلاء فندق قورينا",
    "🌲 كشف نزلاء منتجع شحات",
    "🟢 كشف ركاب طرابلس والغرب", 
    "🔵 كشف ركاب المنطقة الشرقية", 
    "💰 التقارير المالية والإيرادات",
    "📲 تسجيل حضور العائلات بالباركود"
])

# زر التحديث العام في القائمة الجانبية ليكون متاحاً في كل الصفحات
if st.sidebar.button("🔄 سحب وتحديث البيانات الشاملة"):
    try:
        st.session_state['df'] = load_data_public('Form responses 1')
        st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
        st.sidebar.success("تم تحديث كافة البيانات المالية والحجوزات!")
    except Exception as e:
        st.sidebar.error(f"تأكد من إعدادات مشاركة الشيت: {e}")

# تأمين وجود البيانات في session_state لتفادي أخطاء أول تشغيل
if 'df' not in st.session_state:
    try:
        st.session_state['df'] = load_data_public('Form responses 1')
    except:
        pass

if 'df_finance' not in st.session_state:
    try:
        st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
    except:
        pass

# تهيئة ذاكرة الحضور المؤقتة ليوم الرحلة
if 'attended_phones' not in st.session_state:
    st.session_state['attended_phones'] = []
if 'just_attended' not in st.session_state:
    st.session_state['just_attended'] = None

# ----------------------------------------------------
# 💬 الصفحة الأولى: مركز مراسلة حالات الزبائن
# ----------------------------------------------------
if page == "💬 - مركز مراسلة حالات الزبائن":
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
            region = st.selectbox(f"تصفية سريعة حسب {col_region}:", ["الكل"] + list(df[col_region].dropna().unique()))
            if region != "الكل":
                df_filtered = df[df[col_region] == region]
            else:
                df_filtered = df.copy()
        else:
            df_filtered = df.copy()
            
        if not col_name or not col_phone:
            st.warning("⚠️ للمراسلة: تأكد من وجود عمود يحتوي على 'الاسم' وعمود يحتوي على 'رقم الهاتف' في الشيت.")
        else:
            selected_user = st.selectbox("اختر اسم الزبون المراد مراسلته عبر الواتساب:", df_filtered[col_name].dropna().tolist())
            
            if selected_user:
                user_data = df_filtered[df_filtered[col_name] == selected_user].iloc[0]
                
                u_name = user_data[col_name]
                u_phone = user_data[col_phone]
                u_count = user_data[col_count] if col_count else "غير محدد"
                u_hotel = user_data[col_hotel] if col_hotel else "غير محدد"
                u_reg = str(user_data[col_region]) if col_region else ""
                
                phone_str = str(u_phone).replace('.0','') if '.' in str(u_phone) else str(u_phone)
                
                qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={phone_str}"
                
                msg_confirm = (
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
                
                msg_remind_pay = (
                    f"مرحباً بك مجدداً وبكل عائلتك الكريمة مع شركة قصر الهناء 👋✨\n\n"
                    f"✅ تم تأكيد حجزكم بنجاح في #الرحلة_العائلية_للجبل_الاخضر 🏔️🚌\n\n"
                    f"💡 الخطوة المتبقية لتثبيت المقاعد نهائياً:\n"
                    f"يرجى التكرم بزيارة مقر الشركة لإتمام عملية الدفع وتأكيد الهوية.\n\n"
                    f"📍 عنوان الشركة: طرابلس - الظهرة.\n"
                    f"⏰ آخر موعد للاشتراك والدفع: الجمعة 26-06-2026.\n\n"
                    f"📌 ملاحظة: يرجى إحضار إثبات الهوية (الكتيب العائلي أو جوازات السفر) عند الحضور للمقر.\n\n"
                    f"نتطلع لرحلة ممتعة وصناعة ذكريات لا تُنسى معكم! دمت بخير وفي أمان الله 🌹\n"
                    f"شركة قصر الهناء للاستثمار السياحي."
                )
                
                msg_paid = (
                    f"السلام عليكم ورحمة الله وبركاته،\n\n"
                    f"الأستاذ(ة) الفاضل(ة): *{u_name}* 🌟\n\n"
                    f"يسعدنا إبلاغكم بأنه **تم تأكيد السداد المالي بنجاح** وقبول حجزكم نهائياً لرحلة (الجبل الأخضر الساحر 2026) ✅💳\n\n"
                    f"👥 *عدد المقاعد المؤكدة:* {u_count}\n"
                    f"🏨 *ترتيبات الإقامة:* {u_hotel}\n\n"
                    f"🎫 **بطاقة صعود الح
