from celery import shared_task
import time
import requests
import json
from apps.home.actions import upload_cas as upload_cas_actions
from dotenv import load_dotenv
import os, environ
import logging
from factory.pdffusion_api import PDFFusionAPIServiceFactory
from apps.home.actions.pdfdocumentstatus import(
    PDFDocumentStatusRepository as pdfdocumentstatus_actions
)
from apps.home.models import PDFDocument
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

#load env variables from env
load_dotenv()

PDFFUSION_API_ROOT = os.getenv('PDFFUSION_API_ROOT', '') 

#print("PDF FUSION API ROOT : "+PDFFUSION_API_ROOT)

# def make_api_post_request(url, data):
#     # Headers (optional, modify as needed)
#     headers = {
#         'Content-Type': 'application/json',
#         # 'Authorization': 'Bearer YOUR_TOKEN_HERE'  # Uncomment if you need to use an API key
#     }
    
#     # Make the POST request
#     response = requests.post(url, json=data, headers=headers)
#     logger.warning(f"response from: {response}")
#     # Check if the request was successful
#     if response.status_code == 200:
#         print("Request successful!")
#         print("Response:", response.json())
#     else:
#         print(f"Request failed with status code: {response.status_code}")
#         print("Response:", response.text)
#     return response

def call_pdf_fusion(user_id,title, file_name, path, file_hash,web_doc_id):
    pdffusion_service = PDFFusionAPIServiceFactory.get_service()
    post_data = {
        "user_id": user_id,
        "title": title,
        "path": path,
        "file_name" : file_name,
        "file_hash" : file_hash,
        "password" : "CJUPS9965B",
        "web_doc_id" : str(web_doc_id)
    }
    return pdffusion_service.create_document(post_data)

@shared_task
def add(user_id,title, file_name, path, file_hash):
    start_time = time.time()
    time.sleep(10)
    end_time = time.time()
    return call_pdf_fusion(user_id,title, file_name, path, file_hash)

@shared_task
def process_doc(user_id,title, file_name, path, file_hash, web_doc_id):
    logger.warning("PDF FUSION API ROOT : "+PDFFUSION_API_ROOT)
    # call pdf fusion api [cas-document/add] and copy file to pdffusion project dir
    # create document meta in pdffusiondb
    # return doc_id
    result = upload_doc_and_get_id(user_id,title, file_name, path, file_hash,web_doc_id)
    print(result)
    if result["statusCode"] != 201:
        return exit_process_document(user_id,web_doc_id,"Failed to upload document and create id at the backend through pdf fusion")
    logger.warning(result)
    data = result["data"][0]
    print("data from upload_doc_and_get_id: "+str(data))
    backend_doc_id = int(data["doc_id"])
    update_fields = {"backend_doc_id": backend_doc_id}
    logger.warning(update_fields)
    # update edb with backend_doc_id from pdffusion
    result = upload_cas_actions.do_update_fields_cas(user_id,web_doc_id,update_fields)
    if result["statusCode"] != 200:
        return exit_process_document(user_id,web_doc_id,"Failed to update edb with backend_doc_id")
    logger.warning("updated fields in the edb")
    pdffusion_service = PDFFusionAPIServiceFactory.get_service()
    #logger.warning("pdffusion service url  : "+str(pdffusion_service.api_base_url))
    request_body = {
        "user_id": user_id,
        "title": title,
        "path": path,
        "file_name" : file_name,
        "file_hash" : file_hash,
        "password" : "CJUPS9965B",
        "web_doc_id" : str(web_doc_id)
    }
    logger.warning(request_body)
    result = pdffusion_service.process_document(backend_doc_id,request_body)
    print("result from process_document: "+str(result))
    if result["statusCode"] != 200:
        return exit_process_document(user_id,web_doc_id,"Failed to complete processing of the document at the backend through pdf fusion")
    logger.warning(result)
    return result


def upload_doc_and_get_id(user_id,title, file_name, path, file_hash, web_doc_id):
    response = call_pdf_fusion(user_id,title, file_name, path, file_hash,web_doc_id)
    return response

def exit_process_document(user_id,web_doc_id,message):
    # update edb with pdfdocumentstatus as failed
    user = User.objects.get(id=user_id)
    document = PDFDocument.objects.get(id=web_doc_id,user=user)
    pdfdocumentstatus_actions.create_status(document,"failure",message=message)
    #delete cas document from web server


