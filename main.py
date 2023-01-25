import subprocess
import tempfile
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

temp_dir = None

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    # I know this is bad but this is also quick and easy.
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    global temp_dir
    temp_dir = tempfile.TemporaryDirectory()
    pass


@app.get("/")
async def root():
    return "hansard"


@app.get("/report")
def report(
    query: str,
):
    query_filename = query.replace(" ", "_")
    filename = f"{query_filename}.csv"
    global temp_dir
    print(temp_dir.name)
    output_file = "%s/%s-%s" % (temp_dir.name, uuid.uuid4(), filename)
    subprocess.run(
        ["python", "hansard/main.py", "--query", query, "--output", output_file]
    )

    def iterfile():
        with open(output_file, mode="rb") as file_like:
            yield from file_like

    response = StreamingResponse(iterfile(), media_type="text/csv")
    response.headers[
        "Content-Disposition"
    ] = f"attachment; filename={query_filename}.csv"
    return response


@app.get("/test")
def test():
    return {"result": "success"}
