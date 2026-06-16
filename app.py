

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# ====================================================
# 🔒 نظام الحماية والأمان المطور (تم تعديل الباسورد الدائم)
# ====================================================
# تعيين الباسورد الافتراضي الثابت عند إقلاع السيرفر
if 'master_password' not in st.session_state:
    st.session_state['master_password'] = "Samir2026"

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🔒 نظام تسجيل الدخول - شركة قصر الهناء")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3064/3064155.png", width=150)
    with col2:
        st.write("### مرحباً بك في لوحة تحكم الإدارة")
        user_password = st.text_input("الرجاء إدخال كلمة مرور المنظومة للدخول:", type="password")
        
        if st.button("🔓 تسجيل الدخول"):
            if user_password == st.session_state['master_password']:
                st.session_state['authenticated'] = True
                st.success("تم التحقق بنجاح! جاري تحميل المنظومة...")
                st.rerun()
            else:
                st.error("❌ كلمة المرور غير صحيحة، يرجى إعادة المحاولة.")
    st.stop()

# ====================================================
# 🚌 بداية المنظومة الأصلية بعد تخطي جدار الحماية
# ====================================================

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
    keep_cols = [c for c in df_to_export.columns if any(k in c for k in ['الاسم', 'الهاتف', 'رقم', 'العدد', 'أفراد', 'الإقامة', 'فندق', 'انطلاق', 'مكان'])]
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

# دالة لإنشاء رابط الواتساب المباشر للتطبيق
def get_wa_intent(phone, text):
    encoded_text = urllib.parse.quote(text)
    return f"intent://send?phone={phone}&text={encoded_text}#Intent;scheme=smsto;package=com.whatsapp;action=android.intent.action.SENDTO;end"

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

st.sidebar.markdown("---")

# 🛠️ مربع تغيير الباسورد الذكي داخل السايدبار
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
# زر خروج آمن للموظف في القائمة الجانبية
if st.sidebar.button("🔒 تسجيل الخروج الآمن", use_container_width=True):
    st.session_state['authenticated'] = False
    st.rerun()

if st.sidebar.button("🔄 سحب وتحديث البيانات الشاملة", use_container_width=True):
    try:
        st.session_state['df'] = load_data_public('Form responses 1')
        st.session_state['df_finance'] = load_data_public('📊 التقرير المالي والإيرادات')
        st.sidebar.success("تم تحديث كافة البيانات المالية والحجوزات!")
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

إليكم التفاصيل النهائية والخاصة بنقطة انطلاق
