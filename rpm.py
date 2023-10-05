"""Generates a Password off a Master Key and Reference Key"""
import sys
import random
from getpass import getpass
import hashlib
from time import sleep
import pyperclip as pc

# Rich
from rich.panel import Panel
from rich.theme import Theme
from rich.style import Style
from rich.console import Console
from rich.traceback import install

install()
custom_theme = Theme(
    {
        "primary": Style(color="#4050c5"),
        "secondary": Style(color="#bcd6e6"),
        "accent": Style(color="#4e91ba"),
    }
)
console = Console(theme=custom_theme)

# Config
from utils.config import Config

c = Config().config


def help_msg():
    """Prints a list of commands."""

    console.print(
        Panel.fit(
            """[secondary]--help[/]
└ shows this page

[secondary]--hide-all[/]
└ Disables terminal input viewing for both password and key.

[secondary]--hide-pass[/]
└ Disables terminal input viewing for the password.

[secondary]--hide-key[/]
└ Disables terminal input viewing for the key.""",
            title="[accent]Commands Help[/]",
            border_style="primary",
        )
    )
    sys.exit(0)


def startup():
    """Prints a startup message."""

    console.print(
        Panel.fit(
            f"* run {c['Name']} --help\nfor additional options",
            title=f"[accent]RPMv{c['Version']}[/]",
            border_style="primary",
        )
    )


def get_secure(key_type, hide, double):
    """Function for prompting and getting secure values,
    dynamic based on function inputs."""

    checker_list = []

    if double:
        iterations = 2
    else:
        iterations = 1

    for _ in range(iterations):
        secure_value = str(console.input(f"{key_type}: ", password=hide))
        if secure_value == "":
            console.log(
                "[red]ERRORx1[/]: [accent]ValueError[/], Required field left blank."
            )
            sys.exit(1)

        checker_list.append(secure_value)

    if iterations == 2:
        if checker_list[0] == checker_list[1]:
            return secure_value
        else:
            console.log("[red]ERRORx1[/]: Double-checker failed.")
            sys.exit(2)
    else:
        return secure_value


def promptUser(hide, double):
    """Prompts the user for values used by the rest of the script."""

    global masterPassword, referenceKey, passwordLength, showPassword

    masterPassword = get_secure("∙ [accent]Master Password[/]", hide, double)
    referenceKey = get_secure("∙ [accent]Reference Key[/]", hide, double)
    passwordLength = console.input("∙ [accent]Output Len[/] [secondary](22)[/]: ")
    if passwordLength == "":
        passwordLength = 22
    else:
        try:
            passwordLength = int(passwordLength)
        except ValueError:
            console.log(
                "[red]ERRORx1[/]: [accent]ValueError[/], An integer was not entered."
            )
            sys.exit(1)

    showPassword = str(console.input(f"∙ [accent]Show Output[/] [secondary](y/N)[/]: "))
    if showPassword == "y" or showPassword == "Y":
        showPassword = True
    elif showPassword == "n" or showPassword == "N":
        showPassword = False
    elif showPassword == "" or showPassword == " ":
        showPassword = False
    else:
        console.log(
            "[red]ERRORx1[/]: [accent]ValueError[/], Invalid input to y/N question."
        )
        sys.exit(1)


def generator(seed, length):
    """Generates a password based on the values passed to this function."""

    random.seed(seed)

    characters = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=~"
    )

    hasher = hashlib.sha256()

    password = ""
    while len(password) < length:
        data = str(random.random()).encode() + seed.encode()
        hasher.update(data)
        digest = hasher.digest()
        for byte in digest:
            if len(password) >= length:
                break
            index = byte % len(characters)
            password += characters[index]

    return password


def rpm(hide: bool, double: bool):
    """The core of the code."""

    # Prompts the user for values
    promptUser(hide, double)

    # Generates Password
    pw = generator((masterPassword + referenceKey), passwordLength)

    # Either prints or copies the password
    if showPassword:
        console.print(
            Panel.fit(
                pw,
                title=f"[accent]{c['Name']}v{c['Version']}[/]",
                border_style="primary",
            )
        )
    else:
        if c["ClipboardClear"]:
            pc.copy(pw)
            console.print(f"┌ [primary]Copied to Clipboard[/]! [secondary]Clearing in {c['ClipboardTimer']} second(s)[/].")
            sleep(c["ClipboardTimer"])
            pc.copy("// Cleared //")
            console.print("└ [primary]Clipboard Cleared[/]!")
        else:
            pc.copy(pw)
            console.print("∙ [primary]Copied to Clipboard[/]!")
            
        sys.exit(0)


if __name__ == "__main__":
    startup()

    # Sets Defaults
    hideInput = False
    doubleAsk = False

    # Checks arguments and gets user values
    for arg_index in sys.argv[1:]:
        try:
            if "--hide" in arg_index:
                hideInput = True
            elif "--help" in arg_index:
                help_msg()
                break
            elif "--double" in arg_index:
                doubleAsk = True
        except IndexError:
            pass

    rpm(hideInput, doubleAsk)
