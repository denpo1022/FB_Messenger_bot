from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import PySimpleGUI as sg
import schedule
import sys
import time


LOGIN_URL = "https://m.facebook.com/login.php"
DELAY = 5  # seconds
HAVE_DONE = False  # trigger variable
THEME = "Dark"

# The settings file will be in the same folder as this program
settings = sg.UserSettings(path=".")


class FacebookMessageBot:
    def __init__(self, email, password, browser="Firefox"):
        # Store credentials for login
        self.email = email
        self.password = password
        if browser == "Chrome":
            # Use chrome
            self.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install()
            )
        elif browser == "Firefox":
            # Set it to Firefox
            self.driver = webdriver.Firefox(
                executable_path=GeckoDriverManager().install()
            )

    def login(self):
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

        time.sleep(DELAY)

    def go_target_url(self, target_url):
        WebDriverWait(self.driver, DELAY).until(EC.url_changes(target_url))
        self.driver.get(target_url)

    def fill_in_text(self, text):
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
        except Exception as e:
            print(e)

        send_message_button.click()

        # Wait until the input text box appear
        WebDriverWait(self.driver, DELAY).until(
            EC.presence_of_element_located((By.ID, "composerInput"))
        )
        try:
            text_box = self.driver.find_element_by_id("composerInput")
        except Exception as e:
            print(e)

        current_time = " Current time is " + datetime.now().strftime("%H:%M:%S")
        text += current_time
        text_box.send_keys(text)

    def send_text(self):
        # Click the send button because enter doesn't work
        send_button = self.driver.find_element_by_css_selector("button[name='send']")
        send_button.click()

        global HAVE_DONE
        HAVE_DONE = True


def make_window(theme):
    sg.theme(theme)

    # Input layout declaration
    input_layout = [
        # --------------------
        # Account
        # --------------------
        [sg.Text("Your Facebook account :")],
        [sg.Input(settings.get("-input mail-", ""), key="-INPUT MAIL-")],
        [sg.Text(size=(40, 1), key="-OUTPUT MAIL-")],
        # --------------------
        # Password
        # --------------------
        [sg.Text("Your password :")],
        [sg.Input(settings.get("-input password-", ""), key="-INPUT PASSWORD-")],
        [sg.Text(size=(40, 1), key="-OUTPUT PASSWORD-")],
        # --------------------
        # Browser
        # --------------------
        [sg.Text("Select your prefer browser :")],
        [
            sg.Combo(
                values=("Firefox", "Chrome"),
                default_value="Firefox",
                readonly=True,
                k="-COMBO BROWSER-",
            )
        ],
        # --------------------
        # Url
        # --------------------
        [sg.Text("Input target url :")],
        [sg.Input(settings.get("-input url-", ""), key="-INPUT URL-")],
        [sg.Text(size=(40, 1), key="-OUTPUT URL-")],
        # --------------------
        # Time
        # --------------------
        [sg.Text("Choose message sending time option :")],
        [
            sg.Radio(
                "Right now",
                "RadioTime",
                default=True,
                size=(40, 1),
                k="-R CURRENT-",
            )
        ],
        [
            sg.Radio(
                "At specify time",
                "RadioTime",
                default=False,
                size=(40, 1),
                k="-R SPECIFY-",
            )
        ],
        [
            sg.Input(key="-INPUT TIME-", size=(20, 1)),
            sg.CalendarButton(
                "Cal Format %m-%d Jan 2020",
                target="-INPUT TIME-",
                format="%m-%d",
            ),
        ],
        # --------------------
        # Message
        # --------------------
        [sg.Text("Input your message :")],
        [
            sg.Multiline(
                settings.get("-input message-", ""),
                size=(45, 5),
                k="-MLINE MESSAGE-",
            )
        ],
        [sg.Text(size=(40, 1), key="-OUTPUT MESSAGE-")],
        # --------------------
        # Ok button
        # --------------------
        [sg.Button("Ok")],
    ]

    layout = [[sg.Column(input_layout)]]

    return sg.Window("FB Messenger Bot", layout)


def update_input_status(content, window_output, warning_text):
    if not content:
        window_output.update(warning_text, text_color="red")
    else:
        window_output.update("")


def declare_input_dict(input_name, values, window):
    return {
        "value": values["-INPUT " + input_name + "-"],
        "output": window["-OUTPUT " + input_name + "-"],
        "warning": input_name + " cannot be empty!",
    }


def main():
    global HAVE_DONE

    # Create the GUI window
    window = make_window(sg.theme(THEME))

    while True:  # Loop for listening GUI events
        event, values = window.read()
        if event == "Ok":  # If press Ok button

            # Update input values from user
            EMAIL = {
                "value": values["-INPUT MAIL-"],
                "output": window["-OUTPUT MAIL-"],
                "warning": "Mail cannot be empty!",
            }
            PASSWORD = {
                "value": values["-INPUT PASSWORD-"],
                "output": window["-OUTPUT PASSWORD-"],
                "warning": "Password cannot be empty!",
            }
            TARGET_URL = {
                "value": values["-INPUT URL-"],
                "output": window["-OUTPUT URL-"],
                "warning": "Url cannot be empty!",
            }
            MESSAGE = {
                "value": values["-MLINE MESSAGE-"],
                "output": window["-OUTPUT MESSAGE-"],
                "warning": "Message cannot be empty!",
            }
            INPUTS = [EMAIL, PASSWORD, TARGET_URL, MESSAGE]
            BROWSER = values["-COMBO BROWSER-"]

            if (  # Check necessary inputs are not null
                EMAIL["value"]
                and PASSWORD["value"]
                and TARGET_URL["value"]
                and MESSAGE["value"]
            ):
                # Storing input information for next time
                settings["-input mail-"] = values["-INPUT MAIL-"]
                settings["-input password-"] = values["-INPUT PASSWORD-"]
                settings["-input url-"] = values["-INPUT URL-"]
                settings["-input message-"] = values["-MLINE MESSAGE-"]
                break  # If none of the inputs is null, break from loop

            for INPUT in INPUTS:  # Update the warning output
                update_input_status(INPUT["value"], INPUT["output"], INPUT["warning"])

        # If press X on the window top right corner
        elif event == sg.WIN_CLOSED:
            sys.exit()

    window.close()

    # Get your login credentials from the input boxes
    fb_bot = FacebookMessageBot(
        email=EMAIL["value"], password=PASSWORD["value"], browser=BROWSER
    )
    fb_bot.login()
    fb_bot.go_target_url(TARGET_URL["value"])
    fb_bot.fill_in_text(MESSAGE["value"])

    schedule.every().day.at(
        (datetime.now() + timedelta(seconds=5)).strftime("%H:%M:%S")
    ).do(fb_bot.send_text)

    global HAVE_DONE
    while True:
        schedule.run_pending()
        time.sleep(1)
        if HAVE_DONE:
            fb_bot.driver.quit()
            sys.exit()


if __name__ == "__main__":
    main()
