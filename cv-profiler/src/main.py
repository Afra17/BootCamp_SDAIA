import os
import typer
from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown
import os
app = typer.Typer()

@app.command()
def main(
    input_file: str = typer.Argument(..., help="Path to the input CSV file"),
    output_dir: str = typer.Option("output", help="Directory to save the output reports"),
) -> None:
    
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Processing file: {input_file}...")

    try:
        rows = read_csv_rows(input_file)
        report = basic_profile(rows)
        
        json_path = os.path.join(output_dir, "report.json")
        md_path = os.path.join(output_dir, "report.md")

        write_json(report, json_path)
        write_markdown(report, md_path)

        print(f"Success! Reports generated at:\n - {json_path}\n - {md_path}")
    
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    app()


##this part is for streamlit app (not available now)
"""
st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

# Output directory option
use_custom_output = st.checkbox("Specify custom output directory", value=False)
if use_custom_output:
    output_dir = st.text_input("Output directory path", value="output")
else:
    output_dir = "output"

# Process button
if st.button("Generate Report", type="primary"):
    if uploaded_file is None:
        st.error("Please upload a CSV file first.")
    else:
        try:
            # Create output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            st.info(f"Processing file: {uploaded_file.name}...")
            
            # Read CSV from uploaded file
            file_content = uploaded_file.read().decode("utf-8")
            csv_file = io.StringIO(file_content)
            rows = read_csv_rows(csv_file)
            
            # Generate profile report
            report = basic_profile(rows)
            
            # Define output paths
            json_path = os.path.join(output_dir, "report.json")
            md_path = os.path.join(output_dir, "report.md")
            
            # Write reports to files
            write_json(report, json_path)
            write_markdown(report, md_path)
            
            # Success message
            st.success(" Reports generated successfully!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f" JSON Report: `{json_path}`")
            with col2:
                st.info(f" Markdown Report: `{md_path}`")
            
            # Display report preview
            st.subheader("Report Preview")
            
            # Show JSON preview
            with st.expander(" JSON Report"):
                st.json(report)
            
            # Show Markdown preview
            with st.expander(" Markdown Report"):
                with open(md_path, "r") as f:
                    st.markdown(f.read())
            
            # Download buttons
            st.subheader("Download Reports")
            col1, col2 = st.columns(2)
            
            with col1:
                with open(json_path, "r") as f:
                    st.download_button(
                        label="Download JSON Report",
                        data=f.read(),
                        file_name="report.json",
                        mime="application/json"
                    )
            
            with col2:
                with open(md_path, "r") as f:
                    st.download_button(
                        label="Download Markdown Report",
                        data=f.read(),
                        file_name="report.md",
                        mime="text/markdown"
                    )
        
        except FileNotFoundError as e:
            st.error(f"Error: The file was not found. {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

"""