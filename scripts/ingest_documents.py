import sys
import os

# Add root project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import DOCUMENTS_DIR
from backend.database import SessionLocal, Base, engine
from backend.rag.ingestion import DocumentIngestionManager

def run_ingestion():
    print("=========================================")
    print("      SevaAI Document Ingestion          ")
    print("=========================================\n")

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    manager = DocumentIngestionManager()

    print(f"Scanning directory: {DOCUMENTS_DIR}")
    results = manager.ingest_directory(DOCUMENTS_DIR, db)

    scanned = results["scanned_files"]
    successful = results["successful"]
    failed = results["failed"]
    total_pages = results["total_pages"]
    total_chunks = results["total_chunks"]

    print("\n-----------------------------------------")
    print(f"Scanned files : {scanned}")
    print(f"Successful    : {successful}")
    print(f"Failed        : {failed}")
    print(f"Total Pages   : {total_pages}")
    print(f"Total Chunks  : {total_chunks}")
    print("-----------------------------------------")

    if results["details"]:
        print("\nIngestion Summary:")
        for idx, item in enumerate(results["details"], 1):
            status_symbol = "[OK]" if item["status"] == "success" else "[X]"
            print(f"[{idx}/{scanned}] {status_symbol} {item['filename']} -- Pages: {item['pages']}, Chunks: {item['chunks']}")

    print("\nDone. Documents are indexed and ready for SevaAI search!")
    db.close()

if __name__ == "__main__":
    run_ingestion()
