import PySimpleGUI as sg


# The settings file will be located at root folder
SETTINGS = sg.UserSettings(filename="MessengerBot.json", path=".")


def make_window(theme: str) -> sg.Window:
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
        [sg.Input(SETTINGS.get("-input mail-", ""), key="-INPUT MAIL-")],
        [sg.Text(size=(40, 1), key="-OUTPUT MAIL-")],

        # --------------------
        # Password
        # --------------------
        [sg.Text("Your password :")],
        [sg.Input(SETTINGS.get("-input password-", ""), key="-INPUT PASSWORD-")],
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
        [sg.Input(SETTINGS.get("-input url-", ""), key="-INPUT URL-")],
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
                default_value=SETTINGS.get("-combo hour-", ""),
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
                default_value=SETTINGS.get("-combo minute-", ""),
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
                default_value=SETTINGS.get("-combo second-", ""),
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
                SETTINGS.get("-input message-", ""),
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
