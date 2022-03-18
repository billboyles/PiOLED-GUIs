# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname"
    NAME = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "mpstat | awk 'NR==4{printf \"%s\", $13}'"
    CPU = str(100 - round(float(subprocess.check_output(cmd, shell=True).decode("utf-8")))).strip()
    cmd = "free -m | awk 'NR==2{printf \"%2.0f%%\", $3*100/$2 }'"
    MEM = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
    cmd = "df -H | awk 'NR==2{printf \"%s\", $5}'"
    DISK = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
    cmd = "vcgencmd measure_temp | awk -F'[\=\.]' '{printf \"%2s\", $2}'"
    TEMP = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

    # Write four lines of text.

    draw.text((x, top + 0), NAME, font=font, fill=255)
    draw.line(xy=[(x, top + 12), (x + 60, top + 12)], fill=255, width=1)
    draw.text((x, top + 14),      f" CPU: {CPU}%", font=font, fill=255)
    draw.text((x, top + 24),      f" MEM: {MEM}", font=font, fill=255)
    draw.text((x + 64, top + 14), f"DISK: {DISK}", font=font, fill=255)
    draw.text((x + 64, top + 24), f"TEMP: {TEMP}C", font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(0.1)
