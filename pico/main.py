# dMarkle (c) by Greg Coonrod
#
# dMarkle is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
#
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

from machine import Pin
import time
import random

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

DICE = {
    'd4': dict(value=4, bits=3),
    'd6': dict(value=6, bits=3),
    'd8': dict(value=8, bits=4),
    'd10': dict(value=10, bits=4),
    'd12': dict(value=12, bits=4),
    'd20': dict(value=20, bits=5),
    'd100': dict(value=100, bits=7)
}

DICE_LIST = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100']


class Direction:
    LEFT = 0
    RIGHT = 1


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


class RotaryEncoder:

    def __init__(self, clk_pin, dt_pin, btn_pin):
        self.clk = Pin(clk_pin, Pin.IN)
        self.dt = Pin(dt_pin, Pin.IN)

        # Active Low Button
        self.btn = Pin(btn_pin, Pin.IN)

        self.press_handler = None
        self.turn_handler = None

        self.clk.irq(self.__clk_irq_handler, Pin.IRQ_FALLING)
        self.btn.irq(self.__btn_irq_handler, Pin.IRQ_FALLING)

    def register_press_handler(self, handler_func):
        self.press_handler = handler_func

    def register_turn_handler(self, handler_func):
        self.turn_handler = handler_func

    def __clk_irq_handler(self, pin):
        dt_value = self.dt.value()
        #print('IRQ: dt={}'.format(dt_value))
        if dt_value == 0:
            if self.turn_handler != None:
                self.turn_handler(Direction.LEFT)
        else:
            if self.turn_handler != None:
                self.turn_handler(Direction.RIGHT)

    def __btn_irq_handler(self, pin):
        if self.press_handler != None:
            self.press_handler()


class Program:

    def __init__(self):
        self.display = Display()
        self.encoder = RotaryEncoder(clk_pin=20, dt_pin=19, btn_pin=18)
        self.encoder.register_press_handler(self.handle_press)
        self.encoder.register_turn_handler(self.handle_turn)
        self.current_die_idx = 0
        self.current_die = DICE[DICE_LIST[self.current_die_idx]]
        self.display.display_number(self.current_die['value'])

    def roll_dice(self):
        max_value = self.current_die['value']
        bits = self.current_die['bits']

        result = random.getrandbits(bits)
        while result == 0 or result > max_value:
            result = random.getrandbits(bits)

        return result

    def handle_turn(self, direction: Direction):
        if direction == Direction.LEFT:
            if self.current_die_idx == 0:
                self.current_die_idx = 6
            else:
                self.current_die_idx -= 1
        elif direction == Direction.RIGHT:
            if self.current_die_idx == 6:
                self.current_die_idx = 0
            else:
                self.current_die_idx += 1
        else:
            print('WTF')

        self.current_die = DICE[DICE_LIST[self.current_die_idx]]
        num_to_display = self.current_die['value']
        self.display.display_number(num_to_display)
        print('Current Die: {}'.format(self.current_die['value']))

    def handle_press(self):
        roll = self.roll_dice()
        print('{} rolled a {}'.format(DICE_LIST[self.current_die_idx], roll))
        self.display.display_number(roll)


# Main
random.seed(None)
program = Program()
