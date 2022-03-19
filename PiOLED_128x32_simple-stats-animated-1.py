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

#create blank images for drawing and rotating
width = disp.width
height = disp.height
image1 = Image.new("1", (width, height))
image2 = Image.new("1", (width, height))

#get drawing image
draw = ImageDraw.Draw(image2)

#clear screen
draw.rectangle((0, 0, width, height), outline=0, fill=0)

#origin and padding
padding = -2
top = padding
bottom = height - padding


#load font - change font file name to use a different font
#font file must be in same dir as script
font = ImageFont.truetype(font='/home/pi/Open 24 Display St.ttf', size=30)

#get hostname info
cmd = "hostname"
NAME = subprocess.check_output(cmd, shell=True).decode("utf-8")

#display loop
while True:
        
    #clear image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #write text
    draw.text((x, top), NAME, font=font, fill=255)
    
    #rotate image by increments
    for n in range(180, 365, 5):
        rotated_image = image2.rotate(n, expand=False)
        image1.paste(rotated_image)

        # Display image.
        disp.image(image1)
        disp.show()
        time.sleep(0.01)
    
    #wait 1 sec
    time.sleep(1)

    #shell scripts for monitoring
    cmd = "mpstat | awk 'NR==4{printf \"%s\", $13}'"
    CPU = str(100 - round(float(subprocess.check_output(cmd, shell=True).decode("utf-8")))).strip()
    cmd = "free -m | awk 'NR==2{printf \"%2.0f%%\", $3*100/$2 }'"
    MEM = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
    cmd = "df -H | awk 'NR==2{printf \"%s\", $5}'"
    DISK = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
    cmd = "vcgencmd measure_temp | awk -F'[\=\.]' '{printf \"%2s\", $2}'"
    TEMP = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

    #scroll text across screen
    for n in range(0, -1500, -15):

        #clear image
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        #write text
        draw.text((n, top), NAME, font=font, fill=255)
        draw.text((n + 300, top), f"CPU: {CPU}%", font=font, fill=255)
        draw.text((n + 600, top), f"MEM: {MEM}", font=font, fill=255)
        draw.text((n + 900, top), f"DISK: {DISK}", font=font, fill=255)
        draw.text((n + 1200, top), f"TEMP: {TEMP}° C", font=font, fill=255)

        #wait 1 sec after each item
        if n % 300== 0:
            time.sleep(1)

        #display image
        disp.image(image2)
        disp.show()
        time.sleep(0.01)