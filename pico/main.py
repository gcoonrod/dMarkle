# dMarkle (c) by Greg Coonrod
# 
# dMarkle is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
# 
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

from machine import Pin, Timer

class Digit:
    
    def __init__(self, pins):
        self.d0 = Pin(pins[0], Pin.OUT)
        self.d1 = Pin(pins[1], Pin.OUT)
        self.d2 = Pin(pins[2], Pin.OUT)
        self.d3 = Pin(pins[3], Pin.OUT)
        self.blank = False
        self.lampTest = False
        
        self.currentValue = 0
        self.setValue(0)
        
    def setValue(self, value=None):
        if value == None:
            self.blank = True
        else:
            self.blank = False
            self.d0.value(value & 0b0001)
            self.d1.value(value & 0b0010)
            self.d2.value(value & 0b0100)
            self.d3.value(value & 0b1000)
            

if __name__ == "__main__":
    digitOne = Digit([1, 2, 4, 5])
    digitTwo = Digit([9, 10, 11, 12])
    digitThree = Digit([14, 15, 16, 17])
    
    digitOne.setValue(1)
    digitTwo.setValue(2)
    digitThree.setValue(3)
        
            
        
