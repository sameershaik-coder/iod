from apps.home.models import PDFDocument
from django.db import transaction


def do_upload_cas(user,document_name, document_path,file_hash):
    result = {}
    with transaction.atomic():
        if PDFDocument.objects.filter(file_hash=file_hash).exists():
            error_message = "This file has already been uploaded."
            result["status"] = "fail"
            result["message"] = error_message
        else:
            pdf = PDFDocument.objects.create(user=user, title=document_name, document=document_path, file_hash=file_hash)
            pdf.save()
            result["status"] = "success"
            result["web_doc_id"] = pdf.id
        
        return result

def do_update_fields_cas(user,document_id,update_fields):
    result = {}
    with transaction.atomic():
        pdf = PDFDocument.objects.get(id=document_id,user=user)
        for key, value in update_fields.items():
            setattr(pdf, key, value)
        pdf.save()
        result["statusCode"] = 200
        result["web_doc_id"] = pdf.id
        return result

