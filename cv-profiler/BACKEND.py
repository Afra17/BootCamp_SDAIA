"""
BACKEND - Create file: backend.py (or backend/app.py)
This handles all the CSV processing logic
"""
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import json
from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import write_json, write_markdown

app = FastAPI()

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), output_dir: str = "output"):
    """Backend endpoint to process CSV file"""
    try:
        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save uploaded file
        temp_file_path = os.path.join(output_dir, file.filename)
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())
        
        # Process CSV
        rows = read_csv_rows(temp_file_path)
        report = basic_profile(rows)
        
        # Save reports
        json_path = os.path.join(output_dir, "report.json")
        md_path = os.path.join(output_dir, "report.md")
        
        write_json(report, json_path)
        write_markdown(report, md_path)
        
        # Return report data
        return {
            "status": "success",
            "message": "Reports generated successfully",
            "report": report,
            "json_path": json_path,
            "md_path": md_path
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/download-json/")
async def download_json(file_path: str):
    """Backend endpoint to download JSON report"""
    return FileResponse(file_path, media_type="application/json", filename="report.json")

@app.get("/download-md/")
async def download_md(file_path: str):
    """Backend endpoint to download Markdown report"""
    return FileResponse(file_path, media_type="text/markdown", filename="report.md")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

