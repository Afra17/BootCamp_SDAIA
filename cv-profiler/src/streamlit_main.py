import os
import csv
import streamlit as st
from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown
import json

# Initialize session state
if "show_json" not in st.session_state:
    st.session_state.show_json = False
if "report_data" not in st.session_state:
    st.session_state.report_data = None

# Page configuration
st.set_page_config(
    page_title="CSV Profiler",
    layout="centered",
    initial_sidebar_state="collapsed"
)



# Title and header

st.title("📊 CSV Profiler")
st.write("Analyze and profile your CSV files to generate comprehensive data quality reports in JSON and Markdown formats")

# Main container
with st.container():
    st.markdown("""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        """, unsafe_allow_html=True)
    
    # File upload
    st.subheader("Step 1: Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", label_visibility="collapsed")
    
    # Preview first 5 rows
    if uploaded_file is not None:
        st.subheader("Preview (First 5 Rows)")
        try:
            # Convert bytes to text
            uploaded_file.seek(0)
            file_content = uploaded_file.read().decode('utf-8')
            
            # Read CSV from text content
            lines = file_content.split('\n')
            reader = csv.reader(lines)
            headers = next(reader)
            preview_rows = [headers]
            for i, row in enumerate(reader):
                if i < 5 and row:  # Skip empty rows
                    preview_rows.append(row)
                else:
                    break
            
            # Display as table
            st.table(preview_rows)
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    # Output directory option
    st.subheader("Step 2: Output Settings")
    use_custom_output = st.checkbox("Specify custom output directory", value=False)
    if use_custom_output:
        output_dir = st.text_input("Output directory path", value="output")
    else:
        output_dir = "output"
    
    # Generate button
    st.subheader("Step 3: Generate Report")
    if st.button("Generate Report", type="primary", use_container_width=True):
        if uploaded_file is None:
            st.error("Please upload a CSV file first.")
        else:
            try:
                # Create output directory
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                # Progress indicator
                with st.spinner(f"Processing file: {uploaded_file.name}..."):
                    # Save uploaded file temporarily
                    temp_file_path = os.path.join(output_dir, uploaded_file.name)
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Read CSV and generate report
                    rows = read_csv_rows(temp_file_path)
                    report = basic_profile(rows)
                    st.session_state.report_data = report  # Store in session state
                    
                    # Define output paths
                    json_path = os.path.join(output_dir, "report.json")
                    md_path = os.path.join(output_dir, "report.md")
                    
                    # Write reports
                    write_json(report, json_path)
                    write_markdown(report, md_path)
                
                # Success message
                st.success("✅ Reports generated successfully!")
                
                # Display results
                st.subheader("📋 Results")
                
                # Tabs for different views
                tab1, tab2, tab3 = st.tabs(["📝 Markdown Report", "🔍 JSON Report", "⬇️ Downloads"])
                
                with tab1:
                    st.markdown("### Detailed Analysis Report")
                    with open(md_path, "r") as f:
                        st.markdown(f.read())
                
                with tab2:
                    st.markdown("### JSON Data Structure")
                    with open(json_path, "r") as f:
                        st.json(json.load(f))
                
                with tab3:
                    st.markdown("### Download Your Reports")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        with open(json_path, "r") as f:
                            st.download_button(
                                label="📥 Download JSON",
                                data=f.read(),
                                file_name="report.json",
                                mime="application/json",
                                use_container_width=True
                            )
                    
                    with col2:
                        with open(md_path, "r") as f:
                            st.download_button(
                                label="📥 Download Markdown",
                                data=f.read(),
                                file_name="report.md",
                                mime="text/markdown",
                                use_container_width=True
                            )
                
                # Info about saved files
                st.info(f"✨ Files saved to: `{output_dir}`")
            
            except FileNotFoundError as e:
                st.error(f" Error: The file was not found. {str(e)}")
            except Exception as e:
                st.error(f" An error occurred: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

