from selenium.webdriver.common.by import By
from helper.selenium_helper import Selenium_Helper


class LoginPage(Selenium_Helper):
    def __init__(self, driver):
        super().__init__(driver)

    username_element = (By.XPATH, '//input[@name="username"]')
    password_element = (By.XPATH, '//input[@name="password"]')
    login_element = (By.XPATH, '//button[@type="submit"]')

    def login(self, username, password):
        self.element_enter(locator=self.username_element, text=username)
        self.element_enter(locator=self.password_element, text=password)
        self.element_click(locator=self.login_element)

    def check_title(self, title):
        self.title_check(title)

