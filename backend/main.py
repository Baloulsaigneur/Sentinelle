from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from pydantic import BaseModel
from utils import run_nmap, run_nuclei, run_nikto

app = FastAPI()

# CORS pour éviter les erreurs 405 et permettre les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (met ici ton vrai domaine en production)
    allow_credentials=True,
    allow_methods=["POST", "GET"],  # Autorise POST et GET
    allow_headers=["*"],
)

# Simulated in-memory task storage
tasks = {}

# Input validation schema
class ScanRequest(BaseModel):
    target: str


@app.post("/scan/")
def start_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """
    Start a scan process for a given target.
    """
    target = request.target
    task_id = str(uuid4())
    # Store the initial task status
    tasks[task_id] = {"status": "pending", "result": None}
    # Add the scan to background tasks
    background_tasks.add_task(run_scan, task_id, target)
    return {"task_id": task_id, "status": "started"}


def run_scan(task_id: str, target: str):
    """
    Orchestrate Nmap, Nuclei, and Nikto scans.
    """
    try:
        # Run Nmap
        nmap_result = run_nmap(target)

        # Run Nuclei using the target
        nuclei_result = run_nuclei(target)

        # Run Nikto
        nikto_result = run_nikto(target)

        # Aggregate results
        tasks[task_id] = {
            "status": "completed",
            "result": {
                "nmap": nmap_result,
                "nuclei": nuclei_result,
                "nikto": nikto_result
            }
        }
    except Exception as e:
        # Handle errors during scans
        tasks[task_id] = {"status": "error", "error": str(e)}


@app.get("/results/{task_id}")
def get_results(task_id: str):
    """
    Fetch the results of a scan by task ID.
    """
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/")
def root():
    """
    Default endpoint to check if the API is running.
    """
    return {"message": "Pentest API is running"}
