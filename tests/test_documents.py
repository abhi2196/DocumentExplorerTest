import pytest

from utils.logs_util import DocumentExplorerLogger
from utils.document_explorer import Documents
from utils.driver_utils import DriverUtils


@pytest.mark.usefixtures("driver_init")
class TestDocuments:
    logger = DocumentExplorerLogger()
    document = Documents()
    driver_utils = DriverUtils()

    @pytest.mark.parametrize("collection_name, document_path, expected_error", [
        ("abhishek", str(document.pdf_test_file_path), None),
        ("abhishek", str(document.tar_test_file_path), document.document_upload_failure_msg)
    ])
    def test_document_upload(self, collection_name, document_path, expected_error):
        """
        Test to validate document upload use-cases
        1. Upload new document
        2. Upload new document with existing document of same name
        3. Upload new document of unsupported file type (other than PDF, JPG, PNG, TIFF)
        :param collection_name: Name of the collection to create document in (assumes collection exists already)
        :param document_path: Local path pointing to test files
        :param expected_error: Expected error message on create operation
        :return:
        """
        self.logger.log_enter("test_document_upload")

        # upload a document
        self.driver_utils.upload_document(
            self.driver,
            collection_name,
            document_path,
            expected_error=expected_error
        )

        self.logger.log_exit("test_document_upload")

    @pytest.mark.parametrize("collection_name, document_name, expected_result", [
        ("abhishek", document.pdf_test_file_2_name, True),
        ("abhishek", "foobar", False)
    ])
    def test_document_search(self, collection_name, document_name, expected_result):
        """
        Test to validate document search use-cases
        1. Search existing document
        2. Search non-existing document
        :param collection_name: Name of the collection to create
        :param document_name: Name of the document to search
        :param expected_result: Expected output of search operation
        :return:
        """
        self.logger.log_enter("test_document_search")

        # search a document by its name
        results = self.driver_utils.search_document(
            self.driver,
            collection_name,
            document_name
        )

        # compare output returned by search operation with expected result
        assert self.document.check_if_name_exist(document_name, results) == expected_result
        self.logger.log_exit("test_document_search")

    @pytest.mark.skipif(True, reason="TBD")
    def test_document_sort(self):
        """
        Test to validate document sort use-cases
        1. Sort with Name as key (ascending order)
        2. Sort with Name as key (descending order)
        3. Sort with default order
        :return:
        """
        self.logger.log_enter("test_document_sort")
        self.logger.log_exit("test_document_sort")

    @pytest.mark.skipif(True, reason="TBD")
    def test_document_filter(self):
        """
        Test to validate document filter use-cases
        1. Select Processing state filter [Queued, Processing, Processed, Failed, Migrated, Validated]
        2. Select Done state filter [Reviewed, Rejected]
        3. Reset/Reset_All options
        :return:
        """
        self.logger.log_enter("test_document_filter")
        self.logger.log_exit("test_document_filter")
