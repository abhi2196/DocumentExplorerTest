from pathlib import Path

from utils.logs_util import DocumentExplorerLogger


class DocumentExplorer:
    logger = DocumentExplorerLogger()

    def __init__(self):
        self.logger.log_enter("DocumentExplorer: __init__")

        self.app_url = "<ENTER_APP_URL>"
        self.document_explorer_url = self.app_url + '/document-explorer'

        self.test_user_name = "<ENTER_USER_NAME>"
        self.test_user_password = "<ENTER_PASSWORD>"

        self.logger.log_exit("DocumentExplorer: __init__")

    def check_if_name_exist(self, name, item_list):
        """
        Method to check if collection/document name exists in list
        :param name: name of item
        :param item_list: list of items to check the name
        :return: (boolean) True: if name exists
                         False: if name does not exists
        """
        self.logger.log_enter("DocumentExplorer: check_if_name_exist")
        self.logger.log_exit("DocumentExplorer: check_if_name_exist")
        return name in item_list

    def get_name_list(self, item_dict, col_num=0):
        """
        Method to extract list of names from parsed table data
        :param item_dict: parsed table data with row as key and list of cols as values
        :param col_num: the column number for names attribute
        :return: (List) list of names
        """
        self.logger.log_enter("DocumentExplorer: get_name_list")

        name_list = []
        if item_dict:
            for key, values in item_dict.items():
                name_list.append(values[col_num])

        self.logger.log_exit("DocumentExplorer: get_name_list")
        return name_list

    def validate_list_order(self, item_list, sort_order):
        """
        Method to validate if list is in sorted order of sort_order
        :param item_list: the list of items
        :param sort_order: sort_order type [ascending, descending]
        :return:
        """
        self.logger.log_enter("Collections: validate_list_order")

        reverse_flag = False
        if sort_order == "descending":
            reverse_flag = True

        item_list = [item.lower() for item in item_list]
        sorted_list = item_list.copy()
        self.logger.log_debug("Collections: validate_list_order: collection_list: {}".format(item_list))
        sorted_list = sorted(sorted_list, reverse=reverse_flag)
        self.logger.log_debug("Collections: validate_list_order: sorted_list: {}".format(sorted_list))

        if sort_order in ["ascending", "descending"]:
            assert item_list == sorted_list

        self.logger.log_exit("Collections: validate_list_order")


class Collections(DocumentExplorer):
    # Collection CSS elements
    collection_create_button_css = "button.picnicButtonSizeSmall.picnicButtonShapeRound.picnicButtonColorGreen." \
                                   "picnicButtonContentIconOnly.picnicButton"
    collection_name_text_box_css = ".picnicTextBox"
    collection_create_submit_button_css = ".picnicDialogSizeWidthSmall > container:nth-child(2) > " \
                                          "platform-new-collection-dialog:nth-child(1) > footer:nth-child(3) " \
                                          "> buttons:nth-child(1) > button:nth-child(1)"
    collection_create_error_para_css = ".picnicMessenger"
    collection_cancel_button_css = ".picnicDialogSizeWidthSmall > container:nth-child(2) > " \
                                   "platform-new-collection-dialog:nth-child(1) > footer:nth-child(3) > " \
                                   "buttons:nth-child(1) > button:nth-child(2)"
    collection_search_input_css = ".echoTableSelectable > header:nth-child(1) > search:nth-child(1) > " \
                                  "input:nth-child(1)"
    collection_table_css = ".echoTableHeightFull > main:nth-child(2) > table:nth-child(1)"
    collection_table_sort_css = ".tableHeaderIconSort"
    collection_table_page_size_css = "select.ng-pristine"

    # Error messages
    create_error_message = "Something went unexpectedly wrong. Try again. If the problem persists contact your " \
                           "administrator."

    def __init__(self):
        super().__init__()
        self.logger.log_enter("Collections: __init__")
        self.logger.log_exit("Collections: __init__")


class Documents(DocumentExplorer):
    # Documents CSS Elements
    document_upload_button_css = "button.picnicButtonColorGreen:nth-child(1)"
    document_file_input_css = ".picnicGridColumn3 > heading:nth-child(1) > " \
                              "echo-floating-expandable-uploader-standalone:nth-child(2) > input:nth-child(2)"
    document_search_css = "input.ng-pristine"
    document_table_css = ".picnicTableReactiveRows"
    document_clear_finished_css = ".picnicTextUnderline"
    document_upload_status_css = ".picnicGridColumn7 > chunk:nth-child(1)"
    document_upload_floating_css = ".picnicFloatingExpandableMainGapsNo"

    # Error/Success messages
    document_upload_failure_msg = "Rejected (because of type)"
    document_upload_finished_msg = "finished uploading"
    document_upload_success_msg = "Succeeded"

    # Test files
    BASEDIR = Path(__file__).resolve().parent
    pdf_test_file_name = "claim.pdf"
    pdf_test_file_2_name = "ReferenceCardForMac.pdf"
    tar_test_file_name = "geckodriver-v0.24.0-macos.tar.gz"
    pdf_test_file_path = BASEDIR.joinpath("resources/{}".format(pdf_test_file_name))
    tar_test_file_path = BASEDIR.joinpath("resources/{}".format(tar_test_file_name))

    def __init__(self):
        super().__init__()
        self.logger.log_enter("Documents: __init__")
        self.logger.log_exit("Documents: __init__")
