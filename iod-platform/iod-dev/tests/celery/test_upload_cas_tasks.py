import pytest
from unittest.mock import patch
from apps.tasks import process_doc
from apps.home.actions import upload_cas as upload_cas_actions
from tests.test_classes import BaseTest
from apps.home.actions.pdfdocumentstatus import(
    PDFDocumentStatusRepository as pdfdocumentstatus_actions
)
from apps.home.models import PDFDocument

@pytest.mark.django_db
class TestUploadCASTasks(BaseTest):

    @patch('apps.tasks.upload_doc_and_get_id')
    @patch('apps.home.actions.upload_cas.do_update_fields_cas')
    @patch('factory.pdffusion_api.PDFFusionAPIServiceFactory.get_service')
    @patch('apps.tasks.exit_process_document')
    def test_process_document_failure(
            self, mock_exit_process_document, mock_get_service, mock_do_update_fields_cas, mock_upload_doc_and_get_id, user):
        
        # Mock upload document and get ID response
        mock_upload_doc_and_get_id.return_value = {
            "status": "success",
            "doc_id": 12
        }

        # Mock updating fields in CAS response
        mock_do_update_fields_cas.return_value = {"status": "success"}

        # Mock pdffusion service process_document failure
        mock_service_instance = mock_get_service.return_value
        mock_service_instance.process_document.return_value = {"status": "failure"}

        # Call the process_doc task
        result = process_doc(
            user_id=user.id,
            title="Test Document",
            file_name="test.pdf",
            path="/path/to/test.pdf",
            file_hash="fakehash",
            web_doc_id=123
        )

        # Assertions
        mock_upload_doc_and_get_id.assert_called_once_with(user.id, "Test Document", "test.pdf", "/path/to/test.pdf", "fakehash", 123)
        mock_do_update_fields_cas.assert_called_once_with(user.id, 123, {"backend_doc_id": 12})
        mock_service_instance.process_document.assert_called_once_with(12, {
            "user_id": user.id,
            "title": "Test Document",
            "path": "/path/to/test.pdf",
            "file_name": "test.pdf",
            "file_hash": "fakehash",
            "password": "CJUPS9965B",
            "web_doc_id": "123"
        })
        #mock_exit_process_document.assert_called_once_with(user.id, 123, "failure to process document in pdffusion")
        assert result == {"status": "failure"}

    @patch('apps.tasks.upload_doc_and_get_id')
    @patch('apps.home.actions.upload_cas.do_update_fields_cas')
    def test_update_fields_cas_failure(
            self, #mock_exit_process_document, 
            mock_do_update_fields_cas, mock_upload_doc_and_get_id,client, user):
        
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        web_doc_id = upload_cas_actions.do_upload_cas(user, "Test Document", "/path/to/test.pdf", "fakehash").get("web_doc_id")
        
        # Mock upload document and get ID response
        mock_upload_doc_and_get_id.return_value = {
            "status": "success",
            "doc_id": 12
        }

        # Mock updating fields in CAS failure
        mock_do_update_fields_cas.return_value = {"status": "failure"}

        # Call the process_doc task
        result = process_doc(
            user_id=user.id,
            title="Test Document",
            file_name="test.pdf",
            path="/path/to/test.pdf",
            file_hash="fakehash",
            web_doc_id=web_doc_id
        )

        # Assertions
        mock_upload_doc_and_get_id.assert_called_once_with(user.id, "Test Document", "test.pdf", "/path/to/test.pdf", "fakehash", web_doc_id)
        mock_do_update_fields_cas.assert_called_once_with(user.id, web_doc_id, {"backend_doc_id": 12})
        doc = PDFDocument.objects.get(id=web_doc_id)
        statuses = pdfdocumentstatus_actions.get_status_by_document(doc)
        count = statuses.count()
        assert count == 1
        assert statuses[0].status == "failure"
        assert statuses[0].message == "Failed to update edb with backend_doc_id"
        

    @patch('apps.tasks.upload_doc_and_get_id')
    @patch('apps.home.actions.upload_cas.do_update_fields_cas')
    @patch('factory.pdffusion_api.PDFFusionAPIServiceFactory.get_service')
    @patch('apps.tasks.exit_process_document')
    def test_successful_process_doc(
            self, mock_exit_process_document, mock_get_service, mock_do_update_fields_cas, mock_upload_doc_and_get_id, user):
        
        # Mock upload document and get ID response
        mock_upload_doc_and_get_id.return_value = {
            "status": "success",
            "doc_id": 12
        }

        # Mock updating fields in CAS response
        mock_do_update_fields_cas.return_value = {"status": "success"}

        # Mock pdffusion service process_document
        mock_service_instance = mock_get_service.return_value
        mock_service_instance.process_document.return_value = {"status": "success"}

        # Call the process_doc task
        result = process_doc(
            user_id=user.id,
            title="Test Document",
            file_name="test.pdf",
            path="/path/to/test.pdf",
            file_hash="fakehash",
            web_doc_id=123
        )

        # Assertions
        mock_upload_doc_and_get_id.assert_called_once_with(user.id, "Test Document", "test.pdf", "/path/to/test.pdf", "fakehash", 123)
        mock_do_update_fields_cas.assert_called_once_with(user.id, 123, {"backend_doc_id": 12})
        mock_service_instance.process_document.assert_called_once_with(12, {
            "user_id": user.id,
            "title": "Test Document",
            "path": "/path/to/test.pdf",
            "file_name": "test.pdf",
            "file_hash": "fakehash",
            "password": "CJUPS9965B",
            "web_doc_id": "123"
        })
        assert result == {"status": "success"}
        mock_exit_process_document.assert_not_called() 

    @patch('apps.tasks.upload_doc_and_get_id')
    def test_validate_backend_doc_id_fail(self, mock_upload_doc_and_get_id, client, user):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        web_doc_id = upload_cas_actions.do_upload_cas(user, "Test Document", "/path/to/test.pdf", "fakehash").get("web_doc_id")
        # Mock the call_pdf_fusion response
        mock_upload_doc_and_get_id.return_value = {
            "status": "failure",       
            "code" : 500,
            "doc_id" : 0
        }

        # Call the process_doc task
        result = process_doc(
            user_id=user.id,
            title="Test Document",
            file_name="test.pdf",
            path="/path/to/test.pdf",
            file_hash="fakehash",
            web_doc_id=web_doc_id
        )

        # Assertions
        doc = PDFDocument.objects.get(id=web_doc_id)
        statuses = pdfdocumentstatus_actions.get_status_by_document(doc)
        count = statuses.count()
        assert count == 1
        assert statuses[0].status == "failure"
        assert statuses[0].message == "Failed to upload document and create id at the backend through pdf fusion"
    
    @patch('apps.tasks.upload_doc_and_get_id')
    def test_validate_backend_doc_id_success(self, mock_upload_doc_and_get_id, client, user):
        self.initialize_user(user,False,False,True)
        self.user_login(client,user)
        web_doc_id = upload_cas_actions.do_upload_cas(user, "Test Document", "/path/to/test.pdf", "fakehash").get("web_doc_id")
        # Mock the call_pdf_fusion response
        mock_upload_doc_and_get_id.return_value = {
            "status": "success",       
            "code" : 200,
            "doc_id" : 12
        }

        # Call the process_doc task
        result = process_doc(
            user_id=user.id,
            title="Test Document",
            file_name="test.pdf",
            path="/path/to/test.pdf",
            file_hash="fakehash",
            web_doc_id=web_doc_id
        )

        # Assertions
        doc = PDFDocument.objects.get(id=web_doc_id)
        statuses = pdfdocumentstatus_actions.get_status_by_document(doc)
        count = statuses.count()
        assert count == 0