

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse
import numpy as np

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

# تهيئة ذاكرة الحضور المؤقتة ليوم الرحلة حتى لا تضيع القوائم عند التنقل
if 'attended_phones' not in st.session_state:
    st.session_state['attended_phones'] = []

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
            st.warning("⚠️ للمراسلة: تأكد من وجود عمود يحتوي على 'الاسم' وعمود يحتوي على 'رقم الهاتف' in الشيت.")
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
                    f"🎫 **بطاقة صعود الحافلة الرقمية الخاصة بعائلتكم:**\n"
                    f"الرجاء الضغط على الرابط التالي وحفظ صورة الباركود (QR Code) لإبرازها للمشرف عند باب الحافلة يوم الرحلة:\n"
                    f"{qr_api_url}\n\n"
                    f"جاهزون لخدمتكم وصناعة أجمل الذكريات معاً! سيتم إرسال تفاصيل التجمع والانطلاق قبل الرحلة بـ 48 ساعة 🚌✨\n\n"
                    f"*شكراً لكم - إدارة شركة قصر الهناء* 🌹"
                )
                
                msg_tripoli_bus = (
                    f"السلام عليكم ورحمة الله وبركاته،\n\n"
                    f"ركابنا الأعزاء من مدينة طرابلس والمنطقة الغربية (رحلة الجبل الأخضر) 🚌🏔️\n"
                    f"نأمل أن تكونوا بكامل الاستعداد والنشاط لرحلتنا المتميزة مع شركة *قصر الهناء*.\n\n"
                    f"إليكم التفاصيل النهائية والخاصة بنقطة انطلاق باص طرابلس لرحلة الغد بمشيئة الله:\n"
                    f"📍 *مكان التجمع الدقيق:* [اكتب المكان هنا]\n"
                    f"⏰ *وقت التواجد وتنزيل الحقائب:* [الساعة]\n"
                    f"🚀 *وقت تحرك الحافلة الفعلي:* [الساعة] تماماً\n\n"
                    f"👤 *مشرف حافلة طرابلس:* [الاسم] -> [الهاتف]\n"
                    f"📞 *رقم هاتف السائق:* [الرقم]\n\n"
                    f"⚠️ *ملاحظات هامة جداً للرحلة:*\n"
                    f"1. يرجى الالتزام التام والمطلق بوقت التجمع، نظراً لأن الحافلة مرتبطة بجدول زمني طويل لقطع المسافة، ولن نتمكن من الانتظار حفاظاً على راحة العائلات الحاضرة في الموعد.\n"
                    f"2. يرجى مراجعة مشرف الباص فور وصولكم لتأكيد الاسم واستلام ملصقات الحقائب الخاصة بالأمتعة.\n\n"
                    f"*رافقتكم السلامة في طريقكم، ونلتقي غداً على خير وبركة!* 🌹"
                )
                
                msg_cancel = (
                    f"السلام عليكم ورحمة الله وبركاته،\n\n"
                    f"الأستاذ(ة): *{u_name}* 🌹\n\n"
                    f"نفيدكم بأنه بناءً على طلبكم (أو لعدم استكمال إجراءات التأكيد المالي)، **تم إلغاء تسجيلكم** لرحلة الجبل الأخضر 2026 بنجاح 🖥️❌\n\n"
                    f"نتمنى لكم التوفيق، ويسعدنا جداً خدمتكم وانضمامكم إلينا في الرحلات والمواسم القادمة بإذن الله.\n\n"
                    f"*شكراً لكم - شركة قصر الهناء للخدمات السياحية* 🏔️"
                )

                url_confirm = f"whatsapp://send?phone={phone_str}&text={urllib.parse.quote(msg_confirm)}"
                url_remind_pay = f"whatsapp://send?phone={phone_str}&text={urllib.parse.quote(msg_remind_pay)}"
                url_paid = f"whatsapp://send?phone={phone_str}&text={urllib.parse.quote(msg_paid)}"
                url_tripoli_bus = f"whatsapp://send?phone={phone_str}&text={urllib.parse.quote(msg_tripoli_bus)}"
                url_cancel = f"whatsapp://send?phone={phone_str}&text={urllib.parse.quote(msg_cancel)}"
                
                st.write("### 📲 خيارات المراسلة الفورية وحالات الزبون المختار:")
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1: st.markdown(f'<a href="{url_confirm}"><button style="background-color: #2b5c8f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🔵 1. استلام الطلب</button></a>', unsafe_allow_html=True)
                with col2: st.markdown(f'<a href="{url_remind_pay}"><button style="background-color: #1d3557; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🏁 2. تأكيد المقر والدفع</button></a>', unsafe_allow_html=True)
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
        
        if col_name:
            search_user = st.selectbox("🎯 اختر أو اكتب اسم العميل للبحث السريع:", ["-- اختر اسماً لعرض تفاصيل حركته --"] + df[col_name].dropna().tolist())
            
            if search_user != "-- اختر اسماً لعرض تفاصيل حركته --":
                user_full_data = df[df[col_name] == search_user].iloc[0]
                
                st.markdown(f"""
                <div style="background-color: #f8f9fa; border-right: 5px solid #1d3557; padding: 20px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                    <h3 style="color: #1d3557; margin-top: 0;">🎫 بطاقة البيانات التفصيلية للحجز</h3>
                    <hr style="margin: 10px 0;">
                    <p style="font-size: 16px;"><b>👤 اسم العميل بالكامل:</b> {user_full_data.get(col_name, 'غير مسجل')}</p>
                    <p style="font-size: 16px;"><b>📞 رقم الهاتف/الواتساب:</b> {str(user_full_data.get(next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c), 'الهاتف'), 'غير مسجل')).replace('.0','')}</p>
                    <p style="font-size: 16px;"><b>👥 عدد الأفراد المسجلين:</b> {user_full_data.get(next((c for c in df.columns if 'العدد' in c or 'أفراد' in c), 'العدد'), 'غير محدد')}</p>
                    <p style="font-size: 16px;"><b>🏨 الفندق / الإقامة:</b> {user_full_data.get(next((c for c in df.columns if 'الإقامة' in c or 'فندق' in c), 'الإقامة'), 'غير محدد')}</p>
                    <p style="font-size: 16px;"><b>📍 محطة ونقطة الانطلاق:</b> {user_full_data.get(next((c for c in df.columns if 'انطلاق' in c or 'مكان' in c), 'مكان الانطلاق'), 'غير محدد')}</p>
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
        st.success(f"📊 العدد الإجمالي الكلي لكافة المسافرين المسجلين في المنظومة: {df.shape[0]} مسافر")
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
        
        if col_hotel:
            df_quryna = df[df[col_hotel].astype(str).str.contains("قورينا")].copy()
            st.success(f"🏨 إجمالي عدد نزلاء فندق قورينا حالياً: {df_quryna.shape[0]} مسافر")
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
        
        if col_hotel:
            df_shahat = df[df[col_hotel].astype(str).str.contains("شحات")].copy()
            st.info(f"🏡 إجمالي عدد نزلاء منتجع شحات حالياً: {df_shahat.shape[0]} مسافر")
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
        
        if col_region:
            df_tripoli = df[~df[col_region].astype(str).str.contains("الشرقية")].copy()
            st.success(f"📊 إجمالي ركاب طرابلس والغرب المقيدين حالياً: {df_tripoli.shape[0]} مسافر")
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
        
        if col_region:
            df_east = df[df[col_region].astype(str).str.contains("الشرقية")].copy()
            st.info(f"📊 إجمالي ركاب المنطقة الشرقية المقيدين حالياً: {df_east.shape[0]} مسافر")
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
            df['clean_phone'] = df[col_phone].astype(str).str.replace('.0', '', regex=False).str.strip()
            
            df_attended = df[df['clean_phone'].isin(st.session_state['attended_phones'])].copy()
            df_missing = df[~df['clean_phone'].isin(st.session_state['attended_phones'])].copy()
            
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("👥 إجمالي العائلات بالرحلة", len(df))
            with c2: st.metric("🟢 عائلات تم تسجيل حضورها", len(df_attended))
            with c3: st.metric("🔴 عائلات متبقية ومتأخرة", len(df_missing))
                
            st.markdown("---")
            
            # حماية الكود من الانهيار والاعتماد الكلي على التسجيل اليدوي كخيار أول أمن ومجرب
            scan_mode = st.radio("🛠️ اختر طريقة تسجيل صعود العائلة:", ["✏️ تسجيل يدوي سريع (اسم / هاتف)", "📸 استخدام كاميرا الباركود"])
            
            scanned_phone = None
            
            if scan_mode == "📸 استخدام كاميرا الباركود":
                st.write("### 📸 وجه كاميرا الموبايل نحو باركود العائلة:")
                img_file = st.camera_input("اضغط لالتقاط صورة الباركود ومسحه")
                
                if img_file is not None:
                    try:
                        # استيراد المكتبة هنا بشكل محلي ومحمي لمنع توقف التطبيق
                        import cv2
                        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
                        opencv_img = cv2.imdecode(file_bytes, 1)
                        
                        gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
                        detector = cv2.QRCodeDetector()
                        data, bbox, straight_qrcode = detector.detectAndDecode(gray)
                        
                        if data:
                            scanned_phone = str(data).strip()
                        else:
                            data, bbox, straight_qrcode = detector.detectAndDecode(opencv_img)
                            if data:
                                scanned_phone = str(data).strip()
                            else:
                                st.warning("🔄 لم يتم التقاط رمز الباركود بوضوح. يرجى ضبط الإضاءة، أو استخدم خيار 'التسجيل اليدوي السريع' فوراً لتوفير الوقت.")
                    except Exception as e:
                        st.error(f"تنبيه: الكاميرا تحتاج لتثبيت حزم إضافية على السيرفر. يرجى استخدام 'التسجيل اليدوي السريع' الآن لتسير أعمالكم بنجاح.")
            
            else:
                st.write("### ✏️ اختر اسم العائلة المتواجدة أمامك الآن لتسجيلها:")
                missing_list = ["-- اختر اسم العائلة من القائمة لتسجيل حضورها فوراً --"] + df_missing[col_name].dropna().tolist()
                selected_missing = st.selectbox("قائمة العائلات المتأخرة:", missing_list)
                
                if selected_missing != "-- اختر اسم العائلة من القائمة لتسجيل حضورها فوراً --":
                    user_row_manual = df[df[col_name] == selected_missing]
                    if not user_row_manual.empty:
                        scanned_phone = user_row_manual.iloc[0]['clean_phone']
            
            if scanned_phone:
                user_row = df[df['clean_phone'] == scanned_phone]
                
                if not user_row.empty:
                    family_name = user_row.iloc[0][col_name]
                    fam_count = user_row.iloc[0][col_count] if col_count else "غير محدد"
                    
                    st.success(f"✅ تم تحديد العائلة بنجاح!")
                    st.markdown(f"""
                    <div style="background-color: #e8f5e9; border-right: 5px solid #2e7d32; padding: 15px; border-radius: 5px;">
                        <h4 style="color: #2e7d32; margin: 0;">📋 حالة الصعود الحالية:</h4>
                        <p style="margin: 5px 0; font-size: 16px;"><b>اسم العائلة:</b> {family_name} | <b>عدد الأفراد:</b> {fam_count} أشخاص</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    msg_welcome = f"تم تسجيل صعود عائلتكم الكريمة إلى الحافلة بنجاح! 🚌✨\n\nشركة قصر الهناء تتمنى لكم رحلة سعيدة وممتعة إلى الجبل الأخضر. رافقتكم السلامة 🌹"
                    url_welcome = f"whatsapp://send?phone={scanned_phone}&text={urllib.parse.quote(msg_welcome)}"
                    
                    if st.markdown(f'<a href="{url_welcome}"><button style="background-color: #2e7d32; color: white; border: none; padding: 14px 10px; border-radius: 6px; font-size: 14px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 10px;">📲 اضغط هنا لتأكيد الصعود وإرسال رسالة الواتساب للراكب</button></a>', unsafe_allow_html=True):
                        if scanned_phone not in st.session_state['attended_phones']:
                            st.session_state['attended_phones'].append(scanned_phone)
                            st.rerun()
                else:
                    st.error("⚠️ هذا الرقم غير مسجل في كشوفات هذه الرحلة.")
            
            st.markdown("---")
            
            col_tab1, col_tab2 = st.tabs(["🔴 العائلات المتبقية (لم تصل بعد)", "🟢 العائلات التي صعدت الحافلة"])
            
            with col_tab1:
                if not df_missing.empty:
                    st.write("📋 **اضغط على زر التنبيه بجانب اسم العائلة لإعلامهم ببدء صعود الحافلة فوراً:**")
                    for idx, row in df_missing.iterrows():
                        m_name = row[col_name]
                        m_phone = row['clean_phone']
                        m_count = row[col_count] if col_count else "غير محدد"
                        m_reg = row[col_region] if col_region else ""
                        
                        msg_alert = f"مرحباً يا أستاذ {m_name}، نحن الآن في مرحلة صعود حافلة قصر الهناء والانطلاق قريب جداً بمشيئة الله 🚌.\n\nيرجى التكرم بالتوجه نحو الحافلة وإبراز الباركود للمشرف لتسجيل حضوركم وصعودكم. ننتظركم بكل حب 🌹"
                        url_alert = f"whatsapp://send?phone={m_phone}&text={urllib.parse.quote(msg_alert)}"
                        
                        sub_c1, sub_c2 = st.columns([4, 1])
                        with sub_c1:
                            st.markdown(f"👤 **{m_name}** ({m_count} أشخاص) - محطة: {m_reg}")
                        with sub_c2:
                            st.markdown(f'<a href="{url_alert}"><button style="background-color: #d32f2f; color: white; border: none; padding: 5px 8px; border-radius: 4px; font-size: 11px; cursor: pointer; width: 100%;">🔔 تنبيه بالصعود</button></a>', unsafe_allow_html=True)
                else:
                    st.success("🎉 رائـع! اكتمل حضور جميع العائلات بنجاح، الحافلة جاهزة للانطلاق.")
                    
            with col_tab2:
                if not df_attended.empty:
                    show_cols = [col_name]
                    if col_count: show_cols.append(col_count)
                    if col_region: show_cols.append(col_region)
                    st.dataframe(df_attended[show_cols], use_container_width=True)
                else:
                    st.info("ℹ️ لم يتم تسجيل صعود أي عائلة بعد.")
        else:
            st.warning("⚠️ يرجى التأكد من مطابقة أسماء أعمدة الشيت (الاسم والهاتف) لتفعيل نظام الباركود.")
