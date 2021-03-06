from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import schedule


DELAY = 5  # seconds
LOGIN_URL = "https://m.facebook.com/login.php"
M_HEAD = "https://m."
WWW_HEAD = "https://www."


class FacebookMessageBot:
    def __init__(self, email: str, password: str, browser="Firefox") -> None:
        """Initial function for FacebookMessageBot.

        Args:
            email (str): The email account used to login.
            password (str): The password for the email.
            browser (str, optional): The name of the browser. Defaults to "Firefox".
        """
        self.email = email
        self.password = password
        if browser == "Chrome":
            self.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install()
            )
        elif browser == "Firefox":
            self.driver = webdriver.Firefox(
                executable_path=GeckoDriverManager().install()
            )

    def login(self) -> None:
        """Controlling Selenium browser object login FB using input data."""
        self.go_target_url(LOGIN_URL)

        # Wait until the input box appear
        WebDriverWait(self.driver, DELAY).until(
            EC.presence_of_element_located((By.ID, "m_login_email"))
        )
        email_element = self.driver.find_element_by_id("m_login_email")
        email_element.send_keys(self.email)  # Give keyboard input

        password_element = self.driver.find_element_by_id("m_login_password")
        password_element.send_keys(self.password)  # Give password as input too
        password_element.send_keys(Keys.RETURN)

        # Wait until the confirm button is loaded
        WebDriverWait(self.driver, DELAY).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "a[href^='/login/save-device/cancel/?flow=interstitial_nux&nux_source=regular_login']",
                )
            )
        )

    def go_target_url(self, target_url: str) -> None:
        """Controlling Selenium browser go to the target url with proper wait function.

        Args:
            target_url (str): The target url that webdriver will go to.
        """
        # Replace https://www to https://m
        if target_url.startswith(WWW_HEAD):
            target_url = M_HEAD + target_url[len(WWW_HEAD) :]

        WebDriverWait(self.driver, DELAY).until(EC.url_changes(target_url))
        self.driver.get(target_url)

    def fill_in_text(self, text: str) -> None:
        """Controlling Selenium browser input the text contents to messenger chat box.

        Args:
            text (str): The text message that user wants to send.
        """
        # Wait until "send message" button appear and is clickable
        WebDriverWait(self.driver, DELAY).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "a[href^='/messages/thread/']",
                )
            )
        )
        try:
            send_message_button = self.driver.find_element_by_css_selector(
                "a[href^='/messages/thread/']"
            )
            send_message_button.click()
        except Exception as e:
            print(e)

        # Wait until the input text box appear
        WebDriverWait(self.driver, DELAY).until(
            EC.presence_of_element_located((By.ID, "composerInput"))
        )
        try:
            text_box = self.driver.find_element_by_id("composerInput")
            text_box.send_keys(text)
        except Exception as e:
            print(e)

    def send_text(self) -> type[schedule.CancelJob]:
        """After the text are sent, return a schedule.CancelJob to tell the job is done.

        Returns:
            schedule.CancelJob: A object that tells schedule object it's time to cancel the job.
        """
        # Click the send button because enter doesn't work
        send_button = self.driver.find_element_by_css_selector("button[name='send']")
        send_button.click()

        return schedule.CancelJob
