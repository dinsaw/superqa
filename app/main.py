from fastapi import FastAPI, UploadFile, HTTPException, Response

import uuid
import shutil
import os
import json
import dotenv
import logging

from app.rag_util import get_rag

logger = logging.getLogger(__name__)

dotenv.load_dotenv()

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "UP"}


def ask(rag_chain, questions):
    result = {}
    for q in questions:
        result[q] = rag_chain.invoke(q)
    return result


@app.post("/answer")
def answer(source_file: UploadFile, question_file: UploadFile, response: Response):
    request_id = uuid.uuid4().hex
    response.headers["X-Request-ID"] = request_id

    if source_file.content_type not in ["application/pdf", "application/json"]:
        raise HTTPException(
            status_code=400, detail="Source file format should be PDF/JSON"
        )

    if question_file.content_type not in ["application/json"]:
        raise HTTPException(
            status_code=400, detail="Questions file format should be in JSON"
        )

    questions = json.load(question_file.file)
    if not isinstance(questions, list):
        raise HTTPException(
            status_code=400,
            detail="Uploaded questions file does not contain a JSON array.",
        )

    work_dir = f"/tmp/superqa/{request_id}"
    logger.info(f"workdir={work_dir}")
    os.makedirs(os.path.dirname(work_dir + "/"), exist_ok=True)

    source_file_location = f"{work_dir}/{source_file.filename}"
    with open(source_file_location, "wb+") as fo:
        shutil.copyfileobj(source_file.file, fo)

    rag_chain, vectorstore = get_rag(source_file.content_type, source_file_location)
    try:
        result = ask(rag_chain, questions)
    finally:
        vectorstore.delete_collection()
        shutil.rmtree(work_dir)

    return result
