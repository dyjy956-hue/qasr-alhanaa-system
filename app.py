

import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="منظومة قصر الهناء", layout="wide")

# إعدادات بسيطة
SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

def get_data():
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Form%20responses%201'
    return pd.read_csv(url)

st.title("🚌 منظومة قصر الهناء")

try:
    df = get_data()
    st.success("تم تحميل البيانات بنجاح!")
    
    # اختيار العميل
    name_col = df.columns[0]
    phone_col = df.columns[1]
    
    selected = st.selectbox("اختر العميل:", df[name_col].dropna().tolist())
    
    if selected:
        row = df[df[name_col] == selected].iloc[0]
        phone = str(row[phone_col]).replace('.0', '').replace('+', '').replace(' ', '')
        
        msg = f"أهلاً أستاذ {selected}، تم تأكيد حجزكم مع شركة قصر الهناء."
        
        # الرابط لفتح تطبيق واتساب مباشرة
        url = f"whatsapp://send?phone={phone}&text={urllib.parse.quote(msg)}"
        
        st.markdown(f'<a href="{url}" style="text-decoration:none;"><button style="background-color:#25D366; color:white; padding:15px; border-radius:10px; width:100%; border:none; font-weight:bold;">🚀 إرسال عبر تطبيق واتساب</button></a>', unsafe_allow_html=True)
        
        st.write("بيانات العميل:", row)

except Exception as e:
    st.error(f"حدث خطأ في تحميل البيانات: {e}")
    st.write("تأكد من أن اسم الورقة في جوجل شيت هو 'Form responses 1' بالضبط.")
