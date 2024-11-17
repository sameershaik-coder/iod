from apps.home.models import PDFDocumentStatus
from django.db.models import Q

class PDFDocumentStatusRepository:
    
    @staticmethod
    def create_status(document, status, message=None):
        """
        Create a new status entry for the document.
        
        :param document: The PDFDocument instance related to the status.
        :param status: The current status of the document (uploading, processing, etc.).
        :param message: Optional message providing more details about the status.
        :return: The created PDFDocumentStatus instance.
        """
        return PDFDocumentStatus.objects.create(document=document, status=status, message=message)

    @staticmethod
    def get_status_by_document(document):
        """
        Retrieve all status records for a given document.

        :param document: The PDFDocument instance whose status records are to be retrieved.
        :return: A queryset of PDFDocumentStatus instances.
        """
        return PDFDocumentStatus.objects.filter(document=document).order_by('timestamp')

    @staticmethod
    def get_latest_status_by_document(document):
        """
        Retrieve the latest status for a given document.
        
        :param document: The PDFDocument instance whose latest status is to be retrieved.
        :return: A PDFDocumentStatus instance or None if no status exists.
        """
        return PDFDocumentStatus.objects.filter(document=document).order_by('-timestamp').first()

    @staticmethod
    def update_status(document, status, message=None):
        """
        Update the status of a document.

        :param document: The PDFDocument instance whose status is being updated.
        :param status: The new status.
        :param message: Optional message providing more details about the update.
        :return: The updated PDFDocumentStatus instance.
        """
        current_status = PDFDocumentStatusRepository.get_latest_status_by_document(document)
        if current_status:
            current_status.status = status
            current_status.message = message
            current_status.save()
            return current_status
        else:
            return PDFDocumentStatusRepository.create_status(document, status, message)

    @staticmethod
    def get_documents_by_status(status):
        """
        Retrieve all documents that are currently in a given status.
        
        :param status: The status to filter by (e.g., 'processing', 'completed').
        :return: A queryset of PDFDocumentStatus instances.
        """
        return PDFDocumentStatus.objects.filter(status=status)

    @staticmethod
    def delete_status_by_document(document):
        """
        Delete all status records for a given document.
        
        :param document: The PDFDocument instance whose status records are to be deleted.
        :return: Number of deleted records.
        """
        return PDFDocumentStatus.objects.filter(document=document).delete()
