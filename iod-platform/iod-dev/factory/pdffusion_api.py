from django.conf import settings
import httpx
from dotenv import load_dotenv
from abc import ABC, abstractmethod
import os
load_dotenv()

class PDFFusionAPIServiceFactory:
    @staticmethod
    def get_service():
        mock = bool(settings.USE_MOCK)
        print(f"settings to use mock set to : {mock}")
        if mock:
            print("Using Mock FastAPIService")
            return MockFastAPIService()  # Use the mock implementation
        else:
            print("Using Real FastAPIService")
            # load the api base url from env
            PDFFUSION_API_ROOT = os.getenv('PDFFUSION_API_ROOT')
            return RealFastAPIService(api_base_url=PDFFUSION_API_ROOT)  # Use the real implementation

class PDFFusionServiceInterface(ABC):
    @abstractmethod
    def get_document(self, document_id: int):
        pass

    @abstractmethod
    def create_document(self, document_data: dict):
        pass

    @abstractmethod
    def process_document(self, document_data: dict):
        pass

class RealFastAPIService(PDFFusionServiceInterface):
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url

    def get_document(self, document_id: int):
        response = httpx.get(f"{self.api_base_url}/documents/{document_id}")
        response.raise_for_status()
        return response.json()
    
    def create_document(self, document_data: dict):
        print(f"api base url in create document : {self.api_base_url}/cas-document/add")
        response = httpx.post(f"{self.api_base_url}/cas-document/add", json=document_data)
        response.raise_for_status()
        return response.json()

    def process_document(self, backend_doc_id: int, document_data: dict):
        print(f"api base url in process document : {self.api_base_url}/cas-document/{backend_doc_id}/process")
        response = httpx.post(f"{self.api_base_url}/cas-document/{backend_doc_id}/process", json=document_data)
        response.raise_for_status()
        return response.json()

class MockFastAPIService(PDFFusionServiceInterface):
    def get_document(self, document_id: int):
        # Return mock data instead of making an API call
        return {"document_id": document_id, "content": "This is a mock document"}
    def create_document(self, document_data: dict):
        return {
            "statusCode": 200,       
            "data" : [
                {
                    "doc_id": 12
                }
            ],
            "message" : "Document created successfully"  
        }

    def process_document(self, backend_doc_id,document_data: dict):
        # Return mock response for document processing
        return {
                "statusCode": 200,     
                "data" : [
                    {
                        "backend_doc_id" : backend_doc_id
                    }
                ],
                "message" : "Document processed successfully"
                }
