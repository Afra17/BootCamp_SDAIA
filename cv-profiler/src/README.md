# CSV Profiler Tool
Follow these instructions to set up and run the project.


## 1. Clone the repo
git clone https://github.com/Afra17/BootCamp_SDAIA

cd BootCamp_SDAIA

## 2. Create virtual env 
uv venv
source .venv/bin/activate 

## 3. Install dependencies
uv pip install -r requirements.txt

## 4. Run 
python main.py path/to/your/file.csv

## You can specify where to save the reports using --output_dir:
python main.py path/to/your/file.csv --output_dir my_reports


