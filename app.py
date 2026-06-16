

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
            st.warning("⚠️ للمراسلة: تأكد من وجود عمود الاسم والهاتف في كشف البيانات.")
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
🚀 *وقت تحرك الحافلة الفعلي:* [الساعة] تماماً

👤 *مشرف حافلة طرابلس:* [الاسم] -> [الهاتف]
📞 *رقم هاتف السائق:* [الرقم]

⚠️ *ملاحظات هامة جداً للرحلة:*
1. يرجى الالتزام التام والمطلق بوقت التجمع، نظراً لأن الحافلة مرتبطة بجدول زمني طويل لقطع المسافة، ولن نتمكن من الانتظار حفاظاً على راحة العائلات الحاضرة في الموعد.
2. يرجى مراجعة مشرف الباص فور وصولكم لتأكيد الاسم واستلام ملصقات الحقائب الخاصة بالأمتعة.

*رافقتكم السلامة في طريقكم، ونلتقي غداً على خير وبركة!* 🌹"""

                    msg_cancel = f"""السلام عليكم ورحمة الله وبركاته،

الأستاذ(ة): *{u_name}* 🌹

نفيدكم بأنه بناءً على طلبكم (أو لعدم استكمال إجراءات التأكيد المالي)، **تم إلغاء تسجيلكم** لرحلة الجبل الأخضر 2026 بنجاح 🖥️❌

نتمنى لكم التوفيق، ويسعدنا جداً خدمتكم وانضمامكم إلينا في الرحلات والمواسم القادمة بإذن الله.

*شكراً لكم - شركة قصر الهناء للخدمات السياحية* 🏔️"""

                    url_confirm = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_confirm)}"
                    url_remind_pay = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_remind_pay)}"
                    url_paid = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_paid)}"
                    url_tripoli_bus = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_tripoli_bus)}"
                    url_cancel = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_cancel)}"
                    
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1: st.markdown(f'<a href="{url_confirm}" target="_blank"><button style="background-color: #2b5c8f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; width: 100%;">🔵 1. استلام الطلب</button></a>', unsafe_allow_html=True)
                    with col2: st.markdown(f'<a href="{url_remind_pay}" target="_blank"><button style="background-color: #1d3557; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; width: 100%;">🏁 2. تأكيد المقر</button></a>', unsafe_allow_html=True)
                    with col3: st.markdown(f'<a href="{url_paid}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; width: 100%;">🟢 3. السداد النهائي</button></a>', unsafe_allow_html=True)
                    with col4: st.markdown(f'<a href="{url_tripoli_bus}" target="_blank"><button style="background-color: #ff9800; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; width: 100%;">🚌 4. باص طرابلس</button></a>', unsafe_allow_html=True)
                    with col5: st.markdown(f'<a href="{url_cancel}" target="_blank"><button style="background-color: #d32f2f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; width: 100%;">🔴 5. إلغاء الحجز</button></a>', unsafe_allow_html=True)

            # --- التبويب الثاني: المنطقة الشرقية ---
            with tab_east:
                st.write(f"### 📊 ركاب المنطقة الشرقية ({df_east.shape[0]} مسافر):")
                st.dataframe(df_east, use_container_width=True)
                
                selected_user_e = st.selectbox("اختر اسم الزبون (المنطقة الشرقية):", ["-- اختر اسماً --"] + df_east[col_name].dropna().tolist(), key="east_select")
                if selected_user_e != "-- اختر اسماً --":
                    user_data = df_east[df_east[col_name] == selected_user_e].iloc[0]
                    u_name = user_data[col_name]
                    u_phone = user_data[col_phone]
                    u_count = user_data[col_count] if col_count else "غير محدد"
                    u_hotel = user_data[col_hotel] if col_hotel else "غير محدد"
                    u_reg = str(user_data[col_region]) if col_region else ""
                    phone_str = str(u_phone).replace('.0','') if '.' in str(u_phone) else str(u_phone)
                    
                    msg_confirm_e = f"""السلام عليكم ورحمة الله وبركاته،

مرحباً بك في عائلة *شركة قصر الهناء للخدمات السياحية* 🌹

تم استلام بيانات تسجيلكم لرحلة (الجبل الأخضر الساحر 2026) بنجاح عبر المنظومة 📊✨

📌 *
