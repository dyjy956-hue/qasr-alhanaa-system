

# تعليق لحماية السطر الأول من المسافات التلقائية
import streamlit as st
import pandas as pd
import urllib.parse
from io import BytesIO

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# ====================================================
# 🔒 نظام الحماية
# ====================================================
if 'master_password' not in st.session_state: st.session_state['master_password'] = "Samir2026"
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🔒 نظام تسجيل الدخول - شركة قصر الهناء")
    if st.button("🔓 تسجيل الدخول"):
        if st.text_input("كلمة المرور:", type="password") == st.session_state['master_password']:
            st.session_state['authenticated'] = True
            st.rerun()
    st.stop()

# ====================================================
# الدوال
# ====================================================
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def load_data_public(sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data

def get_wa_intent(phone, text):
    p = str(phone).replace('.0','').replace(' ','').replace('+','').replace('-','')
    if len(p) == 9 and p.startswith('9'): p = "218" + p
    elif len(p) == 10 and p.startswith('09'): p = "218" + p[1:]
    return f"intent://send?phone={p}&text={urllib.parse.quote(text)}#Intent;scheme=smsto;package=com.whatsapp;action=android.intent.action.SENDTO;end"

# ====================================================
# الصفحة الأولى: مركز المراسلات (مع الأزرار الخمسة)
# ====================================================
if 'df' not in st.session_state: st.session_state['df'] = load_data_public('Form responses 1')
page = st.sidebar.radio("القائمة:", ["💬 مركز مراسلة حالات الزبائن", "🔍 استعلام وبطاقة حجز عميل", "📋 الكشف الكلي"])

if page == "💬 مركز مراسلة حالات الزبائن":
    df = st.session_state['df']
    col_name = next((c for c in df.columns if 'الاسم' in c), None)
    col_phone = next((c for c in df.columns if 'الهاتف' in c or 'رقم' in c), None)
    
    if col_name and col_phone:
        selected_user = st.selectbox("اختر العميل:", df[col_name].dropna().tolist())
        u = df[df[col_name] == selected_user].iloc[0]
        
        # رسائل الواتساب
        msg_c = f"السلام عليكم، تم استلام بياناتكم لرحلة 2026."
        msg_p = f"تم تأكيد حجزكم بنجاح."
        msg_s = f"تم تأكيد السداد المالي بنجاح."
        msg_b = f"تفاصيل رحلة الغد..."
        msg_x = f"تم إلغاء تسجيلكم بنجاح."
        
        st.write("### 📲 خيارات المراسلة:")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.markdown(f'<a href="{get_wa_intent(u[col_phone], msg_c)}" target="_blank"><button style="width:100%; background:#2b5c8f; color:white; border:none; padding:10px; border-radius:5px;">🔵 1. استلام</button></a>', unsafe_allow_html=True)
        with c2: st.markdown(f'<a href="{get_wa_intent(u[col_phone], msg_p)}" target="_blank"><button style="width:100%; background:#1d3557; color:white; border:none; padding:10px; border-radius:5px;">🏁 2. تأكيد</button></a>', unsafe_allow_html=True)
        with c3: st.markdown(f'<a href="{get_wa_intent(u[col_phone], msg_s)}" target="_blank"><button style="width:100%; background:#25D366; color:white; border:none; padding:10px; border-radius:5px;">🟢 3. سداد</button></a>', unsafe_allow_html=True)
        with c4: st.markdown(f'<a href="{get_wa_intent(u[col_phone], msg_b)}" target="_blank"><button style="width:100%; background:#ff9800; color:white; border:none; padding:10px; border-radius:5px;">🚌 4. باص</button></a>', unsafe_allow_html=True)
        with c5: st.markdown(f'<a href="{get_wa_intent(u[col_phone], msg_x)}" target="_blank"><button style="width:100%; background:#d32f2f; color:white; border:none; padding:10px; border-radius:5px;">🔴 5. إلغاء</button></a>', unsafe_allow_html=True)

# ----------------------------------------------------
# 🔍 الصفحة الثانية: بطاقة العميل مع التكلفة
# ----------------------------------------------------
elif page == "🔍 استعلام وبطاقة حجز عميل":
    col_name = next((c for c in st.session_state['df'].columns if 'الاسم' in c), None)
    search_user = st.selectbox("🎯 اختر العميل:", ["-- اختر --"] + st.session_state['df'][col_name].dropna().tolist())
    if search_user != "-- اختر --":
        u = st.session_state['df'][st.session_state['df'][col_name] == search_user].iloc[0]
        col_cost = next((c for c in st.session_state['df'].columns if 'تكلفة' in c or 'مبلغ' in c or 'سعر' in c), 'غير مسجل')
        st.markdown(f"""<div style="background:#f8f9fa; padding:20px; border-radius:8px;">
            <h3>🎫 بطاقة الحجز</h3>
            <p><b>👤 الاسم:</b> {u.get(col_name)}</p>
            <div style="background:#fff3cd; padding:10px; border-radius:5px;">
                <p style="font-size:18px; color:#856404;"><b>💰 إجمالي التكلفة: {u.get(col_cost, 'غير مسجل')}</b></p>
            </div>
        </div>""", unsafe_allow_html=True)
