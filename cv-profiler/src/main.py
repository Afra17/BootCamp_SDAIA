from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown


def main() -> None:
    rows = read_csv_rows(r"C:\Users\user\OneDrive - University of Prince Mugrin\سطح المكتب\bootcamp\cv-profiler\src\data\sample.csv")
    report = basic_profile(rows)
    write_json(report,"output/report.json")
    write_markdown(report,"output/report.md")
    print("Profile report generated at output/report.json and output/report.md")


if __name__ == "__main__":  
    main()