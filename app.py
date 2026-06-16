

# تعليق لحماية السطر الأول من المسافات التلقائية
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

# 🧭 القائمة الجانبية الشاملة للأقسام الثمانية
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
                
                # تأمين كافة النصوص بالتنصيص الثلاثي الآمن لضمان عدم الانقطاع
                msg_confirm = f"""السلام عليكم ورحمة الله وبركاته،

مرحباً بك أخي/أختي الفاضلة المعزز في عائلة *شركة قصر الهناء للخدمات السياحية* 🌹

يسعدنا جداً إبلاغكم بأنه قد تم استلام بيانات التسجيل الخاصة بكم لرحلة (الجبل الأخضر الساحر 2026) بنجاح عبر المنظومة 📊✨

📌 *الاسم المسجل:* {u_name}
👥 *عدد أفراد العائلة:* {u_count} أشخاص
🏨 *محل الإقامة المختار:* {u_hotel}
📍 *مكان الانطلاق:* {u_reg}

💳 يرجى العلم أن الحجز يعتبر *مبدئياً* حتى يتم تأكيد السداد المالي (سواء نقداً في مقر الشركة أو عبر الحساب المصرفي)، وسيقوم موظف الحجوزات بالتواصل معكم لتمام الإجراءات.

*شكراً لثقتكم باختيار قصر الهناء، ونتمنى لكم رحلة ممتعة معنا مقدماً!* 🏔️ وبإذن الله رحلة مباركة للجميع."""

                msg_remind_pay = f"""مرحباً بك مجدداً وبكل عائلتك الكريمة مع شركة قصر الهناء 👋✨

✅ تم تأكيد حجزكم بنجاح في #الرحلة_العائلية_للجبل_الاخضر 🏔️🚌

💡 الخطوة المتبقية لتثبيت المقاعد نهائياً:
يرجى التكرم بزيارة مقر الشركة لإتمام عملية الدفع وتأكيد الهوية.

📍 عنوان الشركة: طرابلس - الظهرة.
⏰ آخر موعد للاشتراك والدفع: الجمعة 26-06-2026.

📌 ملاحظة: يرجى إحضار إثبات الهوية (الكتيب العائلي أو جوازات السفر) عند الحضور للمقر.

نتطلع لرحلة ممتعة وصناعة ذكريات لا تُنسى معكم! دمت بخير وفي أمان الله 🌹
شركة قصر الهناء للاستثمار السياحي."""

                msg_paid = f"""السلام عليكم ورحمة الله وبركاته،

الأستاذ(ة) الفاضل(ة): *{u_name}* 🌟

يسعدنا إبلاغكم بأنه **تم تأكيد السداد المالي بنجاح** وقبول حجزكم نهائياً لرحلة (الجبل الأخضر الساحر 2026) ✅💳

👥 *عدد المقاعد المؤكدة:* {u_count}
🏨 *ترتيبات الإقامة:* {u_hotel}

جاهزون لخدمتكم وصناعة أجمل الذكريات معاً! سيتم إرسال تفاصيل التجمع والانطلاق قبل الرحلة بـ 48 ساعة 🚌✨

*شكراً لكم - إدارة شركة قصر الهناء* 🌹"""

                msg_tripoli_bus = f"""السلام عليكم ورحمة الله وبركاته،

ركابنا الأعزاء من مدينة طرابلس والمنطقة الغربية (رحلة الجبل الأخضر) 🚌🏔️
نأمل أن تكونوا بكامل الاستعداد والنشاط لرحلتنا المتميزة مع شركة *قصر الهناء*.

إليكم التفاصيل النهائية والخاصة بنقطة انطلاق باص طرابلس لرحلة الغد بمشيئة الله:
📍 *مكان التجمع الدقيق:* [اكتب المكان هنا]
⏰ *وقت التواجد وتنزيل الحقائب:* [الساعة]
🚀 *وقت تحرك الحافلة الفعلي:*
