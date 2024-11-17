import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.contrib import messages
from unittest.mock import patch
from tests.test_classes import BaseTest
@pytest.mark.django_db
class TestViewUpload(BaseTest):
    def test_get_request(self, client, user):
        # Simulate a logged-in user
        client.force_login(user)
        
        # Make a GET request
        response = client.get(reverse('view_upload'))
        
        # Check for a successful response and correct template
        assert response.status_code == 200
        assert 'form' in response.context
        assert 'home/upload.html' in [t.name for t in response.templates]

    def test_post_request_valid_file(self, client, user, mocker):
        # Simulate a logged-in user
        client.force_login(user)
        
        # Mock the result of `upload_cas_actions.do_upload_cas`
        mocker.patch('apps.home.actions.upload_cas.do_upload_cas', return_value={"status": "success", "web_doc_id": 123})
        
        # Create a mock PDF file
        pdf_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        
        # Make a POST request with a valid PDF file
        response = client.post(reverse('view_upload'), {
            'title': 'Test Document',
            'document': pdf_file,
        })
        
        # Check for a successful response
        assert response.status_code == 200
        assert "Your file has been uploaded successfully" in response.content.decode()
        assert 'home/upload_success.html' in [t.name for t in response.templates]

    def test_post_request_valid_file_with_real_pdf(self,client, user):
        # Simulate a logged-in user
        client.force_login(user)

        # Open the real PDF file
        #with open('iod-web/tests/resources/test.pdf', 'rb') as pdf_file:
        with open('tests/resources/test.pdf', 'rb') as pdf_file:
            # Simulate uploading the PDF
            uploaded_pdf = SimpleUploadedFile(pdf_file.name, pdf_file.read(), content_type="application/pdf")
            
            # Make a POST request with a valid PDF file
            response = client.post(reverse('view_upload'), {
                'title': 'Test Document',
                'document': uploaded_pdf,
            })
        
        # Check for a successful response
        assert response.status_code == 200
        assert "Your file has been uploaded successfully" in response.content.decode()
        assert 'home/upload_success.html' in [t.name for t in response.templates]

    def test_post_request_invalid_file(self, client, user):
        # Simulate a logged-in user
        client.force_login(user)
        
        # Create a mock non-PDF file
        non_pdf_file = SimpleUploadedFile("test.txt", b"file_content", content_type="text/plain")
        
        # Make a POST request with a non-PDF file
        response = client.post(reverse('view_upload'), {
            'title': 'Test Document',
            'document': non_pdf_file,
        })
        
        # Check for the error response
        assert response.status_code == 200
        assert "Please upload a valid PDF document." in response.content.decode()
        assert 'home/upload.html' in [t.name for t in response.templates]

    
    @patch('apps.home.actions.upload_cas.do_upload_cas')
    def test_post_request_raise_error_db(self, mock_do_upload_cas,client, user):
        mock_do_upload_cas.return_value = {"status": "fail", "message": "An error occurred in the database."}
        # Simulate a logged-in user
        client.force_login(user)
        #with open('iod-web/tests/resources/test.pdf', 'rb') as pdf_file:
        with open('tests/resources/test.pdf', 'rb') as pdf_file:
            # Simulate uploading the PDF
            uploaded_pdf = SimpleUploadedFile(pdf_file.name, pdf_file.read(), content_type="application/pdf")
            
            # Make a POST request with a valid PDF file
            response = client.post(reverse('view_upload'), {
                'title': 'Test Document',
                'document': uploaded_pdf,
            })
            print(response.content.decode())
            assert response.status_code == 200
            assert 'form' in response.context
            assert response.context['error_message'] == "An error occurred in the database."
            assert 'home/upload.html' in [t.name for t in response.templates]

    def test_post_request_invalid_form(self, client, user):
        # Simulate a logged-in user
        client.force_login(user)
        
        # Send invalid form data (missing document file)
        response = client.post(reverse('view_upload'), {
            'title': 'Test Document',
        })
        
        # Check that the form errors are handled properly
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors
        assert 'home/upload.html' in [t.name for t in response.templates]

    def test_post_request_exception_handling(self, client, user, mocker):
        # Simulate a logged-in user
        client.force_login(user)
        
        # Mock the `upload_cas_actions.do_upload_cas` to raise an exception
        mocker.patch('apps.home.actions.upload_cas.do_upload_cas', side_effect=Exception("An error occurred"))
        
        # Create a mock PDF file
        pdf_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        
        # Make a POST request and simulate an exception
        response = client.post(reverse('view_upload'), {
            'title': 'Test Document',
            'document': pdf_file,
        })
        
        # Check that the error page is rendered
        assert response.status_code == 200
        assert "InvestODiary -  500 Page" in response.content.decode()
