from fastapi import APIRouter, UploadFile, File
from app.services.document_processor import extract_text_from_pdf, chunk_text
from app.services.vector_store import create_vector_store, load_vector_store
from app.services.query_handler import answer_question

router = APIRouter()

@router.post("/upload/")
async def upload_files(files: list[UploadFile] = File(...)):
    all_chunks, all_meta = [], []
    for f in files:
        path = f"./data/{f.filename}"
        with open(path, "wb") as out: out.write(await f.read())
        pages = extract_text_from_pdf(path)
        chunks, meta = chunk_text(pages)
        all_chunks += chunks
        all_meta += [{"filename": f.filename, **m} for m in meta]
    create_vector_store(all_chunks, all_meta)
    return {"status": "ingested", "chunks": len(all_chunks)}

@router.post("/query/")
async def query(q: str):
    vectordb = load_vector_store()
    answer = answer_question(vectordb, q)
    return {"answer": answer}
