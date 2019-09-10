import pytest
from pathlib import Path
from selenium import webdriver
from utils.logs_util import DocumentExplorerLogger
from utils.driver_utils import DriverUtils
from utils.document_explorer import DocumentExplorer

logger = DocumentExplorerLogger()
driver_utils = DriverUtils()
document_explorer = DocumentExplorer()

BASEDIR = Path(__file__).resolve().parent

# Download latest geckodriver for your test environment, mozilla version, os type(macos, linux, windows)
# https://github.com/mozilla/geckodriver/releases
# Change this path accordingly pointing to driver path locally
gecko_driver_path = BASEDIR.joinpath("drivers/macos/geckodriver")

# Download latest chrome driver for your test environment, chrome version, os type(macos, linux, windows)
# http://chromedriver.chromium.org/downloads
# Change this path accordingly pointing to driver path locally
chrome_driver_path = BASEDIR.joinpath("drivers/macos/chromedriver")

# Fixture for Web Drivers
@pytest.fixture(params=["firefox"], scope="class")
def driver_init(request):
    """
    Fixture for initiating web driver used by selenium based on params list
    :param request:
    :return:
    """
    logger.log_enter("driver_init")
    driver = None

    if request.param == "firefox":
        driver = webdriver.Firefox(executable_path=gecko_driver_path)
    elif request.param == "chrome":
        driver = webdriver.Chrome(executable_path=chrome_driver_path)

    # login into the document explorer application
    driver_utils.login(
        driver,
        document_explorer.document_explorer_url,
        document_explorer.test_user_name,
        document_explorer.test_user_password)

    request.cls.driver = driver
    yield
    # close connection
    driver.close()
    logger.log_exit("driver_init")
