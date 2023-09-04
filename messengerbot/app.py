from datetime import datetime

from messengerbot.common.core import FacebookMessageBot
from messengerbot.window.core import make_window, update_input_status

import PySimpleGUI as sg
import schedule
import sys
import time


# Theme for PySimpleGUI
THEME = "Dark"

# The settings file will be located at root folder
SETTINGS = sg.UserSettings(filename="MessengerBot.json", path=".")


def run():
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
                SETTINGS["-input mail-"] = values["-INPUT MAIL-"]
                SETTINGS["-input password-"] = values["-INPUT PASSWORD-"]
                SETTINGS["-input url-"] = values["-INPUT URL-"]
                SETTINGS["-combo hour-"] = values["-COMBO HOUR-"]
                SETTINGS["-combo minute-"] = values["-COMBO MINUTE-"]
                SETTINGS["-combo second-"] = values["-COMBO SECOND-"]
                SETTINGS["-input message-"] = values["-MLINE MESSAGE-"]
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
