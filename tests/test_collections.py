import pytest

from utils.logs_util import DocumentExplorerLogger
from utils.document_explorer import Collections
from utils.driver_utils import DriverUtils


@pytest.mark.usefixtures("driver_init")
class TestCollections:
    logger = DocumentExplorerLogger()
    collections = Collections()
    driver_utils = DriverUtils()

    @pytest.mark.parametrize("collection_name, expected_result, expected_error", [
        ("test_collection", True, None),
        ("abhishek", True, collections.create_error_message)
    ])
    def test_collection_create(self, collection_name, expected_result, expected_error):
        """
        Test to validate collection create use-cases
        1. Create new collection (Assumes collection does not exist already)
        2. Create new collection with existing collection of same name

        :param collection_name: Name of the collection to create
        :param expected_result: Expected output of create operation
        :param expected_error: Expected error message on create operation
        :return:
        """
        self.logger.log_enter("test_collection_create")

        # create a collection
        self.driver_utils.create_collection(
            self.driver,
            collection_name,
            expected_error=expected_error
        )

        # search a collection by its name
        results = self.driver_utils.search_collection(
            self.driver,
            collection_name
        )

        # compare output returned by search operation with expected result
        assert self.collections.check_if_name_exist(collection_name, results) == expected_result

        self.logger.log_exit("test_collection_create")

    @pytest.mark.parametrize("collection_name, expected_result", [
        ("abhishek", True),
        ("foobar", False)
    ])
    def test_collection_search(self, collection_name, expected_result):
        """
        Test to validate collection search use-cases
        1. Search existing collection
        2. Search non-existing collection

        :param collection_name: Name of the collection to search
        :param expected_result: Expected output of search operation
        :return:
        """
        self.logger.log_enter("test_collection_search")

        # search a collection by its name
        results = self.driver_utils.search_collection(
            self.driver,
            collection_name
        )

        # compare output returned by search operation with expected result
        assert self.collections.check_if_name_exist(collection_name, results) == expected_result

        self.logger.log_exit("test_collection_search")

    @pytest.mark.parametrize("sort_order", [
        "ascending",
        "descending"
    ])
    def test_collection_sort(self, sort_order):
        """
        Test to validate collection sort use-cases
        1. Sort with Name as key (ascending order)
        2. Sort with Name as key (descending order)
        3. Sort with default order

        :param sort_order: Sorting order for collection names (ascending, descending, default)
        :return:
        """
        self.logger.log_enter("test_collection_sort")

        # sort the collection list with Name as key
        results = self.driver_utils.sort_collection(
            self.driver,
            sort_order
        )
        self.collections.validate_list_order(results, sort_order)
        self.logger.log_exit("test_collection_sort")

    @pytest.mark.skipif(True, reason="TBD")
    def test_collection_filter(self):
        """
        Test to validate collection filter use-cases
        1. Select Processing state filter
        2. Select Done state filter
        3. Reset/Reset_All options
        :return:
        """
        self.logger.log_enter("test_collection_filter")
        self.logger.log_exit("test_collection_filter")
