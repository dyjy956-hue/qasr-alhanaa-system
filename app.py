

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
            
            # 1. نص رسالة التأكيد المبدئي
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
            
            # 2. نص رسالة التذكير بالدفع والسداد
            msg_remind_pay = (
                f"السلام عليكم ورحمة الله وبركاته،\n\n"
                f"الأستاذ(ة) الفاضل(ة): *{u_name}* 🌹\n\n"
                f"نود تذكيركم بلطف بأن مقاعدكم لرحلة (الجبل الأخضر الساحر 2026) ما زالت محجوزة حجزاً مؤقتاً باسمكم 🚌⏰\n\n"
                f"⚠️ ونظراً للإقبال الكبير واقتراب موعد إغلاق الكشوفات، يرجى استكمال إجراءات **السداد المالي لتأكيد الحجز نهائياً** خلال 48 ساعة لتجنب إلغاء المقاعد تلقائياً.\n\n"
                f"💳 طرق السداد المتاحة:\n"
                f"- نقداً أو صك في مقر الشركة.\n"
                f"- تحويل مصرفي.\n\n"
                f"يسعدنا جداً أن تكونوا معنا في رحلة العمر! للاستفسار أو التأكيد تواصلوا معنا مباشرة 📞"
            )
            
            # 3. نص رسالة تأكيد السداد المالي النهائي
            msg_paid = (
                f"السلام عليكم ورحمة الله وبركاته،\n\n"
                f"الأستاذ(ة) الفاضل(ة): *{u_name}* 🌟\n\n"
                f"يسعدنا إبلاغكم بأنه **تم تأكيد السداد المالي بنجاح** وقبول حجزكم نهائياً لرحلة (الجبل الأخضر الساحر 2026) ✅💳\n\n"
                f"👥 *عدد المقاعد المؤكدة:* {u_count}\n"
                f"🏨 *ترتيبات الإقامة:* {u_hotel}\n\n"
                f"جاهزون لخدمتكم وصناعة أجمل الذكريات معاً! سيتم إرسال تفاصيل التجمع والانطلاق قبل الرحلة بـ 48 ساعة 🚌✨\n\n"
                f"*شكراً لكم - إدارة شركة قصر الهناء* 🌹"
            )
            
            # 4. نص رسالة باص طرابلس وركاب الغرب (التي أرسلتها بالملّي)
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
            
            # 5. نص رسالة الإلغاء
            msg_cancel = (
                f"السلام عليكم ورحمة الله وبركاته،\n\n"
                f"الأستاذ(ة): *{u_name}* 🌹\n\n"
                f"نفيدكم بأنه بناءً على طلبكم (أو لعدم استكمال إجراءات التأكيد المالي)، **تم إلغاء تسجيلكم** لرحلة الجبل الأخضر 2026 بنجاح 🖥️❌\n\n"
                f"نتمنى لكم التوفيق، ويسعدنا جداً خدمتكم وانضمامكم إلينا في الرحلات والمواسم القادمة بإذن الله.\n\n"
                f"*شكراً لكم - شركة قصر الهناء للخدمات السياحية* 🏔️"
            )

            # توليد الروابط المشفرة
            url_confirm = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_confirm)}"
            url_remind_pay = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_remind_pay)}"
            url_paid = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_paid)}"
            url_tripoli_bus = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_tripoli_bus)}"
            url_cancel = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_cancel)}"
            
            # عرض الأزرار الخمسة متناسقة وموزعة بالألوان
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown(f'<a href="{url_confirm}" target="_blank"><button style="background-color: #2b5c8f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🔵 1. حجز مبدئي</button></a>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<a href="{url_remind_pay}" target="_blank"><button style="background-color: #1d3557; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🔷 2. تذكير بالدفع</button></a>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<a href="{url_paid}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🟢 3. تأكيد المال</button></a>', unsafe_allow_html=True)
            with col4:
                # ميزة ذكية: يظهر الزر البرتقالي مخصصاً لركاب طرابلس والغرب فقط بناءً على نص المعادلة السابقة لحظر الشرقية
                if "الشرقية" not in u_reg:
                    st.markdown(f'<a href="{url_tripoli_bus}" target="_blank"><button style="background-color: #ff9800; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🚌 4. باص طرابلس</button></a>', unsafe_allow_html=True)
                else:
                    st.button("🔒 4. ركاب الشرقية", disabled=True, help="هذا العميل تابع للمنطقة الشرقية وليس باص طرابلس.")
            with col5:
                st.markdown(f'<a href="{url_cancel}" target="_blank"><button style="background-color: #d32f2f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🔴 5. إلغاء الحجز</button></a>', unsafe_allow_html=True)
