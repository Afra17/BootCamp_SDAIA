import os
import typer
from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown

app = typer.Typer()

@app.command()
def main(
    input_file: str = typer.Argument(..., help="Path to the input CSV file"),
    output_dir: str = typer.Option("output", help="Directory to save the output reports"),
) -> None:
    """Tool to profile CSV files and generate reports."""
    
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