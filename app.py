

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# دالة سحب البيانات ديناميكياً حسب اسم التبويب
def load_data_from_sheet(sheet_name):
    SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'
    encoded_sheet = urllib.parse.quote(sheet_name)
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

# 🧭 القائمة الجانبية للتنقل داخل المنظومة
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

        if col_region:
            region = st.selectbox(f"تصفية سريعة حسب {col_region}:", ["الكل"] + list(df[col_region].dropna().unique()))
            if region != "الكل":
                df_filtered = df[df[col_region] == region]
            else:
                df_filtered = df.copy()
        else:
            df_filtered = df.copy()
            
        st.write("### 📊 كشف البيانات الشامل:")
        st.dataframe(df_filtered, use_container_width=True)
        st.markdown("---")
        
        if not col_name or not col_phone:
            st.warning("⚠️ للمراسلة: تأكد من وجود عمود يحتوي على 'الاسم' وعمود يحتوي على 'رقم الهاتف' في الشيت.")
        else:
            st.write("### 💬 مركز المراسلات الذكي وحالات الزبائن:")
            selected_user = st.selectbox("اختر اسم الزبون المراد مراسلته:", df_filtered[col_name].dropna().tolist())
            
            if selected_user:
                user_data = df_filtered[df_filtered[col_name] == selected_user].iloc[0]
                
                u_name = user_data[col_name]
                u_phone = user_data[col_phone]
                u_count = user_data[col_count] if col_count else "غير محدد"
                u_hotel = user_data[col_hotel] if col_hotel else "غير محدد"
                u_reg = str(user_data[col_region]) if col_region else ""
                
                phone_str = str(u_phone).replace('.0','') if '.' in str(u_phone) else str(u_phone)
                
                msg_confirm = f"السلام عليكم ورحمة الله وبركاته،\n\nمرحباً بك في عائلة *شركة قصر الهناء للخدمات السياحية* 🌹\n\nتم استلام بيانات تسجيلكم لرحلة (الجبل الأخضر الساحر 2026) بنجاح عبر المنظومة 📊✨\n\n📌 *الاسم:* {u_name}\n👥 *العدد:* {u_count} أشخاص\n🏨 *الإقامة:* {u_hotel}\n📍 *مكان الانطلاق:* {u_reg}\n\n💳 يعتبر الحجز مبدئياً حتى تأكيد السداد المالي.\n\n*شكراً لثقتكم باختيار قصر الهناء!* 🏔️"
                msg_remind_pay = f"مرحباً بك مجدداً وبكل عائلتك الكريمة مع شركة قصر الهناء 👋✨\n\n✅ تم تأكيد حجزكم بنجاح في #الرحلة_العائلية_للجبل_الاخضر 🏔️🚌\n\n💡 الخطوة المتبقية لتثبيت المقاعد نهائياً:\nيرجى التكرم بزيارة مقر الشركة لإتمام عملية الدفع وتأكيد الهوية.\n\n📍 عنوان الشركة: طرابلس - الظهرة.\n⏰ آخر موعد للاشتراك والدفع: الجمعة 26-06-2026.\n\n📌 ملاحظة: يرجى إحضار إثبات الهوية (الكتيب العائلي أو جوازات السفر) عند الحضور للمقر.\n\nنتطلع لرحلة ممتعة وصناعة ذكريات لا تُنسى معكم! دمت بخير وفي أمان الله 🌹\nشركة قصر الهناء للاستثمار السياحي."
                msg_paid = f"السلام عليكم ورحمة الله وبركاته،\n\nالأستاذ(ة) الفاضل(ة): *{u_name}* 🌟\n\nيسعدنا إبلاغكم بأنه **تم تأكيد السداد المالي بنجاح** وقبول حجزكم نهائياً لرحلة (الجبل الأخضر الساحر 2026) ✅💳\n\n👥 *عدد المقاعد المؤكدة:* {u_count}\n🏨 *ترتيبات الإقامة:* {u_hotel}\n\nجاهزون لخدمتكم وصناعة أجمل الذكريات معاً! سيتم إرسال تفاصيل التجمع والانطلاق قبل الرحلة بـ 48 ساعت 🚌✨\n\n*شكراً لكم - إدارة شركة قصر الهناء* 🌹"
                msg_tripoli_bus = f"السلام عليكم ورحمة الله وبركاته،\n\nركابنا الأعزاء من مدينة طرابلس والمنطقة الغربية (رحلة الجبل الأخضر) 🚌🏔️\nنأمل أن تكونوا بكامل الاستعداد والنشاط لرحلتنا المتميزة مع شركة *قصر الهناء*.\n\nإليكم التفاصيل النهائية والخاصة بنقطة انطلاق باص طرابلس لرحلة الغد بمشيئة الله:\n📍 *مكان التجمع الدقيق:* [اكتب المكان هنا]\n⏰ *وقت التواجد وتنزيل الحقائب:* [الساعة]\n🚀 *وقت تحرك الحافلة الفعلي:* [الساعة] تماماً\n\n👤 *مشرف حافلة طرابلس:* [الاسم] -> [الهاتف]\n📞 *رقم هاتف السائق:* [الرقم]\n\n⚠️ *ملاحظات هامة جداً للرحلة:*\n1. يرجى الالتزام التام والمطلق بوقت التجمع، نظراً لأن الحافلة مرتبطة بجدول زمني طويل لقطع المسافة، ولن نتمكن من الانتظار حفاظاً على راحة العائلات الحاضرة في الموعد.\n2. يرجى مراجعة مشرف الباص فور وصولكم لتأكيد الاسم واستلام ملصقات الحقائب الخاصة بالأمتعة.\n\n*رافقتكم السلامة في طريقكم، ونلتقي غداً على خير وبركة!* 🌹"
                msg_cancel = f"السلام عليكم ورحمة الله وبركاته،\n\nالأستاذ(ة): *{u_name}* 🌹\n\nنفيدكم بأنه بناءً على طلبكم (أو لعدم استكمال إجراءات التأكيد المالي)، **تم إلغاء تسجيلكم** لرحلة الجبل الأخضر 2026 بنجاح 🖥️❌\n\nنتمنى لكم التوفيق، ويسعدنا جداً خدمتكم وانضمامكم إلينا في الرحلات والمواسم القادمة بإذن الله.\n\n*شكراً لكم - شركة قصر الهناء للخدمات السياحية* 🏔️"

                url_confirm = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_confirm)}"
                url_remind_pay = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_remind_pay)}"
                url_paid = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_paid)}"
                url_tripoli_bus = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_tripoli_bus)}"
                url_cancel = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_cancel)}"
                
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.markdown(f'<a href="{url_confirm}" target="_blank"><button style="background-color: #2b5c8f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🔵 1. استلام الطلب</button></a>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<a href="{url_remind_pay}" target="_blank"><button style="background-color: #1d3557; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🏁 2. تأكيد المقر</button></a>', unsafe_allow_html=True)
                with col3:
                    st.markdown(f'<a href="{url_paid}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🟢 3. السداد النهائي</button></a>', unsafe_allow_html=True)
                with col4:
                    if "الشرقية" not in u_reg:
                        st.markdown(f'<a href="{url_tripoli_bus}" target="_blank"><button style="background-color: #ff9800; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🚌 4. باص طرابلس</button></a>', unsafe_allow_html=True)
                    else:
                        st.button("🔒 4. ركاب الشرقية", disabled=True)
                with col5:
                    st.markdown(f'<a href="{url_cancel}" target="_blank"><button style="background-color: #d32f2f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🔴 5. إلغاء الحجز</button></a>', unsafe_allow_html=True)

# ----------------------------------------------------
# 📊 الصفحة الثانية: التقارير المالية والإيرادات
# ----------------------------------------------------
elif page == "💰 التقارير المالية والإيرادات":
    st.title("💰 الإيرادات والتقارير المالية للشركة")
    st.subheader("متابعة المداخيل والحسابات لرحلة 2026")
    
    if st.button("🔄 سحب وتحديث البيانات المالية من السحابة"):
        try:
            st.session_state['df_finance'] = load_data_from_sheet('📊 التقرير المالي والإيرادات')
            st.success("تم سحب وتحديث البيانات المالية الحية بنجاح!")
        except Exception as e:
            st.error(f"تأكد من وجود ورقة '📊 التقرير المالي والإيرادات' وإذن مشاركتها: {e}")

    if 'df_finance' in st.session_state:
        df_finance = st.session_state['df_finance']
        
        # عرض الجداول المالية بالكامل المأخوذة من الشيت
        st.write("### 📈 كشف الإيرادات والمصروفات الحالي:")
        st.dataframe(df_finance, use_container_width=True)
        
        # ميزة إضافية مريحة لإظهار إجمالي الصفوف والأعمدة
        st.info(f"💡 مجموع الأسطر المالية المسجلة حالياً: {df_finance.shape[0]} صفّاً.")
