# Gen.2

import sys
import random
from getpass import getpass
import hashlib
from time import sleep
import pyperclip as pc

version = "2"
name = f"RPMv.{version}.py"


# formatting
class f:
    l = 30  # line len

    tl = "╭"
    bl = "╰"
    tr = "╮"
    br = "╯"

    h = "─"
    v = "│"

    top = tl + l * h + tr
    bottom = bl + l * h + br


def help():
    print(
        f"""{f.top}
{f.v}   Commands Help
{f.v}   
{f.v}   --help
{f.v}    {f.bl} shows this page
{f.v}
{f.v}   --hide-all
{f.v}    {f.bl} Disables terminal input viewing for both password and key.
{f.v}
{f.v}   --hide-pass
{f.v}    {f.bl} Disables terminal input viewing for the password.
{f.v}
{f.v}   --hide-key
{f.v}    {f.bl} Disables terminal input viewing for the key.
{f.bottom}"""
    )
    sys.exit(0)


def startup():
    print(
        f"""{f.top}
{f.v}       ── Roc ────────
{f.v}       Password Manager
{f.v}       ──────── v.{version} ──
{f.v}       
{f.v}    * run {name} --help
{f.v}    for additional options
{f.bottom}"""
    )


# Prompts user for the master password and key
def promptUser(hide):
    global masterPassword, referenceKey, passwordLength, showPassword

    print(f.top)

    if hide == "All" or hide == "Pass":
        masterPassword = str(getpass(f"{f.v} Master Password: "))
        if masterPassword == "":
            print("ERRORx1: ValueError, Required field left blank.")
            sys.exit(1)
    else:
        masterPassword = str(input(f"{f.v} Master Password: "))
        if masterPassword == "":
            print("ERRORx1: ValueError, Required field left blank.")
            sys.exit(1)

    if hide == "All" or hide == "Key":
        referenceKey = str(getpass(f"{f.v} Reference Key: "))
        if referenceKey == "":
            print("ERRORx1: ValueError, Required field left blank.")
            sys.exit(1)
    else:
        referenceKey = str(input(f"{f.v} Reference Key: "))
        if referenceKey == "":
            print("ERRORx1: ValueError, Required field left blank.")
            sys.exit(1)

    passwordLength = input(f"{f.v} Output Len: ")
    if passwordLength == "":
        passwordLength = 22
    else:
        try:
            passwordLength = int(passwordLength)
        except ValueError:
            print("ERRORx1: ValueError, An integer was not entered.")
            sys.exit(1)

    showPassword = str(input(f"{f.v} Show Output (y / n): "))
    if showPassword == "y" or showPassword == "Y":
        showPassword = True
    elif showPassword == "n" or showPassword == "N":
        showPassword = False
    elif showPassword == "" or showPassword == " ":
        showPassword = False
    else:
        print("ERRORx1: ValueError, Invalid input to y/n question.")
        sys.exit(1)

    print(f.bottom)


def generator(seed, length):
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


def main():
    # Displays a fancy startup message
    startup()

    # Checks arguments and gets user values
    hide = "False"
    try:
        if "--hide-all" in sys.argv:
            hide = "All"
        elif "--hide-pass" in sys.argv:
            hide = "Pass"
        elif "--hide-key" in sys.argv:
            hide = "Key"
        elif "--help" in sys.argv:
            help()
    except IndexError:
        pass
    promptUser(hide)

    # Generates Password
    pw = generator((masterPassword + referenceKey), passwordLength)

    # Either prints or copies the password
    if showPassword:
        print(f.top)
        print(f.v, pw)
        print(f.bottom)
    else:
        pc.copy(pw)

        print(f"{f.tl} Copied to Clipboard! Clearing in 15 seconds.")

        sleep(15)

        pc.copy("// Cleared //")
        print(f"{f.bl} Clipboard Cleared!")

        sys.exit(0)


main()
