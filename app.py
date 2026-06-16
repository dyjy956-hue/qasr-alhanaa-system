

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# ====================================================
# 🔒 نظام الحماية والأمان المطور (تم تعديل الباسورد الدائم)
# ====================================================
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

# 🧭 القائمة الجانبية
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
            df_filtered = df[df[col_region] == region] if region != "الكل" else df.copy()
        else:
            df_filtered = df.copy()
            
        if not col_name or not col_phone:
            st.warning("⚠️ للمراسلة: تأكد من وجود عمود يحتوي على 'الاسم' وعمود يحتوي على 'رقم الهاتف' في الشيت.")
        else:
            selected_user = st.selectbox("اختر اسم الزبون المراد مراسلته عبر الواتساب:", df_filtered[col_name].dropna().tolist())
            
            if selected_user:
                user_data = df_filtered[df_filtered[col_name] == selected_user].iloc[0]
                u_name = user_data[col_name]
                u_phone = str(user_data[col_phone]).replace('.0','') if '.' in str(user_data[col_phone]) else str(user_data[col_phone])
                u_count = user_data[col_count] if col_count else "غير محدد"
                u_hotel = user_data[col_hotel] if col_hotel else "غير محدد"
                u_reg = str(user_data[col_region]) if col_region else ""
                
                msg_confirm = f"السلام عليكم ورحمة الله وبركاته،\n\nمرحباً بك في عائلة *شركة قصر الهناء للخدمات السياحية* 🌹\n\nتم استلام بيانات تسجيلكم لرحلة (الجبل الأخضر الساحر 2026) بنجاح عبر المنظومة 📊✨\n\n📌 *الاسم:* {u_name}\n👥 *العدد:* {u_count} أشخاص\n🏨 *الإقامة:* {u_hotel}\n📍 *مكان الانطلاق:* {u_reg}\n\n💳 يعتبر الحجز مبدئياً حتى تأكيد السداد المالي.\n\n*شكراً لثقتكم باختيار قصر الهناء!* 🏔️"
                msg_remind_pay = f"مرحباً بك مجدداً وبكل عائلتك الكريمة مع شركة قصر الهناء 👋✨\n\n✅ تم تأكيد حجزكم بنجاح في #الرحلة_العائلية_للجبل_الاخضر 🏔️🚌\n\n💡 الخطوة المتبقية لتثبيت المقاعد نهائياً: يرجى التكرم بزيارة مقر الشركة لإتمام عملية الدفع.\n\n📍 عنوان الشركة: طرابلس - الظهرة.\n⏰ آخر موعد للاشتراك والدفع: الجمعة 26-06-2026.\n\nنتطلع لرحلة ممتعة معكم! دمت بخير وفي أمان الله 🌹\nشركة قصر الهناء للاستثمار السياحي."
                msg_paid = f"السلام عليكم ورحمة الله وبركاته،\n\nالأستاذ(ة) الفاضل(ة): *{u_name}* 🌟\n\nيسعدنا إبلاغكم بأنه **تم تأكيد السداد المالي بنجاح** وقبول حجزكم نهائياً لرحلة (الجبل الأخضر الساحر 2026) ✅💳\n\n👥 *عدد المقاعد المؤكدة:* {u_count}\n🏨 *ترتيبات الإقامة:* {u_hotel}\n\nجاهزون لخدمتكم وصناعة أجمل الذكريات معاً! 🚌✨\n\n*شكراً لكم - إدارة شركة قصر الهناء* 🌹"
                
                msg_tripoli_bus = (
                    "السلام عليكم ورحمة الله وبركاته،\n\n"
                    "ركابنا الأعزاء من مدينة طرابلس والمنطقة الغربية (رحلة الجبل الأخضر) 🚌🏔️\n"
                    "نأمل أن تكونوا بكامل الاستعداد والنشاط لرحلتنا المتميزة مع شركة *قصر الهناء*.\n\n"
                    "إليكم التفاصيل النهائية لنقطة انطلاق باص طرابلس لرحلة الغد بمشيئة الله:\n"
                    "📍 *مكان التجمع الدقيق:* [اكتب المكان هنا]\n"
                    "⏰ *وقت التواجد وتنزيل الحقائب:* [الساعة]\n"
                    "🚀 *وقت تحرك الحافلة الفعلي:* [الساعة] تماماً\n\n"
                    f"👤 *مشرف حافلة طرابلس:* [الاسم] -> [الهاتف]\n"
                    "📞 *رقم هاتف السائق:* [الرقم]\n\n"
                    "*رافقتكم السلامة في طريقكم، ونلتقي غداً على خير وبركة!* 🌹"
                )
                
                msg_cancel = f"السلام عليكم ورحمة الله وبركاته،\n\nالأستاذ(ة): *{u_name}* 🌹\n\nنفيدكم بأنه بناءً على طلبكم، **تم إلغاء تسجيلكم** لرحلة الجبل الأخضر 2026 بنجاح 🖥️❌\n\nنتمنى لكم التوفيق ويسعدنا خدمتكم في الرحلات القادمة بإذن الله.\n\n*شكراً لكم - شركة قصر الهناء للخدمات السياحية* 🏔️"

                url_confirm = get_wa_intent(u_phone, msg_confirm)
                url_remind_pay = get_wa_intent(u_phone, msg_remind_pay)
                url_paid = get_wa_intent(u_phone, msg_paid)
                url_tripoli_bus = get_wa_intent(u_phone, msg_tripoli_bus)
                url_cancel = get_wa_intent(u_phone, msg_cancel)
                
                st.write("### 📲 خيارات المراسلة الفورية وحالات الزبون المختار:")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1: st.markdown(f'<a href="{url_confirm}" target="_blank"><button style="background-color: #2b5c8f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-weight: bold; width: 100%;">🔵 1. استلام</button></a>', unsafe_allow_html=True)
                with col2: st.markdown(f'<a href="{url_remind_pay}" target="_blank"><button style="background-color: #1d3557; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-weight: bold; width: 100%;">🏁 2. تأكيد</button></a>', unsafe_allow_html=True)
                with col3: st.markdown(f'<a href="{url_paid}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-weight: bold; width: 100%;">🟢 3. سداد</button></a>', unsafe_allow_html=True)
                with col4:
                    if "الشرقية" not in u_reg:
                        st.markdown(f'<a href="{url_tripoli_bus}" target="_blank"><button style="background-color: #ff9800; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-weight: bold; width: 100%;">🚌 4. باص</button></a>', unsafe_allow_html=True)
                    else: st.button("🔒 4. مغلق", disabled=True)
                with col5: st.markdown(f'<a href="{url_cancel}" target="_blank"><button style="background-color: #d32f2f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-weight: bold; width: 100%;">🔴 5. إلغاء</button></a>', unsafe_allow_html=True)

# 🔍 باقي الصفحات (نفس منطقك الأصلي)
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
                st.markdown(f"""<div style="background-color: #f8f9fa; border-right: 5px solid #1d3557; padding: 20px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);"><h3>🎫 بطاقة البيانات التفصيلية للحجز</h3><hr><p><b>👤 اسم العميل:</b> {user_full_data.get(col_name, 'غير مسجل')}</p></div>""", unsafe_allow_html=True)

elif page == "📋 الكشف الكلي لجميع الركاب":
    st.title("📋 الكشف الشامل والكلي لجميع ركاب الرحلة")
    st.markdown("---")
    if 'df' in st.session_state:
        display_styled_dataframe(st.session_state['df'])

elif page == "🏢 كشف نزلاء فندق قورينا":
    if 'df' in st.session_state: display_styled_dataframe(st.session_state['df'][st.session_state['df'].astype(str).apply(lambda x: x.str.contains("قورينا")).any(axis=1)])

elif page == "🌲 كشف نزلاء منتجع شحات":
    if 'df' in st.session_state: display_styled_dataframe(st.session_state['df'][st.session_state['df'].astype(str).apply(lambda x: x.str.contains("شحات")).any(axis=1)])

elif page == "🟢 كشف ركاب طرابلس والغرب":
    if 'df' in st.session_state: display_styled_dataframe(st.session_state['df'][~st.session_state['df'].astype(str).apply(lambda x: x.str.contains("الشرقية")).any(axis=1)])

elif page == "🔵 كشف ركاب المنطقة الشرقية":
    if 'df' in st.session_state: display_styled_dataframe(st.session_state['df'][st.session_state['df'].astype(str).apply(lambda x: x.str.contains("الشرقية")).any(axis=1)])

elif page == "💰 التقارير المالية والإيرادات":
    if 'df_finance' in st.session_state: st.dataframe(st.session_state['df_finance'], use_container_width=True)
