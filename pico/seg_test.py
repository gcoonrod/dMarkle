# dMarkle (c) by Greg Coonrod
# 
# dMarkle is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
# 
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

from machine import Pin, Timer

d0 = Pin(1, Pin.OUT)
d1 = Pin(2, Pin.OUT)
d2 = Pin(4, Pin.OUT)
d3 = Pin(5, Pin.OUT)

timer = Timer()

d0.value(0)
d1.value(0)
d2.value(0)
d3.value(0)

displayNumber = 0

def countUp(timer):
    global displayNumber
    d0.value(displayNumber & 0b0001)
    d1.value(displayNumber & 0b0010)
    d2.value(displayNumber & 0b0100)
    d3.value(displayNumber & 0b1000)
    
    if displayNumber < 9:
        displayNumber = displayNumber + 1
    else:
        displayNumber = 0
        
timer.init(freq=2.5, mode=Timer.PERIODIC, callback=countUp)
