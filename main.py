from datetime import datetime

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
THEME = "Dark"

# The settings file will be in the same folder as this program
settings = sg.UserSettings(path=".")


class FacebookMessageBot:
    def __init__(self, email: str, password: str, browser="Firefox") -> None:
        """
        | Initialization of creating Messenger bot instance.
        """
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

    def login(self) -> None:
        """
        | Controling Selenium browser object login FB using input data.
        """
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
        """
        | Controling Selenium browser go to the target url with proper wait function.
        """
        # Replace https://www to https://m
        if target_url.startswith("https://www."):
            target_url = "https://m." + target_url[12:]

        WebDriverWait(self.driver, DELAY).until(EC.url_changes(target_url))
        self.driver.get(target_url)

    def fill_in_text(self, text: str) -> None:
        """
        | Controling Selenium browser input the text contents to chat box.
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

        text_box.send_keys(text)

    def send_text(self) -> schedule.CancelJob:
        """
        | After the text contents are sent, return a schedule.CancelJob to tell the job is done.
        """
        # Click the send button because enter doesn't work
        send_button = self.driver.find_element_by_css_selector("button[name='send']")
        send_button.click()

        return schedule.CancelJob


def make_window(theme: str) -> None:
    """
    | Call this function to create the custom PySimpleGUI window.
    """
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
            sg.Combo(
                values=(
                    "00",
                    "01",
                    "02",
                    "03",
                    "04",
                    "05",
                    "06",
                    "07",
                    "08",
                    "09",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                ),
                default_value=settings.get("-combo hour-", ""),
                readonly=True,
                k="-COMBO HOUR-",
            ),
            sg.Text(":"),
            sg.Combo(
                values=(
                    "00",
                    "01",
                    "02",
                    "03",
                    "04",
                    "05",
                    "06",
                    "07",
                    "08",
                    "09",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                    "31",
                    "32",
                    "33",
                    "34",
                    "35",
                    "36",
                    "37",
                    "38",
                    "39",
                    "40",
                    "41",
                    "42",
                    "43",
                    "44",
                    "45",
                    "46",
                    "47",
                    "48",
                    "49",
                    "50",
                    "51",
                    "52",
                    "53",
                    "54",
                    "55",
                    "56",
                    "57",
                    "58",
                    "59",
                ),
                default_value=settings.get("-combo minute-", ""),
                readonly=True,
                k="-COMBO MINUTE-",
            ),
            sg.Text(":"),
            sg.Combo(
                values=(
                    "00",
                    "01",
                    "02",
                    "03",
                    "04",
                    "05",
                    "06",
                    "07",
                    "08",
                    "09",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                    "31",
                    "32",
                    "33",
                    "34",
                    "35",
                    "36",
                    "37",
                    "38",
                    "39",
                    "40",
                    "41",
                    "42",
                    "43",
                    "44",
                    "45",
                    "46",
                    "47",
                    "48",
                    "49",
                    "50",
                    "51",
                    "52",
                    "53",
                    "54",
                    "55",
                    "56",
                    "57",
                    "58",
                    "59",
                ),
                default_value=settings.get("-combo second-", ""),
                readonly=True,
                k="-COMBO SECOND-",
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


def update_input_status(content: str, window_output: str, warning_text: str) -> None:
    """
    | Everytime when user click "Ok" button will call this function to update the status string of input columns.
    """
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
                settings["-combo hour-"] = values["-COMBO HOUR-"]
                settings["-combo minute-"] = values["-COMBO MINUTE-"]
                settings["-combo second-"] = values["-COMBO SECOND-"]
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

    if values["-R CURRENT-"]:  # If choose Current radio option
        fb_bot.send_text()
    else:  # If choose Specify time radio option

        # Combine time input into correct format (ex: 21:10:02)
        input_time_string = (
            values["-COMBO HOUR-"]
            + ":"
            + values["-COMBO MINUTE-"]
            + ":"
            + values["-COMBO SECOND-"]
        )

        # Create pending schedule task
        schedule.every().day.at(
            datetime.strptime(input_time_string, "%H:%M:%S").strftime("%H:%M:%S")
        ).do(fb_bot.send_text)

        # Check if any pending schedule every second until no more schedule
        while len(schedule.default_scheduler.jobs) > 0:
            schedule.run_pending()
            time.sleep(1)

    fb_bot.driver.quit()
    sys.exit()


if __name__ == "__main__":
    main()
