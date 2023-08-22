from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

BaseUrl = 'https://opensource-demo.orangehrmlive.com/web/index.php/auth/login'
Username = 'Admin'
Password = 'admin123'


@pytest.fixture()
def driver():
    print("1")
    global driver
    driver = webdriver.Chrome(ChromeDriverManager(version='114.0.5735.90').install())
    driver.maximize_window()
    driver.get(BaseUrl)
    driver.implicitly_wait(5)
    yield driver
    driver.close()
    driver.quit()


# @pytest.fixture(scope='class', autouse=True)
# def browser_setup(request):
#     request.cls.driver = webdriver.Chrome(ChromeDriverManager(version='114.0.5735.90').install())
#     request.cls.driver.maximize_window()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    now = datetime.now()
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # file_name = report.nodeid.replace("::", "_") + ".png"
            # file_name = report.nodeid.replace("::", "_") + ".png"
            file_name = "screenshot" + now.strftime("%S%H%d%m%Y") + ".png"
            print(file_name, type(file_name))
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    today = datetime.now()
    report_dir = Path('reports', today.strftime('%Y%m%d'))
    report_dir.mkdir(parents=True, exist_ok=True)
    pytest_html = report_dir / f"Report_{today.strftime('%Y%m%d%H%M%S')}.html"
    config.option.htmlpath = pytest_html
    config.option.self_contained_html = True


def _capture_screenshot(name):
    # print(f"Reports/{name}")
    print(driver.title)
    driver.get_screenshot_as_file(name)


def pytest_html_report_title(report):
    report.title = "OrangeHRM Test Result"


