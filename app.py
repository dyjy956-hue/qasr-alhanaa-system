

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# ====================================================
# 🔒 نظام الحماية والأمان المطور (Samir2026)
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
# 🚌 بداية المنظومة الأصلية
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

def convert_df_to_excel(df_to_export, sheet_name_text='الكشف الرسمي'):
    keep_cols = [c for c in df_to_export.columns if any(k in c for k in ['الاسم', 'الهاتف', 'رقم', 'العدد', 'أفراد', 'الإقامة', 'فندق', 'انطلاق', 'مكان'])]
    if not keep_cols:
        keep_cols = df_to_export.columns
    
    df_clean = df_to_export[keep_cols].copy()
    if '#' not in df_clean.columns and len(df_clean) > 0:
        df_clean.insert(0, '#', range(1, len(df_clean) + 1))
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_clean.to_excel(writer, index=False, sheet_name=sheet_name_text)
    return output.getvalue()

def display_styled_dataframe(dataframe):
    df_display = dataframe.copy()
    if '#' not in df_display.columns:
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

st.sidebar.markdown("---")

# 🛠️ مربع تغيير الباسورد داخل السايدبار
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
# 💬 الصفحات اللوجستية (1-7)
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
            st.warning("⚠️ للمراسلة: تأكد من وجود عمود الاسم والهاتف.")
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
                
                msg_confirm = f"""السلام عليكم ورحمة الله وبركاته،\n\nمرحباً بك في عائلة *شركة قصر الهناء للخدمات السياحية* 🌹\n\nتم استلام بيانات تسجيلكم لرحلة (الجبل الأخضر الساحر 2026) بنجاح عبر المنظومة 📊✨\n\n📌 *الاسم:* {u_name}\n👥 *العدد:* {u_count} أشخاص\n🏨 *الإقامة:* {u_hotel}\n📍 *مكان الانطلاق:* {u_reg}\n\n💳 يعتبر الحجز مبدئياً حتى تأكيد السداد المالي.\n\n*شكراً لثقتكم باختيار قصر الهناء!* 🏔️"""
                msg_remind_pay = f"""مرحباً بك مجدداً وبكل عائلتك الكريمة مع شركة قصر الهناء 👋✨\n\n✅ تم تأكيد حجزكم بنجاح في #الرحلة_العائلية_للجبل_الاخضر 🏔️🚌\n\n💡 الخطوة المتبقية لتثبيت المقاعد نهائياً:\nيرجى التكرم بزيارة مقر الشركة لإتمام عملية الدفع وتأكيد الهوية.\n\n📍 عنوان الشركة: طرابلس - الظهرة.\n⏰ آخر موعد للاشتراك والدفع: الجمعة 26-06-2026.\n\n📌 ملاحظة: يرجى إحضار إثبات الهوية (الكتيب العائلي أو جوازات السفر) عند الحضور للمقر.\n\nنتطلع لرحلة ممتعة وصناعة ذكريات لا تُنسى معكم! دمت بخير وفي أمان الله 🌹\nشركة قصر الهناء للاستثمار السياحي."""
                msg_paid = f"""السلام عليكم ورحمة الله وبركاته،\n\nالأستاذ(ة) الفاضل(ة): *{u_name}* 🌟\n\nيسعدنا إبلاغكم بأنه **تم تأكيد السداد المالي بنجاح** وقبول حجزكم نهائياً لرحلة (الجبل الأخضر الساحر 2026) ✅💳\n\n👥 *عدد المقاعد المؤكدة:* {u_count}\n🏨 *ترتيبات الإقامة:* {u_hotel}\n\nجاهزون لخدمتكم وصناعة أجمل الذكريات معاً! سيتم إرسال تفاصيل التجمع والانطلاق قبل الرحلة بـ 48 ساعة 🚌✨\n\n*شكراً لكم - إدارة شركة قصر الهناء* 🌹"""
                msg_tripoli_bus = f"""السلام عليكم ورحمة الله وبركاته،\n\nركابنا الأعزاء من مدينة طرابلس والمنطقة الغربية (رحلة الجبل الأخضر) 🚌🏔\nنأمل أن تكونوا بكامل الاستعداد والنشاط لرحلتنا المتميزة مع شركة *قصر الهناء*.\n\nإليكم التفاصيل النهائية والخاصة بنقطة انطلاق باص طرابلس لرحلة الغد بمشيئة الله:\n📍 *مكان التجمع الدقيق:* [اكتب المكان هنا]\n⏰ *وقت التواجد وتنزيل الحقائب:* [الساعة]\n🚀 *وقت تحرك الحافلة الفعلي:* [الساعة] تماماً\n\n👤 *مشرف حافلة طرابلس:* [الاسم] -> [الهاتف]\n📞 *رقم هاتف السائق:* [الرقم]\n\n⚠️ *ملاحظات هامة جداً للرحلة:*\n1. يرجى الالتزام التام والمطلق بوقت التجمع.\n2. يرجى مراجعة مشرف الباص فور وصولكم.\n\n*رافقتكم السلامة في طريقكم، ونلتقي غداً على خير وبركة!* 🌹"""
                msg_cancel = f"""السلام عليكم ورحمة الله وبركاته،\n\nالأستاذ(ة): *{u_name}* 🌹\n\nنفيدكم بأنه بناءً على طلبكم، **تم إلغاء تسجيلكم** لرحلة الجبل الأخضر 2026 بنجاح 🖥❌\n\nشكراً لكم - شركة قصر الهناء"""

                url_confirm = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_confirm)}"
                url_remind_pay = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_remind_pay)}"
                url_paid = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_paid)}"
                url_tripoli_bus = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_tripoli_bus)}"
                url_cancel = f"https://wa.me/{phone_str}?text={urllib.parse.quote(msg_cancel)}"
                
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1: st.markdown(f'<a href="{url_confirm}" target="_blank"><button style="background-color: #2b5c8f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🔵 1. استلام الطلب</button></a>', unsafe_allow_html=True)
                with col2: st.markdown(f'<a href="{url_remind_pay}" target="_blank"><button style="background-color: #1d3557; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🏁 2. تأكيد المقر والدفع</button></a>', unsafe_allow_html=True)
                with col3: st.markdown(f'<a href="{url_paid}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🟢 3. السداد النهائي</button></a>', unsafe_allow_html=True)
                with col4:
                    if "الشرقية" not in u_reg: st.markdown(f'<a href="{url_tripoli_bus}" target="_blank"><button style="background-color: #ff9800; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🚌 4. باص طرابلس</button></a>', unsafe_allow_html=True)
                    else: st.button("🔒 4. ركاب الشرقية", disabled=True)
                with col5: st.markdown(f'<a href="{url_cancel}" target="_blank"><button style="background-color: #d32f2f; color: white; border: none; padding: 12px 5px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: bold; width: 100%;">🔴 5. إلغاء الحجز</button></a>', unsafe_allow_html=True)

elif page == "🔍 استعلام وبطاقة حجز عميل":
    st.title("🔍 نظام الاستعلام الفوري وعرض بيانات الحجز")
    if 'df' in st.session_state:
        df = st.session_state['df']
        col_name = next((c for c in df.columns if 'الاسم' in c or 'اسم' in c), None)
        if col_name:
            search_user = st.selectbox("🎯 اختر أو اكتب اسم العميل للبحث السريع:", ["-- اختر اسماً --"] + df[col_name].dropna().tolist())
            if search_user != "-- اختر اسماً --":
                user_full_data = df[df[col_name] == search_user].iloc[0]
                st.markdown(f"""<div style="background-color: #f8f9fa; border-right: 5px solid #1d3557; padding: 20px; border-radius: 8px;"><h3 style="color: #1d3557; margin-top: 0;">🎫 بطاقة بيانات الحجز</h3><hr><p><b>👤 اسم العميل:</b> {user_full_data.get(col_name)}</p><p><b>📞 الهاتف:</b> {str(user_full_data.get(next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c), 'الهاتف'))).replace('.0','')}</p><p><b>🏨 الإقامة:</b> {user_full_data.get(next((c for c in df.columns if 'الإقامة' in c or 'فندق' in c), 'الإقامة'))}</p></div>""", unsafe_allow_html=True)

elif page == "📋 الكشف الكلي لجميع الركاب":
    st.title("📋 الكشف الشامل والكلي لجميع ركاب الرحلة")
    if 'df' in st.session_state:
        df = st.session_state['df']
        st.success(f"📊 إجمالي ركاب المنظومة: {df.shape[0]} مسافر")
        st.download_button("📥 تحميل الكشف العام كاملاً كملف Excel", data=convert_df_to_excel(df, 'الكشف العام'), file_name="Total_Passengers.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        display_styled_dataframe(df)

elif page == "🏢 كشف نزلاء فندق قورينا":
    st.title("🏢 كشف المسافرين المقيمين في فندق قورينا")
    if 'df' in st.session_state:
        df = st.session_state['df']
        col_hotel = next((c for c in df.columns if 'الإقامة' in c or 'فندق' in c), None)
        if col_hotel:
            df_quryna = df[df[col_hotel].astype(str).str.contains("قورينا")].copy()
            st.success(f"🏨 نزلاء قورينا: {df_quryna.shape[0]} مسافر")
            st.download_button("📥 تحميل كشف فندق قورينا كملف Excel", data=convert_df_to_excel(df_quryna, 'نزلاء قورينا'), file_name="Quryna_Guests.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            display_styled_dataframe(df_quryna)

elif page == "🌲 كشف نزلاء منتجع شحات":
    st.title("🌲 كشف المسافرين المقيمين في منتجع شحات السياحي")
    if 'df' in st.session_state:
        df = st.session_state['df']
        col_hotel = next((c for c in df.columns if 'الإقامة' in c or 'فندق' in c), None)
        if col_hotel:
            df_shahat = df[df[col_hotel].astype(str).str.contains("شحات")].copy()
            st.info(f"🏡 نزلاء شحات: {df_shahat.shape[0]} مسافر")
            st.download_button("📥 تحميل كشف منتجع شحات كملف Excel", data=convert_df_to_excel(df_shahat, 'نزلاء شحات'), file_name="Shahat_Guests.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            display_styled_dataframe(df_shahat)

elif page == "🟢 كشف ركاب طرابلس والغرب":
    st.title("🟢 كشف ركاب باص طرابلس والمنطقة الغربية")
    if 'df' in st.session_state:
        df = st.session_state['df']
        col_region = next((c for c in df.columns if 'انطلاق' in c or 'مكان' in c), None)
        if col_region:
            df_tripoli = df[~df[col_region].astype(str).str.contains("الشرقية")].copy()
            st.success(f"🚌 ركاب طرابلس والغرب: {df_tripoli.shape[0]} مسافر")
            st.download_button("📥 تحميل كشف باص طرابلس كملف Excel", data=convert_df_to_excel(df_tripoli, 'ركاب الغرب'), file_name="Tripoli_Bus.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            display_styled_dataframe(df_tripoli)

elif page == "🔵 كشف ركاب المنطقة الشرقية":
    st.title("🔵 كشف ركاب المنطقة الشرقية")
    if 'df' in st.session_state:
        df = st.session_state['df']
        col_region = next((c for c in df.columns if 'انطلاق' in c or 'مكان' in c), None)
        if col_region:
            df_east = df[df[col_region].astype(str).str.contains("الشرقية")].copy()
            st.info(f"📊 ركاب الشرقية: {df_east.shape[0]} مسافر")
            st.download_button("📥 تحميل كشف ركاب الشرقية كملف Excel", data=convert_df_to_excel(df_east, 'ركاب الشرقية'), file_name="Eastern_Passengers.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            display_styled_dataframe(df_east)

# ----------------------------------------------------
# 💰 الصفحة الثامنة: التقارير المالية والإيرادات (النسخة الفخمة والملونة بالكامل)
# ----------------------------------------------------
elif page == "💰 التقارير المالية والإيرادات":
    st.title("💰 الخزينة والتقارير المالية للشركة")
    st.subheader("لوحة تحكم تفاعلية ملونة بالكامل لمتابعة بنود الإيرادات والمصروفات")
    st.markdown("---")
    
    if 'df_finance' in st.session_state:
        df_finance = st.session_state['df_finance']
        
        # 🎨 دالة ذكية لتلوين أسطر الجدول بناءً على الكلمات المفتاحية
        def style_financial_rows(row):
            # نقوم بالبحث داخل كل خانات السطر عن أي إشارة لنوع الحركة
            row_str = " ".join(row.astype(str))
            if any(k in row_str for k in ['إيراد', 'ايراد', 'قبض', 'سداد', 'دخل']):
                return ['background-color: #e8f5e9; color: #1b5e20; font-weight: bold;'] * len(row)  # لون أخضر مريح
            elif any(k in row_str for k in ['مصروف', 'مصاريف', 'صرف', 'دفع', 'خروج']):
                return ['background-color: #ffebee; color: #b71c1c; font-weight: bold;'] * len(row)  # لون أحمر هادئ
            return [''] * len(row)
        
        # 📊 بناء 3 بطاقات ملونة فخمة وكبيرة في الأعلى لعرض ملخص الوضع المالي
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown("""<div style="background-color: #e8f5e9; border-right: 5px solid #2e7d32; padding: 20px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);"><p style="color: #2e7d32; margin:0; font-size:15px; font-weight:bold;">🟢 حركة المداخيل الحية</p><h3 style="color: #1b5e20; margin:5px 0 0 0;">متابعة الإيرادات المقبوضة</h3></div>""", unsafe_allow_html=True)
        with m_col2:
            st.markdown("""<div style="background-color: #ffebee; border-right: 5px solid #c62828; padding: 20px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);"><p style="color: #c62828; margin:0; font-size:15px; font-weight:bold;">🔴 حركة المصاريف الجارية</p><h3 style="color: #b71c1c; margin:5px 0 0 0;">متابعة البنود التشغيلية</h3></div>""", unsafe_allow_html=True)
        with m_col3:
            st.markdown("""<div style="background-color: #e3f2fd; border-right: 5px solid #1565c0; padding: 20px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);"><p style="color: #1565c0; margin:0; font-size:14px; font-weight:bold;">🏢 إدارة شركة قصر الهناء</p><h3 style="color: #0d47a1; margin:5px 0 0 0;">مواسم وحسابات 2026</h3></div>""", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("### 🗂️ كشف الحركة المالي المُلوّن ديناميكياً:")
        
        # تطبيق التلوين الاحترافي الكامل على الجدول القادم من جوجل شيت دون تعديل حرف واحد في البيانات
        styled_df = df_finance.style.apply(style_financial_rows, axis=1)
        
        # عرض الجدول الملون بحجم كامل وجذاب جداً للموظفين والإدارة
        st.dataframe(styled_df, use_container_width=True, height=450)
        
        st.success("💡 ميزة ذكية: يتم تلوين كل سطر باللون الأخضر تلقائياً إذا كان (إيراد) وباللون الأحمر إذا كان (مصروف) بناءً على بيانات الشيت.")
    else:
        st.warning("🔄 الرجاء الضغط على زر 'سحب وتحديث البيانات الشاملة' في القائمة الجانبية لسحب التقرير المالي.")
