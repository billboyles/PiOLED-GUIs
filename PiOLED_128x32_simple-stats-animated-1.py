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
image1 = Image.new("1", (width, height))
image2 = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image2)

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
font = ImageFont.truetype(font='/home/pi/GUIs/Open 24 Display St.ttf', size=30)

while True:
        
    #clear image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #get info
    cmd = "hostname"
    NAME = subprocess.check_output(cmd, shell=True).decode("utf-8")

    #write text
    draw.text((x, top + 0), NAME, font=font, fill=255)
    
    #rotate image by increments
    for n in range(180, 365, 5):
        rotated_image = image2.rotate(n, expand=False)
        image1.paste(rotated_image)

        # Display image.
        disp.image(image1)
        disp.show()
        time.sleep(0.01)
    
    time.sleep(1)

    cmd = "mpstat | awk 'NR==4{printf \"%s\", $13}'"
    CPU = str(100 - round(float(subprocess.check_output(cmd, shell=True).decode("utf-8")))).strip()
    cmd = "free -m | awk 'NR==2{printf \"%2.0f%%\", $3*100/$2 }'"
    MEM = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
    cmd = "df -H | awk 'NR==2{printf \"%s\", $5}'"
    DISK = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
    cmd = "vcgencmd measure_temp | awk -F'[\=\.]' '{printf \"%2s\", $2}'"
    TEMP = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

    for n in range(0, -1500, -15):

        #clear image
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        #write text
        draw.text((n, top), NAME, font=font, fill=255)
        draw.text((n + 300, top), f"CPU: {CPU}%", font=font, fill=255)
        draw.text((n + 600, top), f"MEM: {MEM}", font=font, fill=255)
        draw.text((n + 900, top), f"DISK: {DISK}", font=font, fill=255)
        draw.text((n + 1200, top), f"TEMP: {TEMP}° C", font=font, fill=255)

        if n % 300== 0:
            time.sleep(1)

        # Display image.
        disp.image(image2)
        disp.show()
        time.sleep(0.01)