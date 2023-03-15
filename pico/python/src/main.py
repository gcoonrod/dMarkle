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

from Driver74HC4511 import CD74HC4511, Signals

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

    def __init__(self, signals: Signals):
        self.signal_pins = dict(
            d0 = Pin(signals.d0, Pin.OUT),
            d1 = Pin(signals.d1, Pin.OUT),
            d2 = Pin(signals.d2, Pin.OUT),
            d3 = Pin(signals.d3, Pin.OUT),
            lamp_test = Pin(signals.lamp_test, Pin.OUT),
            blank = Pin(signals.blank, Pin.OUT),
            latch_enable = Pin(signals.latch_enable, Pin.OUT)
        )
        self.driver = CD74HC4511(
            bcd_input = [
                self.signal_pins['d3'],
                self.signal_pins['d2'],
                self.signal_pins['d1'],
                self.signal_pins['d0']
            ],
            lamp_test = self.signal_pins['lamp_test'],
            blank = self.signal_pins['blank'],
            latch_enable = self.signal_pins['latch_enable']
        )
        

    def set_value(self, value: int, blank=False):
        self.driver.set_bcd(value)

    def set_blank(self, value=True):
        self.driver.blank_output(value)


class Display:

    def __init__(self):
        self.current_value = 0
        self.ones_digit = Digit(Signals(0, 1, 2, 3, -1, 6, 9))
        self.tens_digit = Digit(Signals(0, 1, 2, 3, -1, 8, 5))
        self.hundreds_digit = Digit(Signals(0, 1, 2, 3, -1, 7, 4))

    def display_number(self, value):
        if value > 999 or value < 0:
            self.show_error()
        else:
            self.current_value = value
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
                
    def blink_display(self):
        for _ in range(2):
            self.ones_digit.set_blank()
            self.tens_digit.set_blank()
            self.hundreds_digit.set_blank()
            time.sleep_ms(10)
            self.ones_digit.set_blank(False)
            self.tens_digit.set_blank(False)
            self.hundreds_digit.set_blank(False)
            time.sleep_ms(10)

    def show_error(self):
        print('Oops')
        
    def animate_roll(self, sleep_time = 100, iterations = 5):
        # Blank everything first
        self.ones_digit.set_blank()
        self.tens_digit.set_blank()
        self.hundreds_digit.set_blank()
        
        for _ in range(iterations):
            self.hundreds_digit.set_value(0)
            time.sleep_ms(sleep_time)
            self.hundreds_digit.set_blank()
            self.tens_digit.set_value(0)
            time.sleep_ms(sleep_time)
            self.tens_digit.set_blank()
            self.ones_digit.set_value(0)
            time.sleep_ms(sleep_time)
            self.ones_digit.set_blank()    
            


class RotaryEncoder:
    THRESHOLD = 2

    def __init__(self, clk_pin, dt_pin, btn_pin):
        self.clk = Pin(clk_pin, Pin.IN)
        self.dt = Pin(dt_pin, Pin.IN)
        
        self.dt_prev_val = 0
        self.clicks = 0

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
        if self.turn_handler is None:
            return
        
        dt_value = self.dt.value()
        turn_direction = None
        
        if dt_value == self.dt_prev_val:
            if self.clicks > RotaryEncoder.THRESHOLD:
                self.clicks = 0
                turn_direction = Direction.LEFT if dt_value == 0 else Direction.RIGHT
            else:
                self.clicks += 1
        else:
            self.clicks = 0
        
        if turn_direction is not None:
            self.turn_handler(turn_direction) 
        #print('IRQ: dt={}'.format(dt_value))

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
        self.display.blink_display()
        print('Current Die: {}'.format(self.current_die['value']))

    def handle_press(self):
        roll = self.roll_dice()
        print('{} rolled a {}'.format(DICE_LIST[self.current_die_idx], roll))
        self.display.animate_roll()
        self.display.display_number(roll)


# Main
random.seed(None)
program = Program()
