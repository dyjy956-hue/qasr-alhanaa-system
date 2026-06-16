

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# ====================================================
# 🔒 نظام الحماية
# ====================================================
if 'master_password' not in st.session_state:
    st.session_state['master_password'] = "Samir2026"

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🔒 نظام تسجيل الدخول - شركة قصر الهناء")
    if st.button("🔓 تسجيل الدخول"):
        if st.text_input("كلمة المرور:", type="password") == st.session_state['master_password']:
            st.session_state['authenticated'] = True
            st.rerun()
    st.stop()

# ====================================================
# الدوال الأساسية
# ====================================================
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

# دالة فتح تطبيق الواتساب مباشرة
def get_wa_intent(phone, text):
    return f"intent://send?phone={phone}&text={urllib.parse.quote(text)}#Intent;scheme=smsto;package=com.whatsapp;action=android.intent.action.SENDTO;end"

# ====================================================
# القائمة الجانبية
# ====================================================
st.sidebar.title("🏢 لوحة تحكم قصر الهناء")
page = st.sidebar.radio("انتقل إلى:", ["💬 مركز المراسلات", "🔍 استعلام وبطاقة حجز عميل", "📋 الكشف الكلي للركاب"])

if 'df' not in st.session_state: st.session_state['df'] = load_data_public('Form responses 1')

# ----------------------------------------------------
# 💬 الصفحة الأولى: مركز مراسلة حالات الزبائن
# ----------------------------------------------------
if page == "💬 مركز مراسلة حالات الزبائن":
    st.title("💬 مركز المراسلات الذكي")
    df = st.session_state['df']
    # البحث عن عمود الاسم الثلاثي
    col_name = next((c for c in df.columns if 'الاسم' in c), None)
    col_phone = next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c), None)

    if col_name and col_phone:
        selected_user = st.selectbox("اختر العميل:", df[col_name].dropna().tolist())
        user_data = df[df[col_name] == selected_user].iloc[0]
        
        msg = f"السلام عليكم،\nعزيزي *{user_data[col_name]}* 🌹\nتم استلام بياناتكم بنجاح في شركة قصر الهناء."
        url = get_wa_intent(str(user_data[col_phone]).replace('.0',''), msg)
        st.markdown(f'<a href="{url}" target="_blank"><button style="background-color: #25D366; color: white; padding: 10px; border-radius: 5px;">📲 إرسال عبر واتساب</button></a>', unsafe_allow_html=True)

# ----------------------------------------------------
# 🔍 الصفحة الثانية: استعلام وبطاقة حجز عميل (مع إجمالي التكلفة)
# ----------------------------------------------------
elif page == "🔍 استعلام وبطاقة حجز عميل":
    st.title("🔍 نظام الاستعلام الفوري")
    df = st.session_state['df']
    col_name = next((c for c in df.columns if 'الاسم' in c), None)
    
    if col_name:
        search_user = st.selectbox("🎯 اختر العميل (الاسم الثلاثي):", ["-- اختر --"] + df[col_name].dropna().tolist())
        if search_user != "-- اختر --":
            user_data = df[df[col_name] == search_user].iloc[0]
            
            # البحث الذكي عن عمود التكلفة (سواء كان اسمه تكلفة، مبلغ، سعر)
            col_cost = next((c for c in df.columns if 'تكلفة' in c or 'مبلغ' in c or 'سعر' in c), None)
            cost_val = user_data.get(col_cost, 'غير محدد')
            
            st.markdown(f"""
            <div style="background-color: #f8f9fa; border-right: 5px solid #1d3557; padding: 20px; border-radius: 8px;">
                <h3>🎫 بطاقة البيانات - {user_data[col_name]}</h3>
                <p><b>👤 الاسم الثلاثي:</b> {user_data[col_name]}</p>
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; border: 1px solid #ffeeba;">
                    <p style="font-size: 20px; color: #856404; margin: 0;"><b>💰 إجمالي التكلفة: {cost_val}</b></p>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif page == "📋 الكشف الكلي للركاب":
    st.dataframe(st.session_state['df'], use_container_width=True)
