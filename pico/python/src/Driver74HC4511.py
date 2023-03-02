# dMarkle (c) by Greg Coonrod
# 
# dMarkle is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
# 
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

from machine import Pin
from time import sleep_us
from typing import List

class Signals:
    d0: int
    d1: int
    d2: int
    d3: int
    lamp_test: int
    blank: int
    latch_enable: int
    def __init__(self, d0: int, d1: int, d2: int, d3: int, lamp_test: int, blank: int, latch_enable: int):
        self.d0 = d0
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
        self.lamp_test = lamp_test
        self.blank = blank
        self.latch_enable = latch_enable
        

class CD74HC4511:
    
    def __init__(self, bcd_input: List[Pin], lamp_test: Pin, blank: Pin, latch_enable: Pin):
        self.bcd_input_pins = bcd_input
        self.lamp_test_pin = lamp_test
        self.blank_pin = blank
        self.latch_enable_pin = latch_enable
        
        self.lamp_test(False)
        self.blank_output(True)
        self.latch_enable(True)
     
    # BL (Blank) is an active low signal   
    def blank_output(self, value=True):
        self.blank_pin.value(not value)
    
    # LT (Lamp Test) is an active low signal    
    def lamp_test(self, value=True):
        self.lamp_test_pin.value(not value)
        
    # LE (Latch Enable) is an active low signal
    def latch_enable(self, value=True):
        self.latch_enable_pin.value(not value)
    
    # Toggle LE high and then low 
    def latch_input(self):
        self.latch_enable(False)
        sleep_us(1)
        self.latch_enable(True)
    
    # Shift out the bits of value LSB first into the input pins    
    def set_bcd(self, value: int):
        if value >= 0 and value < 10:
            for bit in range(3, -1, -1):
                print("Setting D{} to {}".format(bit, (value >> bit) & 1))
                self.bcd_input_pins[bit].value((value >> bit) & 1)