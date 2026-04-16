from pathlib import Path
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.options import Options

def pytest_setup_options():
    options = Options()
    options.binary_location = "/Users/wehi/Desktop/Google Chrome.app/Contents/MacOS/Google Chrome"
    return options