  
# About:
  This is an open-source bot, the code is open for anyone to see, fork and
update.
  As the developer, I created this bot just for my personal use, I decided to
publish to help other people and maybe get a few bucks in donation.  As the
time went by, more and more people started opening issues, asking for help and
suggesting changes.
  I try to answer everyone, but lately it has been hard to keep  up. As the
only donation I received so far amounts to only 1 BCOIN and the bot
currently works perfectly for me. I am not feeling to motivated to spend the
time it needs to maintain the bot. I would like to keep this bot free and open
source, so as an incentive for me to spend the time and energy maintaining the
bot, I have created some donation milestones so people can collectively fund
the bot.

Currently, I will be manually updating the donation counter daily, maybe in
the future I can set it up, so it increments automatically.

1 Spend some time in my days reviewing issues, and organizing repository.
Review and merge pull requests.

2 A step-by-step guide in how to troubleshoot and fix the most common bugs,
maybe with some flow charts.

3 A step-by-step guide in how to set up the bot in a VPS using google cloud
free trial (3 months) 

4 Implement and maintain the feature for sending selected heroes home.(a lot
of iteration will be needed solving minor bugs, as I do not own any house).

5 Insert an random value in every movement and delay in the bot to further
prevent detection.

6 Work in the bug fixes relating to the login sequence.

7 Work with the people who are having this issue to solve the errors
happening when running the bot in a windows double monitor setup.



``` 
             1(15%)        2,3(30%)     4(40%)               5(60%)          6(75%)     7(85%)
[x==============|===============|==========|====================|===============|==========|===============] (500$)
```
### Smart Chain Wallet:
#### 0xbd06182D8360FB7AC1B05e871e56c76372510dDf

### Paypal:
[Donate:](https://www.paypal.com/donate?hosted_button_id=JVYSC6ZYCNQQQ)
https://www.paypal.com/donate?hosted_button_id=JVYSC6ZYCNQQQ

## Disclaymer:
  
  The bombcrypto developers have not manifested themselves yet regarding the
  use of bots. Do your own research and use the bot at your own risk. I am not
  responsible for any future penalties.


# Installation:
### Download and install Phython from the [site](https://www.python.org/downloads/) or from the [windows store](https://www.microsoft.com/p/python-37/9nj46sx7x90p?activetab=pivot:overviewtab). 

If you download from the site it is important to tick the option "add python
to path":
![Check Add python to PATH](https://github.com/mpcabete/bombcrypto-bot/raw/ee1b3890e67bc30e372359db9ae3feebc9c928d8/readme-images/path.png)

### Download the code as a zip file and extract it.

### Copy the path of the bot directory:

![caminho](https://github.com/mpcabete/bombcrypto-bot/raw/main/readme-images/address.png)

### Open the terminal.

Press the windows key + R and type "cmd":

![launch terminal](https://github.com/mpcabete/bombcrypto-bot/raw/main/readme-images/cmd.png)

### cd into the bot directory:
Type the command:

```
cd <path you copied>
```

![cd](https://github.com/mpcabete/bombcrypto-bot/raw/main/readme-images/cd.png)

### Install the dependencies:

```
pip install -r requirements.txt
```

  
![pip](https://github.com/mpcabete/bombcrypto-bot/raw/main/readme-images/pip.png)

### It is finished! Now to run the bot you just need to type:

```
python index.py
```

![run](https://github.com/mpcabete/bombcrypto-bot/raw/main/readme-images/run.png)


# How to use?

Abra o terminal, se ainda não tiver navegado para a pasta do bot dê novamente o comando
Open the terminal, cd into the folder if you haven't yet:

```
"cd" + path
```

To run it use the command

```
python index.py
```

As soon as you start the bot it will send the heroes to work. For it to work the game window needs to be visible.
It will constantly check if it needs to login or press the "new map" button. 
From 15 to 15 min it will send all heroes to work again


# Send home feature:

## How to use it:
Save a screenshot of the heroes you want to be sent home in the directory: /targets/heroes-to-send-home


## How it should behave:
It will automatically  load the screenshots of the heroes when starting up.
After it clicks in the heroes with the green bar to send them to work, it will look if there is any of the heroes that are saved in the directory in the screen.
If tit finds one of the heroes, the bot checks if the home button is dark and the work button is not dark.
If both these conditions are true, it clicks the home button.

## Troubleshooting:
#### I have not been able to fine adjust it, so here is some problems that may occur, and how to solve them:

- The bot should distinguish between the dark, the clear and the gray home buttons.
  - If the bot says that a hero is working or home, but he is not, that is because the bot is not detecting the dark home button, make the option "home: home_button_trashhold" smaller. You can also replace the image send-home.png in the targets folder.

  - If the bot is trapped in an loop clicking in an clear home button, he thinks that the clear button is the dark button, make the option home: home_button_trashhold bigger.

- The bot should detect the heroes you saved to the directory.
  - If the bot clicks the wrong heroes, it thinks that another hero is the one you saved the screenshot. Make the option home: hero_trashhold bigger
  - If it does not detect your heroes, make it smaller. You can also try replacing the screenshot with another part of the hero.

  ----------------

## Pay me a coffe :)

### Wallet:
#### 0xbd06182D8360FB7AC1B05e871e56c76372510dDf
### Paypal:
[Donate](https://www.paypal.com/donate?hosted_button_id=JVYSC6ZYCNQQQ)
