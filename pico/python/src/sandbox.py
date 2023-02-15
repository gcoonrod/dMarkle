# dMarkle (c) by Greg Coonrod
# 
# dMarkle is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
# 
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

from tm1620 import TM1620
from time import sleep_ms

display = TM1620(3, 4, 5)
display.initialize_display(4, True, 4)

while True:
    display.set_display_string('HALO', 0)
    sleep_ms(300)
    display.set_display_string('Mark', 0)
    sleep_ms(300)
    for x in range(100):
        display.set_display_number(x, 0)
        sleep_ms(100)
    
