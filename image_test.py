from luma.core.interface.serial import i2c
from luma.oled.device import sh1106, sh1107
from PIL import Image

second = sh1107(i2c(port=5, address=0x3C), rotate=1, width=128, height=128)
first = sh1106(i2c(port=4, address=0x3C))
logo = Image.open("smile.png").convert("1")
white_image = Image.new("1", (second.width, second.height), 1)

if __name__ == "__main__":
    second.display(white_image)
    first.display(logo)

    while True:
        pass
