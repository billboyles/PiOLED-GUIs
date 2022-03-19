#import modules
import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


#create i2c interface
i2c = busio.I2C(SCL, SDA)

#create OLED class
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

#clear display
disp.fill(0)
disp.show()

#create blank image
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

#get drawing image
draw = ImageDraw.Draw(image)

#clear image
draw.rectangle((0, 0, width, height), outline=0, fill=0)

#origin and padding
padding = -2
top = padding
bottom = height - padding
x = 0


#load font
font = ImageFont.load_default()

#display loop
while True:

    #clear image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #shell scripts for monitoring
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

    #write text
    draw.text((x, top + 0), NAME, font=font, fill=255)
    
    #draw line
    draw.line(xy=[(x, top + 12), (x + 60, top + 12)], fill=255, width=1, joint=None)
    
    #write more text
    draw.text((x, top + 14),      f" CPU: {CPU}%", font=font, fill=255)
    draw.text((x, top + 24),      f" MEM: {MEM}", font=font, fill=255)
    draw.text((x + 64, top + 14), f"DISK: {DISK}", font=font, fill=255)
    draw.text((x + 64, top + 24), f"TEMP: {TEMP}C", font=font, fill=255)

    #display
    disp.image(image)
    disp.show()
    time.sleep(0.1)
