FROM dorowu/ubuntu-desktop-lxde-vnc

RUN apt-get update && sudo apt-get install python3-pyqt5 -y && sudo apt-get install git -y && sudo apt-get install pyqt5-dev-tools -y && sudo apt-get install qttools5-dev-tools -y && apt-get install xclip -y && apt-get install python3-pip -y && apt-get install python3-tk python3-dev -y && pip install pyautogui ; pip install python-xlib

#install DEPs
RUN git clone https://github.com/mpcabete/bombcrypto-bot.git /root/Desktop/bombcrypto-bot && pip install -r /root/Desktop/bombcrypto-bot/requirements.txt
