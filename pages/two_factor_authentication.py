from pypom import Page
from selenium.webdriver.common.by import By


class TwoFactorAuthentication(Page):
    _github_passcode_field_locator = (By.CSS_SELECTOR, 'input[id="otp"]')
    _github_enter_passcode_button_locator = (By.CSS_SELECTOR, '.btn-primary')

    def enter_github_passcode(self, passcode):
        self.find_element(*self._github_passcode_field_locator).send_keys(passcode)
        self.find_element(*self._github_enter_passcode_button_locator).click()
