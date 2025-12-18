"""
FRONTEND - Create file: frontend.py
This is the Streamlit UI (no backend logic here)
"""
import streamlit as st
import requests
import csv
import json

st.set_page_config(page_title="CSV Profiler", layout="centered", initial_sidebar_state="collapsed")

# Title
st.title("📊 CSV Profiler")
st.write("Analyze and profile your CSV files to generate comprehensive data quality reports")

# Backend API URL
BACKEND_URL = "https://bootcamp-sdaia.onrender.com"

# File upload
st.subheader("📁 Step 1: Upload CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv", label_visibility="collapsed")

# Preview first 5 rows
if uploaded_file is not None:
    st.subheader("👀 Preview (First 5 Rows)")
    try:
        uploaded_file.seek(0)
        file_content = uploaded_file.read().decode('utf-8')
        lines = file_content.split('\n')
        reader = csv.reader(lines)
        headers = next(reader)
        preview_rows = [headers]
        for i, row in enumerate(reader):
            if i < 5 and row:
                preview_rows.append(row)
            else:
                break
        st.table(preview_rows)
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")

# Output directory
st.subheader("📂 Step 2: Output Settings")
use_custom_output = st.checkbox("Specify custom output directory", value=False)
output_dir = st.text_input("Output directory path", value="output") if use_custom_output else "output"

# Generate button
st.subheader("⚙️ Step 3: Generate Report")
if st.button("🚀 Generate Report", type="primary", use_container_width=True):
    if uploaded_file is None:
        st.error("❌ Please upload a CSV file first.")
    else:
        with st.spinner(f"Processing file: {uploaded_file.name}..."):
            try:
                # Send file to backend
                files = {"file": uploaded_file.getbuffer()}
                params = {"output_dir": output_dir}
                
                response = requests.post(f"{BACKEND_URL}/upload-csv/", files=files, params=params)
                result = response.json()
                
                if result["status"] == "success":
                    st.success("✅ Reports generated successfully!")
                    
                    # Store report in session state
                    st.session_state.report = result["report"]
                    st.session_state.json_path = result["json_path"]
                    st.session_state.md_path = result["md_path"]
                else:
                    st.error(f"❌ Error: {result['message']}")
            
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}\nMake sure backend is running on {BACKEND_URL}")

# Display results if available
if "report" in st.session_state:
    st.subheader("📋 Results")
    tab1, tab2, tab3 = st.tabs(["📝 Markdown Report", "🔍 JSON Report", "⬇️ Downloads"])
    
    with tab1:
        st.markdown("### Detailed Analysis Report")
        with open(st.session_state.md_path, "r") as f:
            st.markdown(f.read())
    
    with tab2:
        st.markdown("### JSON Data Structure")
        st.json(st.session_state.report)
    
    with tab3:
        st.markdown("### Download Your Reports")
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Download JSON",
                data=json.dumps(st.session_state.report, indent=2),
                file_name="report.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            with open(st.session_state.md_path, "r") as f:
                st.download_button(
                    label="📥 Download Markdown",
                    data=f.read(),
                    file_name="report.md",
                    mime="text/markdown",
                    use_container_width=True
                )
        
        st.info(f"✨ Files saved to: `{st.session_state.json_path}`")