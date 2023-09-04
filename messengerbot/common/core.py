from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import schedule


DELAY = 10.0  # seconds
LOGIN_URL = "https://m.facebook.com/login.php"
M_HEAD = "https://m."
WWW_HEAD = "https://www."
MES_IMG_CSS = "img[src*='https://static.xx.fbcdn.net/rsrc.php/v3/y9/r/YjBUcSAL8TC.png']"


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
            self.driver = webdriver.Chrome()
        elif browser == "Firefox":
            self.driver = webdriver.Firefox()

    def login(self) -> None:
        """Controlling Selenium browser object login FB using input data."""
        self.go_target_url(LOGIN_URL)

        # Wait until the input box appear
        email_input = WebDriverWait(self.driver, DELAY).until(
            EC.presence_of_element_located((By.ID, "m_login_email"))
        )
        # email_element = self.driver.find_element(By.ID, "m_login_email")
        email_input.send_keys(self.email)  # Give keyboard input

        password_input = self.driver.find_element(By.ID, "m_login_password")
        password_input.send_keys(self.password)  # Give password as input too
        password_input.send_keys(Keys.RETURN)

        # Wait until the confirm button is loaded
        WebDriverWait(self.driver, DELAY).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "a[href^='/login/save-device/cancel/?flow=interstitial_nux&nux_source=regular_login']",
                )
            ),
            "Cannot locate confirm button!",
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
        try:
            send_message_button = WebDriverWait(
                self.driver, DELAY, ignored_exceptions=StaleElementReferenceException
            ).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        MES_IMG_CSS,
                    )
                ),
                "Cannot locate send message button!",
            )
            self.driver.implicitly_wait(DELAY)
            ActionChains(self.driver).move_to_element(send_message_button).send_keys(
                Keys.TAB
            ).click().perform()
        except Exception as error:
            print("An exception occurred:", type(error).__name__, "-", error)

        # Wait until the input text box appear
        try:
            # self.driver.implicitly_wait(DELAY)
            text_box = WebDriverWait(self.driver, DELAY).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='訊息']")),
                "Cannot locate input text box!",
            )
            self.driver.implicitly_wait(DELAY)
            ActionChains(self.driver).move_to_element(text_box).click().send_keys(
                text
            ).perform()
        except Exception as error:
            print("An exception occurred:", type(error).__name__, "-", error)

    def send_text(self) -> type[schedule.CancelJob]:
        """After the text are sent, return a schedule.CancelJob to tell the job is done.

        Returns:
            schedule.CancelJob: A object that tells schedule object it's time to cancel the job.
        """
        # Click the send button because enter doesn't work
        send_button = self.driver.find_element(
            By.CSS_SELECTOR, "path[d*='M16.6915026']"
        )
        send_button.click()

        return schedule.CancelJob
