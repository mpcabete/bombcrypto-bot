# bombcrypto-bot

## Added extra functions

- Use browser with different zoom (scale)
- Support for multiple accounts on the same monitor (use IFRAME URL to access)
- Debug by game functions
- Support for retina displays

# Installation:

1- Download and install Python in version greater than 3 from [official website](https://www.python.org/downloads/) or through [windows store](https://www.microsoft.com/p/python-37/9nj46sx7x90p?activetab=pivot:overviewtab).

2 - After installing python:

- for `windows` _run as administrator_ the `install.bat` file in the bot's main folder.
- for `linux` execute `run.sh` file in the bot's main folder.

# Settings:

You can configure some options by changing the `config.yaml` file in the bot's main folder.

## `scale_image`

- You now have support to put how many % zoom you are using in your browser.

  > Also pay attention to the ZOOM of the _Metamask_ notification window, it must be the same used in the browser.

  - ### `enable`

    When `True`, activates the functionality to use a different scale. Otherwise, leave the value as `False`

    > Value must be: `True` or `False`

  - ### `percent`
    The zoom percentage of your browser and the metamask notification window.
    > Value must be from: `50` to `100`. The lower the value, the more imprecise the bot's detections will be.

## `is_retina_screen`

- If your computer is a mac device with retina display, you will need to enable this option for the bot to click accurately. If your bot moves the mouse to random places, maybe this option will help you.
  > Value must be: `True` to enable, or `False` to disable

## `mouse_move_speed`

- You can set the speed with which the mouse moves on the screen before clicking.
  > Value must be from: `0.1` to `1`

## `multiples_accounts_same_monitor`

- This option enables the use of multiple accounts on the same monitor, the actions being performed synchronously, that is, one window at a time. To use this functionality we suggest using a URL from the game's IFRAME.

  - ### `enable`

    > Value must be: `True` to enable or `False` to disable

  - ### `window_contains_title`
    This option offers the possibility to change the text that will be used to detect as windows. This text must be in the title of the never window.
