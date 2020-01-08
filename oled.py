#!/usr/bin/python3
import time
import misc
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

font = {
    '10': ImageFont.truetype('fonts/DejaVuSansMono-Bold.ttf', 10),
    '11': ImageFont.truetype('fonts/DejaVuSansMono-Bold.ttf', 11),
    '12': ImageFont.truetype('fonts/DejaVuSansMono-Bold.ttf', 12),
    '14': ImageFont.truetype('fonts/DejaVuSansMono-Bold.ttf', 14),
}

misc.set_mode(23, 0)
time.sleep(0.2)
misc.set_mode(23, 1)

disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
width = disp.width
height = disp.height

disp.begin()
disp.clear()
disp.display()

image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)


def welcome():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0, 0), 'Rock Pi SATA HAT', font=font['14'], fill=255)
    draw.text((20, 16), 'loading...', font=font['12'], fill=255)
    disp.image(image)
    disp.display()


def goodbye():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((20, 8), 'Good Bye ~', font=font['14'], fill=255)
    disp.image(image)
    disp.display()
    time.sleep(3)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    disp.image(image)
    disp.display()


def put_disk_info():
    k, v = misc.get_disk_info()
    text1 = 'Disk: {} {}'.format(k[0], v[0])

    if len(k) == 5:
        text2 = '{} {}  {} {}'.format(k[1], v[1], k[2], v[2])
        text3 = '{} {}  {} {}'.format(k[3], v[3], k[4], v[4])
        page = [
            {'xy': (0, -2), 'text': text1, 'fill': 255, 'font': font['11']},
            {'xy': (0, 10), 'text': text2, 'fill': 255, 'font': font['11']},
            {'xy': (0, 21), 'text': text3, 'fill': 255, 'font': font['11']},
        ]
    elif len(k) == 3:
        text2 = '{} {}  {} {}'.format(k[1], v[1], k[2], v[2])
        page = [
            {'xy': (0, 2), 'text': text1, 'fill': 255, 'font': font['12']},
            {'xy': (0, 18), 'text': text2, 'fill': 255, 'font': font['12']},
        ]
    else:
        page = [{'xy': (0, 2), 'text': text1, 'fill': 255, 'font': font['14']}]

    return page


def gen_pages():
    pages = {
        0: [
            {'xy': (0, -2), 'text': misc.get_info('up'), 'fill': 255, 'font': font['11']},
            {'xy': (0, 10), 'text': misc.get_info('temp'), 'fill': 255, 'font': font['11']},
            {'xy': (0, 21), 'text': misc.get_info('ip'), 'fill': 255, 'font': font['11']},
        ],
        1: [
            {'xy': (0, 2), 'text': misc.get_info('cpu'), 'fill': 255, 'font': font['12']},
            {'xy': (0, 18), 'text': misc.get_info('men'), 'fill': 255, 'font': font['12']},
        ],
        2: put_disk_info()
    }

    return pages


def slider(lock):
    with lock:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        for item in misc.slider_next(gen_pages()):
            draw.text(**item)
        disp.image(image)
        disp.display()


def auto_slider(lock):
    while misc.conf['slider']['auto']:
        slider(lock)
        misc.slider_sleep()
    else:
        slider(lock)