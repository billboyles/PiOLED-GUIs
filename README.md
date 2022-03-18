# PiOLED-GUIs
Simple static and animated GUIs for 128x32 monochrome PiOLEDs

## Introduction

These GUIs were written for the [Adafruit 128x32 PiOLED](https://www.adafruit.com/product/3527) for use with Raspberry Pi. It's possible and even likely they work for other branded OLED devices of similar size and resolution, and other SOCs like Arduino as long as they are running CircuitPython. However, at this time, they're not really built with those other use cases in mind and may take some tweaking. 

## Prereqs

The easiest way to install these is to follow the Adafruit installation guide [here](https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/). Once this is completed, you are ready to run these GUIs. The script installs the necessary libraries (unless otherwise noted in the README) and configures the screen.

## Installation

Simply the copy the desired GUI file (and any font files, configuration files, or image files as necessary- you can find a list below) into the home, or ~, directory of your Raspberry Pi. The GUI can then be run with `~ $ python <filename>.py`. The GUI will run unitl the script is stopped with `Ctrl-C`.

## Running Automatically

To have the script run automatically, there are a few different ways. The two ways I've used have been through `rc.local` and `crontab`.

### rc.local method

1. Open the the `rc.local` file with `~ $ sudo nano /etc/rc.local`. 
2. In the bottom of the file, above the line `exit 0`, add the following line: `sudo python3 /home/pi/<filename>.py &`, replacing `<filename>` with the name of the desired GUI file.
3. Save and exit with `Ctrl-x` then `y`.
4. **(optional)** To allow for logging, append the above line with the following: `> OLED_log 2>&1`. This will create a log file called 'OLED_log'.

_Note: These instructions are also provided in more detail, with screenshots, in the Adafruit document linked above. In my experience, this method is sometimes hard to make work. To avoid that, I use the `crontab` method._

### crontab method

1. Open `crontab` with the command `~ $ crontab -e`. 
2. A the bottom of the file, below the commented lines, add the following: `@reboot python <filename>.py`, replacing `<filename>` with the name of the desired GUI file.
3. Save and exit with 'Ctrl-x' and `y`. 
4. **(optional)** To allow for logging, append the above line with the following: `> OLED_log 2>&1`. This will create a log file called 'OLED_log'.

## Additional Requirements

#### PiOLED_128x32_simple_stats-1.py

+ This file requires the `mpstats` command. To install, use `sudo apt-get install sysstat`.

#### PiOLED_128x32_simple_stats-animated-1.py

+ This file requires the `mpstats` command. To install, use `sudo apt-get install sysstat`.

+ This file uses the **'Open 24 Display St'** font from [DaFont](https://dafont.com). On the site, this font is marked as free for personal and non-commercial use and has hence been included in this project. However, check with the font creator for questions about whether the license covers your use case. The font may need to be installed in the system. Doing so is beyond the sdcope of this guide, but instructions can be found [here](https://www.unixtutorial.org/how-to-install-ttf-fonts-in-linux/). To use a different font, replace the filename after `font=` in line 53 of the code: `font = ImageFont.truetype(font='/home/pi/GUIs/Open 24 Display St.ttf', size=30)`.

