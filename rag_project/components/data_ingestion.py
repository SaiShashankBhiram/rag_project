import os
import pickle
import sys
from pymongo import MongoClient
from urllib.parse import quote_plus
from rag_project.logger import logging
from rag_project.exception import CustomException

def ingest_from_mongodb():
    logging.info("Connecting to MongoDB")

    try:
        username = quote_plus("saishashankbhiram")
        password = quote_plus("Admin123")
        uri = f"mongodb+srv://{username}:{password}@cluster0.o0y1c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        client = MongoClient(uri)
        db = client["rag_app_db"]
        collection = db["pdf_documents"]

        logging.info("Fetching data from MongoDB")
        data_cursor = collection.find()
        documents = []

        for i, doc in enumerate(data_cursor, start=1):
            try:
                text = doc.get("content", "")
                metadata = doc.get("metadata", {})
                if text.strip():
                    logging.info(f"Document {i} retreived, length: {len(text)} chars")
                    documents.append({"content": text, "metadata": metadata})
                else:
                    logging.warning(f"Document {i} is empty or whitespace, skipping")
            except Exception as doc_error:
                logging.error(f"Error processing document {i}: {doc_error}")
                raise CustomException(doc_error, sys)
            
        logging.info(f"Total documents fetched: {len(documents)}")

        try:
            BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            DATA_DIR = os.path.join(BASE_DIR, "data")
            os.makedirs(DATA_DIR, exist_ok=True)

            with open(os.path.join(DATA_DIR, "documents.pkl"), "wb") as f:
                pickle.dump(documents, f)
                logging.info("Documents saved to data/documents.pkl")

        except Exception as file_error:
            logging.error(f"Error saving documents to file: {file_error}")
            raise CustomException(file_error, sys)
        
    except Exception as mongo_error:
        logging.error(f"Error connecting to MongoDB: {mongo_error}")
        raise CustomException(mongo_error, sys)
    
if __name__ == "__main__":
    try:
        ingest_from_mongodb()
    except CustomException as ce:
        logging.error(f" Critical Failure: {ce}")