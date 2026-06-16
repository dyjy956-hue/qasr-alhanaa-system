

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

# دالة ذكية لإصدار صوت "بييب" النجاح عبر المتصفح فوراً عند مسح الباركود
def play_success_sound():
    sound_html = """
    <audio autoplay>
        <source src="https://assets.mixkit.co/active_storage/sfx/2568/2568-84.wav" type="audio/wav">
    </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

# 🧭 القائمة الجانبية الشاملة للأقسام التسعة الكاملة والمستقرة
st.sidebar.title("🏢 لوحة تحكم شركة قصر الهناء")
page = st.sidebar.radio("انتقل إلى القائمة:", [
    "💬 مركز مراسلة حالات الزبائن",
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

# تهيئة ذاكرة الحضور المؤقتة بناءً على "الاسم" بدلاً من الهاتف لمنع التداخل
if 'attended_names' not in st.session_state:
    st.session_state['attended_names'] = []
if 'just_attended_name' not in st.session_state:
    st.session_state['just_attended_name'] = None

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
                
                # تشفير اسم الزبون داخل الباركود ليكون فريداً
                encoded_name_for_qr = urllib.parse.quote(str(u_name).strip())
                qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_name_for_qr}"
                
                msg_confirm = f"""السلام عليكم ورحمة الله وبركاته،

مرحباً بك أخي/أختي الفاضلة المعزز في عائلة *شركة قصر الهناء للخدمات السياحية* 🌹

يسعدنا جداً إبلاغكم بأنه قد تم استلام بيانات التسجيل الخاصة بكم لرحلة (الجبل الأخضر الساحر 2026) بنجاح عبر المنظومة 📊✨

📌 *الاسم المسجل:* {u_name}
👥 *عدد أفراد العائلة:* {u_count} أشخاص
🏨 *محل الإقامة المختار:* {u_hotel}
📍 *مكان الانطلاق:* {u_reg}

💳 يرجى العلم أن الحجز يعتبر *مبدئياً* حتى يتم تأكيد السداد المالي (سواء نقداً في مقر الشركة أو عبر الحساب المصرفي)، وسيقوم موظف الحجوزات بالتواصل معكم لتمام الإجراءات.

*شكراً لثقتكم باختيار قصر الهناء، ونتمنى لكم رحلة ممتعة معنا مقدماً!* 🏔️ وبإذن الله رحلة مباركة للجميع."""

                msg_remind_pay = f"""مرحباً بك مجدداً وبكل عائلتك الكريمة مع شركة قصر الهناء 👋✨\n\n✅ تم تأكيد حجزكم بنجاح في #الرحلة_العائلية_للجبل_الاخضر 🏔️🚌\n\n💡 الخطوة المتبقية لتثبيت المقاعد نهائياً:\nيرجى التكرم بزيارة مقر الشركة لإتمام عملية الدفع وتأكيد الهوية.\n\n📍 عنوان الشركة: طرابلس - الظهرة.\n⏰ آخر موعد للاشتراك والدفع: الجمعة 26-06-2026.\n\n📌 ملاحظة: يرجى إحضار إثبات الهوية (الكتيب العائلي أو جوازات السفر) عند الحضور للمقر.\n\nنتطلع لرحلة ممتعة وصناعة ذكريات لا تُنسى معكم! دمت بخير وفي أمان الله 🌹\nشركة قصر الهناء للاستثمار السياحي."""

                msg_paid = f"""السلام عليكم ورحمة الله وبركاته،\n\nالأستاذ(ة) الفاضل(ة): *{u_name}* 🌟\n\nيسعدنا إبلاغكم بأنه **تم تأكيد السداد المالي بنجاح** وقبول حجزكم نهائياً لرحلة (الجبل الأخضر الساحر 2026) ✅💳\n\n👥 *عدد المقاعد المؤكدة:* {u_count}\n🏨 *ترتيبات الإقامة:* {u_hotel}\n\n🎫 **بطاقة صعود الحافلة الرقمية الخاصة بعائلتكم:**\nالرجاء الضغط على الرابط التالي وحفظ صورة الباركود (QR Code) لإبرازها للمشرف عند باب الحافلة يوم الرحلة:\n{qr_api_url}\n\nجاهزون لخدمتكم وصناعة أجمل الذكريات معاً! سيتم إرسال تفاصيل التجمع والانطلاق قبل الرحلة بـ 48 ساعة 🚌✨\n\n*شكراً لكم - إدارة شركة قصر الهناء* 🌹"""
                
                msg_tripoli_bus = f"""السلام عليكم ورحمة الله وبركاته،\n\nركابنا الأعزاء من مدينة طرابلس والمنطقة الغربية (رحلة الجبل الأخضر) 🚌🏔️\nنأمل أن تكونوا بكامل الاستعداد والنشاط لرحلتنا المتميزة مع شركة *قصر الهناء*.\n\nإليكم التفاصيل النهائية والخاصة بنقطة انطلاق باص طرابلس لرحلة الغد بمشيئة الله:\n📍 *مكان التجمع الدقيق:* [اكتب المكان هنا]\n⏰ *وقت التواجد وتنزيل الحقائب:* [الساعة]\n🚀 *وقت تحرك الحافلة الفعلي:* [الساعة] تماماً\n\n👤 *مشرف حافلة طرابلس:* [الاسم] -> [الهاتف]\n📞 *رقم هاتف السائق:* [الرقم]\n\n⚠️ *ملاحظات هامة جداً للرحلة:\n1. يرجى الالتزام التام والمطلق بوقت التجمع، نظراً لأن الحافلة مرتبطة بجدول زمني طويل لقطع المسافة، ولن نتمكن من الانتظار حفاظاً على راحة العائلات الحاضرة في الموعد.\n2. يرجى مراجعة مشرف الباص فور وصولكم لتأكيد الاسم واستلام ملصقات الحقائب الخاصة بالأمتعة.\n\n*رافقتكم السلامة في طريقكم، ونلتقي غداً على خير وبركة!* 🌹"""
                
                msg_cancel = f"""السلام عليكم ورحمة الله وبركاته،\n\nالأستاذ(ة): *{u_name}* 🌹\n\nنفيدكم بأنه بناءً على طلبكم (أو لعدم استكمال إجراءات التأكيد المالي)، **تم إلغاء تسجيلكم** لرحلة الجبل الأخضر 2026 بنجاح 🖥️❌\n\nنتمنى لكم التوفيق، ويسعدنا جداً خدمتكم وانضمامكم إلينا في الرحلات والمواسم القادمة بإذن الله.\n\n*شكراً لكم - شركة قصر الهناء للخدمات السياحية* 🏔️"""

                url_confirm = f"whatsapp://send?phone={phone_str}&text={urllib.parse.quote(msg_confirm)}"
                url_remind_pay = f"whatsapp://send?phone={phone_str}&text={urllib.parse.quote(msg_remind_pay)}"
                url_paid = f"whatsapp://send?phone={phone_str}&text={urllib.parse.quote(msg_paid)}"
                url_tripoli_bus = f"whatsapp://send?phone={phone_str}&text={urllib.parse.quote(msg_tripoli_bus)}"
                url_cancel = f"whatsapp://send?phone={phone_str}&text={urllib.parse.quote(msg_cancel)}"
                
                st.write("### 📲 خيارات المراسلة الفورية وحالات الزبون المختار:")
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1: st.markdown(f'<a href="{url_confirm}"><button style="background-color: #2b5c8f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🔵 1. تأكيد الحجز</button></a>', unsafe_allow_html=True)
                with col2: st.markdown(f'<a href="{url_remind_pay}"><button style="background-color: #1d3557; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🏁 2. التأكيد النهائي</button></a>', unsafe_allow_html=True)
                with col3: st.markdown(f'<a href="{url_paid}"><button style="background-color: #25D366; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🟢 3. السداد النهائي</button></a>', unsafe_allow_html=True)
                with col4:
                    if "الشرقية" not in u_reg:
                        st.markdown(f'<a href="{url_tripoli_bus}"><button style="background-color: #ff9800; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🚌 4. باص طرابلس</button></a>', unsafe_allow_html=True)
                    else:
                        st.button("🔒 4. ركاب الشرقية", disabled=True, help="هذا العميل تابع للمنطقة الشرقية.")
                with col5: st.markdown(f'<a href="{url_cancel}"><button style="background-color: #d32f2f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🔴 5. إلغاء الحجز</button></a>', unsafe_allow_html=True)

# ----------------------------------------------------
# 🔍 الصفحة الثانية: استعلام وبطاقة حجز عميل
# ----------------------------------------------------
elif page == "🔍 استعلام وبطاقة حجز عميل":
    st.title("🔍 نظام الاستعلام الفوري وعرض بيانات الحجز")
    st.subheader("ابحث باسم العميل لاستخراج بطاقة الحجز الفندقية واللوجستية الكاملة")
    st.markdown("---")
    
    if 'df' in st.session_state:
        df = st.session_state['df']
        col_name = next((c for c in df.columns if 'الاسم' in c or 'اسم' in c), None)
        col_price = next((c for c in df.columns if 'اجمالي التكلفة' in c or 'إجمالي التكلفة' in c or 'تكلفة' in c or 'التكلفة' in c or 'السعر' in c or 'اجمالي' in c), None)
        
        if col_name:
            search_user = st.selectbox("🎯 اختر أو اكتب اسم العميل للبحث السريع:", ["-- اختر اسماً لعرض تفاصيل حركته --"] + df[col_name].dropna().tolist())
            
            if search_user != "-- اختر اسماً لعرض تفاصيل حركته --":
                user_full_data = df[df[col_name] == search_user].iloc[0]
                u_price = user_full_data.get(col_price, 'غير محدد') if col_price else "غير محدد"
                
                u_display_name = user_full_data.get(col_name, 'غير مسجل')
                u_display_phone = str(user_full_data.get(next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c), 'الهاتف'), 'غير مسجل')).replace('.0','')
                u_display_count = user_full_data.get(next((c for c in df.columns if 'العدد' in c or 'أفراد' in c), 'العدد'), 'غير محدد')
                u_display_hotel = user_full_data.get(next((c for c in df.columns if 'الإقامة' in c or 'فندق' in c), 'الإقامة'), 'غير محدد')
                u_display_reg = user_full_data.get(next((c for c in df.columns if 'انطلاق' in c or 'مكان' in c), 'مكان الانطلاق'), 'غير محدد')

                # ✅ تم إدراج وتثبيت متغير السعر والتكلفة u_price بداخل البطاقة الرمادية ليعود للظهور بوضوح
                st.markdown(f"""
                <div style="background-color: #f8f9fa; border-right: 5px solid #1d3557; padding: 20px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                    <h3 style="color: #1d3557; margin-top: 0;">🎫 بطاقة البيانات التفصيلية للحجز</h3>
                    <hr style="margin: 10px 0;">
                    <p style="font-size: 16px;"><b>👤 اسم العميل بالكامل:</b> {u_display_name}</p>
                    <p style="font-size: 16px;"><b>📞 رقم الهاتف/الواتساب:</b> {u_display_phone}</p>
                    <p style="font-size: 16px;"><b>👥 عدد الأفراد المسجلين:</b> {u_display_count}</p>
                    <p style="font-size: 16px;"><b>🏨 الفندق / الإقامة:</b> {u_display_hotel}</p>
                    <p style="font-size: 16px;"><b>📍 محطة ونقطة الانطلاق:</b> {u_display_reg}</p>
                    <p style="font-size: 16px; color: #2e7d32;"><b>💰 سعر الحجز / القيمة المالية:</b> {u_price}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### 📄 الصف الكامل للبيانات كما ورد في الشيت:")
                st.dataframe(pd.DataFrame([user_full_data]), use_container_width=True)
        else:
            st.warning("⚠️ لم يتم العثور على عمود الاسم في ملف البيانات للبحث به.")

# ----------------------------------------------------
# 📋 الصفحة الثالثة: الكشف الكلي لجميع الركاب
# ----------------------------------------------------
elif page == "📋 الكشف الكلي لجميع الركاب":
    st.title("📋 الكشف الشامل والكلي لجميع ركاب الرحلة")
    st.subheader("عرض قاعدة البيانات الكاملة من السحابة دون أي استثناء")
    st.markdown("---")
    
    if 'df' in st.session_state:
        df = st.session_state['df']
        col_count = next((c for c in df.columns if 'العدد' in c or 'أفراد' in c or 'اشخاص' in c or 'عدد أفراد العائلة' in c), None)
        
        total_people = 0
        if col_count:
            total_people = int(pd.to_numeric(df[col_count], errors='coerce').sum())
            
        st.success(f"📊 إجمالي عدد حجوزات (العائلات): {df.shape[0]} عائلة | 👥 الإجمالي العام لعدد الركاب الفعليين: {total_people} شخص مسافر")
        st.dataframe(df, use_container_width=True)

# ----------------------------------------------------
# 🏢 الصفحة الرابعة: كشف نزلاء فندق قورينا
# ----------------------------------------------------
elif page == "🏢 كشف نزلاء فندق قورينا":
    st.title("🏢 كشف المسافرين المقيمين في فندق قورينا")
    st.subheader("تصفية تلقائية بناءً على خيار الإقامة الفندقية المختارة")
    st.markdown("---")
    
    if 'df' in st.session_state:
        df = st.session_state['df']
        col_hotel = next((c for c in df.columns if 'الإقامة' in c or 'فندق' in c or 'محل' in c), None)
        col_stay_count = next((c for c in df.columns if 'عدد افراد العائلة للمبييت' in c or 'عدد أفراد العائلة للمبيت' in c or 'للمبييت' in c or 'للمبيت' in c or 'العدد' in c), None)
        
        if col_hotel:
            df_quryna = df[df[col_hotel].astype(str).str.contains("قورينا")].copy()
            
            total_guests = 0
            if col_stay_count:
                total_guests = int(pd.to_numeric(df_quryna[col_stay_count], errors='coerce').sum())
                
            st.success(f"🏨 إجمالي عدد غرف/حجوزات فندق قورينا: {df_quryna.shape[0]} حجز | 👥 إجمالي عدد النزلاء الفعليين للمبيت: {total_guests} شخص")
            st.dataframe(df_quryna, use_container_width=True)
        else:
            st.warning("⚠️ لم يتم العثور على عمود الإقامة/الفندق في ملف البيانات لتصفية النزلاء.")

# ----------------------------------------------------
# 🌲 الصفحة الخامسة: كشف نزلاء منتجع شحات
# ----------------------------------------------------
elif page == "🌲 كشف نزلاء منتجع شحات":
    st.title("🌲 كشف المسافرين المقيمين في منتجع شحات السياحي")
    st.subheader("تصفية تلقائية بناءً على خيار الإقامة الفندقية المختارة")
    st.markdown("---")
    
    if 'df' in st.session_state:
        df = st.session_state['df']
        col_hotel = next((c for c in df.columns if 'الإقامة' in c or 'فندق' in c or 'محل' in c), None)
        col_stay_count = next((c for c in df.columns if 'عدد افراد العائلة للمبييت' in c or 'عدد أفراد العائلة للمبيت' in c or 'للمبييت' in c or 'للمبيت' in c or 'العدد' in c), None)
        
        if col_hotel:
            df_shahat = df[df[col_hotel].astype(str).str.contains("شحات")].copy()
            
            total_guests = 0
            if col_stay_count:
                total_guests = int(pd.to_numeric(df_shahat[col_stay_count], errors='coerce').sum())
                
            st.info(f"🏡 إجمالي عدد شاليهات/حجوزات منتجع شحات: {df_shahat.shape[0]} حجز | 👥 إجمالي عدد النزلاء الفعليين للمبيت: {total_guests} شخص")
            st.dataframe(df_shahat, use_container_width=True)
        else:
            st.warning("⚠️ لم يتم العثور على عمود الإقامة/الفندق في ملف البيانات لتصفية النزلاء.")

# ----------------------------------------------------
# 🟢 الصفحة السادسة: كشف ركاب طرابلس والغرب
# ----------------------------------------------------
elif page == "🟢 كشف ركاب طرابلس والغرب":
    st.title("🟢 كشف ركاب باص طرابلس والمنطقة الغربية")
    st.subheader("كشف المسافرين المستثنى منه ركاب المنطقة الشرقية")
    st.markdown("---")
    
    if 'df' in st.session_state:
        df = st.session_state['df']
        col_region = next((c for c in df.columns if 'انطلاق' in c or 'مكان' in c or 'تسجيل' in c), None)
        col_count = next((c for c in df.columns if 'العدد' in c or 'أفراد' in c or 'اشخاص' in c or 'عدد أفراد العائلة' in c), None)
        
        if col_region:
            df_tripoli = df[~df[col_region].astype(str).str.contains("الشرقية")].copy()
            
            tripoli_people = 0
            if col_count:
                tripoli_people = int(pd.to_numeric(df_tripoli[col_count], errors='coerce').sum())
                
            st.success(f"📊 إجمالي حجوزات طرابلس والغرب: {df_tripoli.shape[0]} عائلة | 👥 إجمالي عدد الركاب الفعليين: {tripoli_people} شخص")
            st.dataframe(df_tripoli, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

# ----------------------------------------------------
# 🔵 الصفحة السابعة: كشف ركاب المنطقة الشرقية
# ----------------------------------------------------
elif page == "🔵 كشف ركاب المنطقة الشرقية":
    st.title("🔵 كشف ركاب المنطقة الشرقية")
    st.subheader("كشف مخصص للمسافرين المسجلين من المنطقة الشرقية فقط")
    st.markdown("---")
    
    if 'df' in st.session_state:
        df = st.session_state['df']
        col_region = next((c for c in df.columns if 'انطلاق' in c or 'مكان' in c or 'تسجيل' in c), None)
        col_count = next((c for c in df.columns if 'العدد' in c or 'أفراد' in c or 'اشخاص' in c or 'عدد أفراد العائلة' in c), None)
        
        if col_region:
            df_east = df[df[col_region].astype(str).str.contains("الشرقية")].copy()
            
            east_people = 0
            if col_count:
                east_people = int(pd.to_numeric(df_east[col_count], errors='coerce').sum())
                
            st.info(f"📊 إجمالي حجوزات المنطقة الشرقية: {df_east.shape[0]} عائلة | 👥 إجمالي عدد الركاب الفعليين: {east_people} شخص")
            st.dataframe(df_east, use_container_width=True)
        else:
            st.warning("⚠️ لم يتم العثور على عمود المنطقة لتصفية ركاب الشرقية.")

# ----------------------------------------------------
# 💰 الصفحة الثامنة: التقارير المالية والإيرادات
# ----------------------------------------------------
elif page == "💰 التقارير المالية والإيرادات":
    st.title("💰 الإيرادات والتقارير المالية للشركة")
    st.subheader("متابعة المداخيل والحسابات لرحلة 2026")
    st.markdown("---")

    if 'df_finance' in st.session_state:
        df_finance = st.session_state['df_finance']
        st.write("### 📈 كشف الإيرادات والمصروفات الحالي:")
        st.dataframe(df_finance, use_container_width=True)
        st.info(f"💡 مجموع الأسطر المالية المسجلة حالياً: {df_finance.shape[0]} صفّاً.")
    else:
        st.warning("🔄 الرجاء الضغط على زر 'سحب وتحديث البيانات الشاملة' في القائمة الجانبية لسحب التقرير المالي.")

# ----------------------------------------------------
# 📲 الصفحة التاسعة: تسجيل حضور العائلات بالباركود
# ----------------------------------------------------
elif page == "📲 تسجيل حضور العائلات بالباركود":
    st.title("📲 نظام مسح الباركود الذكي وتثبيت الحضور الفوري")
    st.subheader("لوحة حية مخصصة لمشرف الحافلة لإدارة ركوب العائلات")
    st.markdown("---")
    
    if 'df' in st.session_state:
        df = st.session_state['df']
        
        col_name = next((c for c in df.columns if 'الاسم' in c or 'اسم' in c), None)
        col_phone = next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c or 'موبايل' in c), None)
        col_count = next((c for c in df.columns if 'العدد' in c or 'أفراد' in c or 'اشخاص' in c), None)
        col_region = next((c for c in df.columns if 'انطلاق' in c or 'مكان' in c or 'تسجيل' in c), None)
        
        if col_name and col_phone:
            df['clean_name'] = df[col_name].astype(str).str.strip()
            all_valid_names = df['clean_name'].tolist()
            
            st.session_state['attended_names'] = [n for n in st.session_state['attended_names'] if n in all_valid_names]
            
            df_attended = df[df['clean_name'].isin(st.session_state['attended_names'])].copy()
            df_missing = df[~df['clean_name'].isin(st.session_state['attended_names'])].copy()
            
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("👥 إجمالي العائلات بالرحلة", len(df))
            with c2: st.metric("🟢 عائلات تم تسجيل حضورها", len(df_attended))
            with c3: st.metric("🔴 عائلات متبقية ومتأخرة", len(df_missing))
                
            st.markdown("---")
            
            scan_mode = st.radio("🛠️ اختر طريقة تسجيل صعود العائلة:", ["✏️ تسجيل يدوي سريع (اسم / هاتف)", "📸 استخدام كاميرا الباركود"])
            
            scanned_name = None
            
            if scan_mode == "📸 استخدام كاميرا الباركود":
                st.write("### 📸 وجه كاميرا الموبايل نحو باركود العائلة:")
                img_file = st.camera_input("اضغط لالتقاط صورة الباركود ومسحه")
                
                if img_file is not None:
                    try:
                        import cv2
                        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
                        opencv_img = cv2.imdecode(file_bytes, 1)
                        gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
                        detector = cv2.QRCodeDetector()
                        data, bbox, straight_qrcode = detector.detectAndDecode(gray)
                        
                        if data and str(data).strip() in all_valid_names:
                            scanned_name = str(data).strip()
                        else:
                            data, bbox, straight_qrcode = detector.detectAndDecode(opencv_img)
                            if data and str(data).strip() in all_valid_names:
                                scanned_name = str(data).strip()
                            else:
                                st.warning("🔄 لم يتم التقاط رمز الباركود بوضوح. الرجاء استخدام خيار 'التسجيل اليدوي السريع'.")
                    except Exception as e:
                        st.error("تنبيه الحساب السحابي: يرجى تفعيل 'التسجيل اليدوي السريع' لإتمام العمل فوراً بنجاح.")
            
            else:
                st.write("### ✏️ اختر اسم العائلة المتواجدة أمامك الآن لتسجيلها:")
                missing_list = ["-- اختر اسم العائلة من القائمة لتسجيل حضورها فوراً --"] + df_missing[col_name].dropna().tolist()
                selected_missing = st.selectbox("قائمة العائلات المتأخرة:", missing_list)
                
                if selected_missing != "-- اختر اسم العائلة من القائمة لتسجيل حضورها فوراً --":
                    potential_name = str(selected_missing).strip()
                    if potential_name in all_valid_names:
                        scanned_name = potential_name
            
            if scanned_name and scanned_name in all_valid_names:
                if scanned_name in st.session_state['attended_names'] and scanned_name != st.session_state['just_attended_name']:
                    st.warning(f"⚠️ تنبيه: العائلة باسم ({scanned_name}) تم تسجيل حضورها وصعودها مسبقاً الحافلة!")
                elif scanned_name not in st.session_state['attended_names']:
                    st.session_state['attended_names'].append(scanned_name)
                    st.session_state['just_attended_name'] = scanned_name
                    play_success_sound()
                    st.rerun()

            if st.session_state['just_attended_name']:
                active_name = st.session_state['just_attended_name']
                user_row = df[df['clean_name'] == active_name]
                
                if not user_row.empty:
                    family_name = user_row.iloc[0][col_name]
                    fam_count = user_row.iloc[0][col_count] if col_count else "غير محدد"
                    u_phone_val = user_row.iloc[0][col_phone]
                    phone_for_msg = str(u_phone_val).replace('.0','') if '.' in str(u_phone_val) else str(u_phone_val)
                    
                    st.success("✅ تم تأكيد صعود العائلة وتثبيتها في الكشوفات بنجاح!")
                    st.markdown(f"""
                    <div style="background-color: #e8f5e9; border-right: 5px solid #2e7d32; padding: 15px; border-radius: 5px;">
                        <h4 style="color: #2e7d32; margin: 0;">📋 حالة الصعود الحالية:</h4>
                        <p style="margin: 5px 0; font-size: 16px;"><b>اسم العائلة:</b> {family_name} | <b>عدد الأفراد:</b> {fam_count} أشخاص</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    msg_welcome = f"تم تسجيل صعود عائلتكم الكريمة إلى الحافلة بنجاح! 🚌✨\n\nشركة قصر الهناء تتمنى لكم رحلة سعيدة وممتعة إلى الجبل الأخضر. رافقتكم السلامة 🌹"
                    url_welcome = f"whatsapp://send?phone={phone_for_msg}&text={urllib.parse.quote(msg_welcome)}"
                    
                    col_btn1, col_btn2 = st.columns([3, 1])
                    with col_btn1:
                        st.markdown(f'<a href="{url_welcome}"><button style="background-color: #2e7d32; color: white; border: none; padding: 14px 10px; border-radius: 6px; font-size: 14px; cursor: pointer; font-weight: bold; width: 100%;">📲 إرسال رسالة الترحيب الفورية للراكب عبر واتساب</button></a>', unsafe_allow_html=True)
                    with col_btn2:
                        if st.button("🔄 جاهز للباركود التالي"):
                            st.session_state['just_attended_name'] = None
                            st.rerun()
                else:
                    st.error("⚠️ هذا الاسم غير مسجل في كشوفات هذه الرحلة.")
            
            st.markdown("---")
            
            col_tab1, col_tab2 = st.tabs(["🔴 العائلات المتبقية (لم تصل بعد)", "🟢 العائلات التي صعدت الحافلة"])
            
            with col_tab1:
                if not df_missing.empty:
                    st.write("📋 **اضغط على زر التنبيه بجانب اسم العائلة لإعلامهم ببدء صعود الحافلة فوراً:**")
                    for idx, row in df_missing.iterrows():
                        m_name = row[col_name]
                        m_phone_val = row[col_phone]
                        m_count = row[col_count] if col_count else "غير محدد"
                        m_reg = row[col_region] if col_region else ""
                        
                        phone_alert_str = str(m_phone_val).replace('.0','') if '.' in str(m_phone_val) else str(m_phone_val)
                        
                        msg_alert = f"مرحباً يا أستاذ {m_name}، نحن الآن في مرحلة صعود حافلة قصر الهناء والانطلاق قريب جداً بمشيئة الله 🚌.\n\nيرجى التكرم بالتوجه نحو الحافلة وإبراز الباركود للمشرف لتسجيل حضوركم وصعودكم. ننتظركم بكل حب 🌹"
                        url_alert = f"whatsapp://send?phone={phone_alert_str}&text={urllib.parse.quote(msg_alert)}"
                        
                        sub_c1, sub_c2 = st.columns([4, 1])
                        with sub_c1:
                            st.markdown(f"👤 **{m_name}** ({m_count} أشخاص) - محطة: {m_reg}")
                        with sub_c2:
                            st.markdown(f'<a href="{url_alert}"><button style="background-color: #d32f2f; color: white; border: none; padding: 5px 8px; border-radius: 4px; font-size: 11px; cursor: pointer; width: 100%;">🔔 تنبيه بالصعود</button></a>', unsafe_allow_html=True)
                else:
                    st.success("🎉 رائـع! اكتمل حضور جميع العائلات بنجاح، الحافلة جاهزة للانطلاق.")
                    
            with col_tab2:
                if not df_attended.empty:
                    st.dataframe(df_attended, use_container_width=True)
                else:
                    st.info("ℹ️ لم يتم تسجيل صعود أي عائلة بعد.")
        else:
            st.warning("⚠️ يرجى التأكد من مطابقة أسماء أعمدة الشيت (الاسم والهاتف) لتفعيل نظام الباركود.")
