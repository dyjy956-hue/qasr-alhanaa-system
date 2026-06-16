

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

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

# دالة هندسية بديلة ومضمونة 100% لتصدير كشوفات Excel مرتبة وأنيقة وتفتح في كل مكان
def convert_df_to_excel(df_to_export):
    keep_cols = [c for c in df_to_export.columns if any(k in c for k in ['الاسم', 'الهاتف', 'رقم', 'العدد', 'أفراد', 'الإقامة', 'فندق', 'انطلاق', 'مكان'])]
    if not keep_cols:
        keep_cols = df_to_export.columns[:5]
    
    df_clean = df_to_export[keep_cols].copy()
    df_clean.insert(0, '#', range(1, len(df_clean) + 1))
    
    output = BytesIO()
    # استخدام التنسيق الافتراضي المضمون في سيرفرات streamlit سريعة التشغيل
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_clean.to_excel(writer, index=False, sheet_name='الكشف الرسمي')
    return output.getvalue()

def display_styled_dataframe(dataframe):
    df_display = dataframe.copy()
    df_display.insert(0, '#', range(1, len(df_display) + 1))
    st.dataframe(df_display.set_index('#'), use_container_width=True)

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

if st.sidebar.button("🔄 سحب وتحديث البيانات الشاملة"):
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

👥 *عدد المقاعد المؤاعد المؤكدة:* {u_count}
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
                
                st.write("### 📲 خيارات المراسلة الفورية وحالات الزبون المختار:")
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1: st.markdown(f'<a href="{url_confirm}" target="_blank"><button style="background-color: #2b5c8f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🔵 1. استلام الطلب</button></a>', unsafe_allow_html=True)
                with col2: st.markdown(f'<a href="{url_remind_pay}" target="_blank"><button style="background-color: #1d3557; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🏁 2. تأكيد المقر والدفع</button></a>', unsafe_allow_html=True)
                with col3: st.markdown(f'<a href="{url_paid}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🟢 3. السداد النهائي</button></a>', unsafe_allow_html=True)
                with col4:
                    if "الشرقية" not in u_reg:
                        st.markdown(f'<a href="{url_tripoli_bus}" target="_blank"><button style="background-color: #ff9800; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🚌 4. باص طرابلس</button></a>', unsafe_allow_html=True)
                    else:
                        st.button("🔒 4. ركاب الشرقية", disabled=True, help="هذا العميل تابع للمنطقة الشرقية.")
                with col5: st.markdown(f'<a href="{url_cancel}" target="_blank"><button style="background-color: #d32f2f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🔴 5. إلغاء الحجز</button></a>', unsafe_allow_html=True)

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
        else:
            st.warning("⚠️ لم يتم العثور على عمود الاسم في ملف البيانات.")

# ----------------------------------------------------
# 📋 الصفحة الثالثة: الكشف الكلي لجميع الركاب + زر Excel
# ----------------------------------------------------
elif page == "📋 الكشف الكلي لجميع الركاب":
    st.title("📋 الكشف الشامل والكلي لجميع ركاب الرحلة")
    st.markdown("---")
    if 'df' in st.session_state:
        df = st.session_state['df']
        st.success(f"📊 العدد الإجمالي الكلي لكافة المسافرين المسجلين في المنظومة: {df.shape[0]} مسافر")
        
        # زر إكسيل الفخم الجديد المضمون سحابياً
        excel_data = convert_df_to_excel(df)
        st.download_button("📥 تحميل الكشف العام كاملاً كملف Excel للمنظومة", data=excel_data, file_name="Total_Trip_Passengers
