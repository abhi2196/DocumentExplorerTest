import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException, \
    StaleElementReferenceException, ElementNotInteractableException

from utils.logs_util import DocumentExplorerLogger
from utils.document_explorer import Collections
from utils.document_explorer import Documents


class DriverUtils:
    logger = DocumentExplorerLogger()
    collection = Collections()
    document = Documents()

    def __init__(self):
        self.logger.log_enter("DriverUtils: __init__")
        self.logger.log_exit("DriverUtils: __init")

    def login(self, driver, url, username, password):
        """
        Method to login into Document Explorer Application
        :param driver: webdriver object to use
        :param url: url of document explorer application
        :param username: username for login
        :param password: password for login
        :return:
        """
        self.logger.log_enter("DriverUtils: login")

        driver.get(url)
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("kc-login").click()

        self.logger.log_exit("DriverUtils: login")

    def click_button(self, driver, button_css):
        self.logger.log_enter("DriverUtils: click_button")

        # click on button
        try:
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_css)))
            self.logger.log_debug("DriverUtils: click_button button {}".format(button))
            if button:
                button.click()
        except TimeoutException as e:
            self.logger.log_debug("DriverUtils: click_button Exception: {}".format(e))

        self.logger.log_exit("DriverUtils: click_button")

    def get_collection_search_element(self, driver):
        """
        Method to get collection search bar element in the UI.
        :param driver: webdriver object to use
        :return: Collection Search Element Object
        """
        self.logger.log_enter("DriverUtils: get_collection_search_element")

        search_element = None
        try:
            search_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, self.collection.collection_search_input_css)))
            self.logger.log_debug("DriverUtils: get_collection_search_element search_element: {}".format(
                search_element))
        except NoSuchElementException as e:
            self.logger.log_error("DriverUtils: search_document Exception: {}".format(e))

        self.logger.log_exit("DriverUtils: get_collection_search_element")
        return search_element

    def parse_table(self, driver, table_css):
        """
        Method to parse the table in the UI.
        :param driver: webdriver object to use
        :param table_css: CSS selector for table element
        :return: (Dict) dictionary of parsed element in the table
        """
        self.logger.log_enter("DriverUtils: parse_table")

        table_contents = {}
        try:
            # TODO: Use better logic to wait for table items to get loaded instead of static sleep
            time.sleep(10)
            table = driver.find_element_by_css_selector(table_css)
            self.logger.log_debug("DriverUtils: parse_table table: {}".format(table))

            if table:
                rows = table.find_elements(By.TAG_NAME, "tr")
                for row in rows:
                    self.logger.log_info("DriverUtils: parse_table row: {}".format(row.text))
                    cols = row.find_elements(By.TAG_NAME, "td")
                    columns_list = []
                    for col in cols:
                        self.logger.log_info("DriverUtils: parse_table col: {}".format(col.text))
                        columns_list.append(col.text)
                    table_contents[row.text] = columns_list
        except NoSuchElementException as e:
            self.logger.log_error("DriverUtils: parse_table Exception: {}".format(e))
        except StaleElementReferenceException as e:
            self.logger.log_error("DriverUtils: parse_table Exception: {}".format(e))

        self.logger.log_exit("DriverUtils: parse_table")
        return table_contents

    def change_collection_page_size(self, driver, page_size):
        """
        Method to change collection table page size
        :param driver: webdriver object to use
        :param page_size: the page size value [5, 10, 15, 20, 25, 50, 75, 100]
        :return:
        """
        self.logger.log_enter("DriverUtils: change_collection_page_size")

        try:
            time.sleep(5)
            collection_page_size_select = Select(driver.find_element_by_css_selector(
                self.collection.collection_table_page_size_css))
            self.logger.log_debug(
                "DriverUtils: change_collection_page_size collection_page_size_select: {}".format(
                    collection_page_size_select))
            if collection_page_size_select:
                collection_page_size_select.select_by_value(page_size)
        except NoSuchElementException as e:
            self.logger.log_error("DriverUtils: change_collection_page_size Exception: {}".format(e))

        self.logger.log_exit("DriverUtils: change_collection_page_size")

    def create_collection(self, driver, collection_name, expected_error=None):
        """
        Method to create a collection
        :param driver: webdriver object to use
        :param collection_name: name of the collection to create
        :param expected_error: expected error message
        :return:
        """
        self.logger.log_enter("DriverUtils: create_collection")

        try:
            # wait for some time to page to get load
            time.sleep(10)
            # click on create collection button
            self.click_button(driver, self.collection.collection_create_button_css)

            # enter the collection name
            text_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, self.collection.collection_name_text_box_css)))
            self.logger.log_debug("DriverUtils: create_collection text_box {}".format(text_box))
            if text_box:
                text_box.send_keys(collection_name)

            # click on submit button
            self.click_button(driver, self.collection.collection_create_submit_button_css)

            # parse error message box text
            error_message_para = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, self.collection.collection_create_error_para_css)))
            self.logger.log_debug("DriverUtils: create_collection error_message_para {}".format(error_message_para))
            if error_message_para:
                if expected_error:
                    # validate error message with expected error
                    assert expected_error == error_message_para.text

                # click on cancel button to close the collection frame
                cancel_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, self.collection.collection_cancel_button_css)))
                self.logger.log_debug("DriverUtils: create_collection cancel_button {}".format(cancel_button))
                if cancel_button:
                    cancel_button.click()

        except NoSuchElementException as e:
            self.logger.log_error("DriverUtils: create_collection Exception: {}".format(e))
        except ElementClickInterceptedException as e:
            self.logger.log_error("DriverUtils: create_collection Exception: {}".format(e))
        except TimeoutException as e:
            self.logger.log_error("DriverUtils: create_collection Exception: {}".format(e))

        self.logger.log_exit("DriverUtils: create_collection")

    def search_collection(self, driver, collection_name):
        """
        Method to search a collection
        :param driver: webdriver object to use
        :param collection_name: name of the collection to search
        :return: (List) list of collection names
        """
        self.logger.log_enter("DriverUtils: search_collection")

        results = {}
        try:
            # get collection search bar
            search_element = self.get_collection_search_element(driver)
            if search_element:
                # clear the search input in collection search bar
                search_element.clear()
                time.sleep(5)
                # input collection name
                search_element.send_keys(collection_name)
                # parse results from collection table
                results = self.parse_table(driver, self.collection.collection_table_css)
        except NoSuchElementException as e:
            self.logger.log_error("DriverUtils: search_collection Exception: {}".format(e))
        except TimeoutException as e:
            self.logger.log_error("DriverUtils: search_collection Exception: {}".format(e))

        self.logger.log_exit("DriverUtils: search_collection")
        return self.collection.get_name_list(results)

    def sort_collection(self, driver, sort_order):
        """
        Method to sort the collection list
        :param driver: webdriver to use
        :param sort_order: the order of sort [ascending, descending, default]
        :return: (List) list of collection names
        """
        self.logger.log_enter("DriverUtils: sort_collection")

        results = None
        try:
            # TODO: Use better logic to parse all collections by parsing each page
            self.change_collection_page_size(driver, "100")
            # get collection sort button
            collection_sort_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, self.collection.collection_table_sort_css)))
            self.logger.log_debug(
                "DriverUtils: sort_collection collection_sort_button: {}".format(collection_sort_button))

            # TODO: Click on sort button only update table, after scrolling into table or clicking on screen
            if collection_sort_button:
                time.sleep(5)
                if sort_order == "ascending":
                    # click once for ascending
                    collection_sort_button.click()
                elif sort_order == "descending":
                    # click twice for descending
                    collection_sort_button.click()
                    collection_sort_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, self.collection.collection_table_sort_css)))
                    time.sleep(5)
                    collection_sort_button.click()

            # parse results from collection table
            results = self.parse_table(driver, self.collection.collection_table_css)

        except NoSuchElementException as e:
            self.logger.log_error("DriverUtils: sort_collection Exception: {}".format(e))
        except ElementClickInterceptedException as e:
            self.logger.log_error("DriverUtils: sort_collection Exception: {}".format(e))
        except StaleElementReferenceException as e:
            self.logger.log_error("DriverUtils: sort_collection Exception: {}".format(e))
        finally:
            try:
                # reset collection sort button state
                # get collection sort button
                collection_sort_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, self.collection.collection_table_sort_css)))
                if collection_sort_button:
                    time.sleep(5)
                    if sort_order == "ascending":
                        # click twice for ascending
                        collection_sort_button.click()
                        collection_sort_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                            By.CSS_SELECTOR, self.collection.collection_table_sort_css)))
                        time.sleep(5)
                        collection_sort_button.click()
                    elif sort_order == "descending":
                        # click once for descending
                        collection_sort_button.click()
            except NoSuchElementException as e:
                self.logger.log_error("DriverUtils: sort_collection finally Exception: {}".format(e))
            except ElementClickInterceptedException as e:
                self.logger.log_error("DriverUtils: sort_collection finally Exception: {}".format(e))

        self.logger.log_exit("DriverUtils: sort_collection")
        return self.collection.get_name_list(results)

    def select_collection_for_document(self, driver, search_element, collection_name):
        """
        Method to select a collection element for doing operations on documents
        :param driver: webdriver to use
        :param search_element: collection search bar element
        :param collection_name: name of the collection to select
        :return:
        """
        self.logger.log_enter("DriverUtils: select_collection_for_document")

        try:
            if search_element:
                # input collection names in collection search bar
                search_element.clear()
                time.sleep(5)
                search_element.send_keys(collection_name)
                time.sleep(5)
                collection_table = driver.find_element_by_css_selector(self.collection.collection_table_css)
                self.logger.log_debug(
                    "DriverUtils: select_collection_for_document collection_table: {}".format(collection_table))

                if collection_table:
                    # click on collection name row
                    rows = collection_table.find_elements(By.TAG_NAME, "tr")
                    rows[0].find_elements(By.TAG_NAME, "td")[0].click()

        except NoSuchElementException as e:
            self.logger.log_error("DriverUtils: select_collection_for_document Exception: {}".format(e))
        except ElementClickInterceptedException as e:
            self.logger.log_error("DriverUtils: select_collection_for_document Exception: {}".format(e))
        except TimeoutException as e:
            self.logger.log_error("DriverUtils: select_collection_for_document Exception: {}".format(e))
        except ElementNotInteractableException as e:
            self.logger.log_error("DriverUtils: select_collection_for_document Exception: {}".format(e))

        self.logger.log_exit("DriverUtils: select_collection_for_document")

    def wait_for_document_upload(self, driver):
        """
        Method to wait for document upload operation completion.
        :param driver: webdriver object to use
        :return: (string) document upload operation message
        """
        self.logger.log_enter("DriverUtils: wait_for_document_upload")
        upload_result = None
        try:
            upload_status = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, self.document.document_upload_status_css)))
            self.logger.log_debug("DriverUtils: wait_for_document_upload upload_status {}".format(upload_status))

            wait_poll_count = 10
            wait_sleep_time = 3
            # poll for 30 secs to check document upload status
            for i in range(wait_poll_count):
                if self.document.document_upload_finished_msg not in upload_status.text:
                    time.sleep(wait_sleep_time)
                else:
                    break

            hover = ActionChains(driver).move_to_element(upload_status)
            hover.perform()
            upload_floating = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, self.document.document_upload_floating_css)))
            self.logger.log_debug("DriverUtils: wait_for_document_upload upload_floating {}".format(upload_floating))
            self.logger.log_info("DriverUtils: wait_for_document_upload upload_floating text {}".format(
                upload_floating.text))
            upload_result = upload_floating.text

            # click on clear_finished button
            clear_finished = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, self.document.document_clear_finished_css)))
            self.logger.log_debug("DriverUtils: wait_for_document_upload clear_finished {}".format(clear_finished))
            clear_finished.click()
        except NoSuchElementException as e:
            self.logger.log_error("DriverUtils: wait_for_document_upload Exception: {}".format(e))

        self.logger.log_exit("DriverUtils: wait_for_document_upload")
        return upload_result.split('\n')[-1]

    def upload_document(self, driver, collection_name, document_path, expected_error=None):
        """
        Method to upload document in a collection
        :param driver: webdriver to use
        :param collection_name: name of the collection to use
        :param document_path: the local path of the document file to upload
        :param expected_error: expected error message
        :return:
        """
        self.logger.log_enter("DriverUtils: upload_document")
        time.sleep(10)
        # get collection search bar element
        search_element = self.get_collection_search_element(driver)
        try:
            # select collection element
            self.select_collection_for_document(driver, search_element, collection_name)
            upload_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, self.document.document_upload_button_css)))
            self.logger.log_debug("DriverUtils: upload_document upload_button {}".format(upload_button))

            file_input = driver.find_element_by_css_selector(self.document.document_file_input_css)
            self.logger.log_debug("DriverUtils: upload_document file_input {}".format(file_input))

            if upload_button:
                # send file path to file input element
                file_input.send_keys(document_path)
                # click on upload button
                upload_button.click()
        # collection create button going in stale state
        except StaleElementReferenceException as e:
            self.logger.log_error("DriverUtils: upload_document Exception: {}".format(e))
            time.sleep(5)
            # wait for document upload operation
            upload_result = self.wait_for_document_upload(driver)
            self.logger.log_info("DriverUtils: upload_document upload_result: {}".format(upload_result))
            if expected_error:
                assert expected_error == upload_result
            else:
                assert self.document.document_upload_success_msg == upload_result

        except NoSuchElementException as e:
            self.logger.log_error("DriverUtils: upload_document Exception: {}".format(e))
        except ElementClickInterceptedException as e:
            self.logger.log_error("DriverUtils: upload_document Exception: {}".format(e))
        except TimeoutException as e:
            self.logger.log_error("DriverUtils: upload_document Exception: {}".format(e))
        except ElementNotInteractableException as e:
            self.logger.log_error("DriverUtils: upload_document Exception: {}".format(e))
        finally:
            driver.refresh()
            time.sleep(10)

        self.logger.log_exit("DriverUtils: upload_document")

    def search_document(self, driver, collection_name, document_name):
        """
        Method to search a document in a collection
        :param driver: webdriver object to use
        :param collection_name: name of the collection
        :param document_name: name of the document
        :return: (List) list of document names
        """
        self.logger.log_enter("DriverUtils: search_document")

        results = {}
        # get collection search bar element
        search_element = self.get_collection_search_element(driver)
        try:
            # select collection
            self.select_collection_for_document(driver, search_element, collection_name)
            doc_search_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, self.document.document_search_css)))
            self.logger.log_debug("DriverUtils: search_document upload_button {}".format(doc_search_element))

            if doc_search_element:
                # clear document search bar
                doc_search_element.clear()
                time.sleep(5)
                # input document name in document search bar
                doc_search_element.send_keys(document_name)
                # parse results from document table
                results = self.parse_table(driver, self.document.document_table_css)
        except NoSuchElementException as e:
            self.logger.log_error("DriverUtils: search_document Exception: {}".format(e))
        except ElementClickInterceptedException as e:
            self.logger.log_error("DriverUtils: search_document Exception: {}".format(e))
        except TimeoutException as e:
            self.logger.log_error("DriverUtils: search_document Exception: {}".format(e))
        finally:
            driver.refresh()
            time.sleep(10)

        self.logger.log_exit("DriverUtils: search_document")
        return self.document.get_name_list(results, col_num=1)
