import argparse
import os
from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown

def main() -> None:
    parser = argparse.ArgumentParser(description="Tool to profile CSV files and generate reports.")
    
    parser.add_argument("input_file", type=str, help="Path to the input CSV file")
    
    parser.add_argument("--output_dir", type=str, default="output", help="Directory to save the output reports")

    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    print(f"Processing file: {args.input_file}...")

    try:
        rows = read_csv_rows(args.input_file)
        report = basic_profile(rows)
        
        json_path = os.path.join(args.output_dir, "report.json")
        md_path = os.path.join(args.output_dir, "report.md")

        write_json(report, json_path)
        write_markdown(report, md_path)

        print(f"Success Reports generated at:\n - {json_path}\n - {md_path}")
    
    except FileNotFoundError:
        print(f"Error: The file '{args.input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":  
    main()