#import modules
import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import slanted_lines_animated_1_config
line_number = slanted_lines_animated_1_config.LINE_NUMBER
line_width = slanted_lines_animated_1_config.LINE_WIDTH
line_space = slanted_lines_animated_1_config.LINE_SPACE
slantiness = slanted_lines_animated_1_config.SLANTINESS
speed = slanted_lines_animated_1_config.SPEED
font_file = slanted_lines_animated_1_config.FONT_FILE

#create i2c interface
i2c = busio.I2C(SCL, SDA)

#create OLED class
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

#clear display
disp.fill(0)
disp.show()

#create blank image for drawing
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

#get drawing image
draw = ImageDraw.Draw(image)

#clear screen
draw.rectangle((0, 0, width, height), outline=0, fill=0)

#origin and padding
padding = -2
top = padding
bottom = height - padding

#load font - change font file name to use a different font
#font file must be in same dir as script

font = ImageFont.truetype(font=font_file, size=44)

#get hostname info
cmd = "hostname"
NAME = subprocess.check_output(cmd, shell=True).decode("utf-8")
text_length = font.getsize(NAME)[0]
text_height = font.getsize(NAME)[1]

#calculate needed overflow
margin_fudge =  0 - (slantiness * 2) - ((line_width * line_number) + (line_space * (line_number - 1))) - text_length
text_fudge = (height - text_height) / 2

#display loop
while True:

    for n in range(132, margin_fudge, -4):

        #clear image
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        x = 0

        for i in range(0, line_number):
            
            for j in range(0, line_width):
                draw.line([(n + x, top), ((n + x - slantiness), (height + 2))], fill=255, width=1, joint=None)
                #print(f"line {j}: {n + x}")
                x += 1
            
            if i != line_number:
                for k in range(0, line_space):
                    draw.line([(n + x, top), ((n + x - slantiness), (height + 2))], fill=0, width=1, joint=None)
                    #print(f"space {k}: {n + x}")
                    x += 1
            
            #draw.polygon([((n + x), top), ((n + x - slantiness), (top + 32)), ((n + x), (top + 32))], fill=255, outline=None)

        #write text
        draw.text(((n + x - 15), top + text_fudge), NAME, font=font, fill=255)

        #display image
        disp.image(image)
        disp.show()
        time.sleep(speed)