import pandas as pd
import csv 
from io import StringIO
import streamlit as st
from csv_profiler.render import write_json, write_markdown

"""
data={
    'Name':['Alice','Bob','Charlie','David','Eva'],
    'Age':[25,30,35,40,45],
    'City':['New York','Los Angeles','Chicago','Houston','Phoenix']
}

df= pd.DataFrame(data)
st.title("Simple DataFrame Display")
st.subheader("This is a simple DataFrame displayed using Streamlit.")
st.dataframe(df)    


st.subheader("DataFrame Statistics")
st.write("Here are some basic statistics about the DataFrame:")
st.table(df.describe())
"""
#---------------------------------


# دالة مساعدة لتحويل الصفوف إلى نص مارك داون
def convert_to_markdown(rows):
    if not rows:
        return ""
    
    # 1. استخراج عناوين الأعمدة
    headers = list(rows[0].keys())
    
    # 2. إنشاء سطر العناوين
    md_output = "| " + " | ".join(headers) + " |\n"
    
    # 3. إنشاء الفاصل (---)
    md_output += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    
    # 4. إضافة البيانات صفاً بصف
    for row in rows:
        values = [str(row[h]) for h in headers]
        md_output += "| " + " | ".join(values) + " |\n"
        
    return md_output

# إعدادات الصفحة
st.set_page_config(page_title="CSV Uploader", layout="wide")
st.title("CSV Uploader, Viewer & Markdown Converter")

# رفع الملف
uploaded = st.file_uploader("Upload CSV file", type="csv")
show_stats = st.checkbox("Show Statistics", value=False)

if uploaded is not None:
    # قراءة الملف
    text = uploaded.getvalue().decode("utf-8")
    row = list(csv.DictReader(StringIO(text)))

    st.write(f"### Preview of `{uploaded.name}`")
    st.write("Rows loaded:", len(row))

    # عرض الإحصائيات (الصفوف الأولى) إذا تم تفعيل الخيار
    if show_stats:
        st.write(row[:5])
    else:
        st.write("Statistics not requested.")
    
    st.divider() # خط فاصل للتجميل

    # --- الجزء الجديد: تحويل وتنزيل المارك داون ---
    st.subheader("Markdown Export")
    
    # تحويل البيانات
    markdown_text = convert_to_markdown(row)
    
    # عرض معاينة بسيطة للمارك داون (اختياري)
    with st.expander("See Markdown Preview"):
        st.code(markdown_text, language="markdown")

    # زر التحميل
    st.download_button(
        label="Download as Markdown",
        data=markdown_text,
        file_name=f"{uploaded.name.split('.')[0]}.md",
        mime="text/markdown"
    )