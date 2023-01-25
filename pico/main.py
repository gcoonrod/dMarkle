# dMarkle (c) by Greg Coonrod
#
# dMarkle is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
#
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

from machine import Pin
import time

NUMBERS = {
    0: dict(d3=0, d2=0, d1=0, d0=0, LE=0, BL=1, LT=1),
    1: dict(d3=0, d2=0, d1=0, d0=1, LE=0, BL=1, LT=1),
    2: dict(d3=0, d2=0, d1=1, d0=0, LE=0, BL=1, LT=1),
    3: dict(d3=0, d2=0, d1=1, d0=1, LE=0, BL=1, LT=1),
    4: dict(d3=0, d2=1, d1=0, d0=0, LE=0, BL=1, LT=1),
    5: dict(d3=0, d2=1, d1=0, d0=1, LE=0, BL=1, LT=1),
    6: dict(d3=0, d2=1, d1=1, d0=0, LE=0, BL=1, LT=1),
    7: dict(d3=0, d2=1, d1=1, d0=1, LE=0, BL=1, LT=1),
    8: dict(d3=1, d2=0, d1=0, d0=0, LE=0, BL=1, LT=1),
    9: dict(d3=1, d2=0, d1=0, d0=1, LE=0, BL=1, LT=1),
}


class Digit:

    def __init__(self, pins):
        self.d3 = Pin(pins['d3'], Pin.OUT, value=0)
        self.d2 = Pin(pins['d2'], Pin.OUT, value=0)
        self.d1 = Pin(pins['d1'], Pin.OUT, value=0)
        self.d0 = Pin(pins['d0'], Pin.OUT, value=0)
        self.blank = Pin(pins['BL'], Pin.OUT, value=0)
        self.latch = Pin(pins['LE'], Pin.OUT, value=1)

    def set_value(self, value, blank=False):
        if blank:
            self.blank.off()
        else:
            self.blank.on()
            lookup = NUMBERS[value]
            self.d0.value(lookup['d0'])
            self.d1.value(lookup['d1'])
            self.d2.value(lookup['d2'])
            self.d3.value(lookup['d3'])
            time.sleep_us(50)
            self.latch.off()
            time.sleep_us(50)
            self.latch.on()
            time.sleep_us(50)

    def set_blank(self, value=True):
        if value:
            self.blank.off()
        else:
            self.blank.on()


class Display:

    def __init__(self):
        self.ones_digit = Digit(dict(d3=3, d2=2, d1=1, d0=0, LE=9, BL=6))
        self.tens_digit = Digit(dict(d3=3, d2=2, d1=1, d0=0, LE=8, BL=5))
        self.hundreds_digit = Digit(dict(d3=3, d2=2, d1=1, d0=0, LE=7, BL=4))

    def display_number(self, value):
        if value > 999 or value < 0:
            self.show_error()
        else:
            digits = list(str(value))
            digits.reverse()
            num_digits = len(digits)
            if num_digits > 0:
                self.ones_digit.set_value(int(digits[0]))
            else:
                self.ones_digit.set_blank()

            if num_digits > 1:
                self.tens_digit.set_value(int(digits[1]))
            else:
                self.tens_digit.set_blank()

            if num_digits > 2:
                self.hundreds_digit.set_value(int(digits[2]))
            else:
                self.hundreds_digit.set_blank()

    def show_error(self):
        print('Oops')


# Main

display = Display()

num_to_show = 0
while True:
    display.display_number(num_to_show)
    time.sleep_ms(10)
    if num_to_show < 999:
        num_to_show += 1
    else:
        num_to_show = 0
