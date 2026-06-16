

import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="فحص المنظومة", layout="wide")

SHEET_ID = '1emyWyimRfJEaX6TKCj2Q8G2h99BND1Or6wG4aZ-Xbpo'

st.title("🛠️ فحص الاتصال بملف البيانات")

try:
    # محاولة سحب البيانات
    encoded_sheet = urllib.parse.quote('Form responses 1')
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_sheet}'
    
    st.write("جاري الاتصال بالرابط:", url)
    
    df = pd.read_csv(url)
    
    if not df.empty:
        st.success("✅ تم العثور على البيانات بنجاح!")
        st.dataframe(df.head())
    else:
        st.warning("⚠️ الملف فارغ!")

except Exception as e:
    st.error(f"❌ حدث خطأ أثناء الاتصال: {e}")
    st.markdown("### الحلول المقترحة:")
    st.write("1. تأكد من أن ملف جوجل شيت مضبوط على **'أي شخص لديه الرابط' (Anyone with the link)**.")
    st.write("2. تأكد من أن الرابط الذي وضعته في `SHEET_ID` هو الرابط الطويل المكون من حروف وأرقام.")
