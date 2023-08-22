from conftest import *
from pages.LoginPage import LoginPage


# @pytest.mark.usefixtures("browser_setup")
@pytest.mark.usefixtures("driver")
class Test_Login:

    def setup_class(self):
        # self.driver.get(BaseUrl)
        self.login = LoginPage(self.driver)

    def test_validate_login(self):
        self.login.login(Username, Password)
        self.login.check_title("OrangeHRM1")

    def teardown_class(self):
        self.driver.quit()

