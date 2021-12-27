FROM dorowu/ubuntu-desktop-lxde-vnc

RUN sudo apt remove firefox -y && \
    sudo apt remove google-chrome-stable -y && \
    sudo apt update && \
    sudo apt upgrade -y && \
    sudo apt install python3-pyqt5 -y && \
    sudo apt install git -y && \
    sudo apt install pyqt5-dev-tools -y && \
    sudo apt install qttools5-dev-tools -y && \
    sudo apt install xclip -y && \
    sudo apt install python3-pip -y && \
    sudo apt  install python3-tk python3-dev -y && \
    sudo pip install pyautogui ; pip install python-xlib && \
    sudo apt install apt-transport-https curl -y && \
    sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=amd64] https://brave-browser-apt-release.s3.brave.com/ stable main"|sudo tee /etc/apt/sources.list.d/brave-browser-release.list && \
    sudo apt update && \
    sudo apt install brave-browser -y

#install DEPs
RUN git clone https://github.com/mpcabete/bombcrypto-bot.git /home/ubuntu/Desktop/bombcrypto-bot && pip install -r /home/ubuntu/Desktop/bombcrypto-bot/requirements.txt
