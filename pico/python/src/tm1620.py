# dMarkle (c) by Greg Coonrod
#
# dMarkle is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
#
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

from machine import Pin
import time


def delay():
    time.sleep_us(1)


class TM1620:
    CMD_DATA_AUTO = 0x40
    CMD_DATA_READ = 0x42
    CMD_DATA_FIXED = 0x44
    CMD_DISPLAY = 0x80
    CMD_ADDRESS = 0xC0

    FONT_HEX = {
        0: 0b00111111,
        1: 0b00000110,
        2: 0b01011011,
        3: 0b01001111,
        4: 0b01100110,
        5: 0b01101101,
        6: 0b01111101,
        7: 0b00000111,
        8: 0b01111111,
        9: 0b01101111,
        10: 0b01110111,
        11: 0b01111100,
        12: 0b00111001,
        13: 0b01011110,
        14: 0b01111001,
        15: 0b01110001
    }

    FONT_ASCII = {
        ' ': 0b00000000,  # (32)  <space>
        '!': 0b10000110,  # (33)	!
        '"': 0b00100010,  # (34)	"
        '#': 0b01111110,  # (35)	#
        '$': 0b01101101,  # (36)	$
        '%': 0b00000000,  # (37)	%
        '&': 0b00000000,  # (38)	&
        '\'': 0b00000010,  # (39)	'
        '(': 0b00110000,  # (40)	(
        ')': 0b00000110,  # (41)	)
        '*': 0b01100011,  # (42)	*
        '+': 0b00000000,  # (43)	+
        ',': 0b00000100,  # (44)	,
        '-': 0b01000000,  # (45)	-
        '.': 0b10000000,  # (46)	.
        '/': 0b01010010,  # (47)	/
        '0': 0b00111111,  # (48)	0
        '1': 0b00000110,  # (49)	1
        '2': 0b01011011,  # (50)	2
        '3': 0b01001111,  # (51)	3
        '4': 0b01100110,  # (52)	4
        '5': 0b01101101,  # (53)	5
        '6': 0b01111101,  # (54)	6
        '7': 0b00100111,  # (55)	7
        '8': 0b01111111,  # (56)	8
        '9': 0b01101111,  # (57)	9
        ':': 0b00000000,  # (58)	:
        ';': 0b00000000,  # (59)	;
        '<': 0b00000000,  # (60)	<
        '=': 0b01001000,  # (61)	=
        '>': 0b00000000,  # (62)	>
        '?': 0b01010011,  # (63)	?
        '@': 0b01011111,  # (64)	@
        'A': 0b01110111,  # (65)	A
        'B': 0b01111111,  # (66)	B
        'C': 0b00111001,  # (67)	C
        'D': 0b00111111,  # (68)	D
        'E': 0b01111001,  # (69)	E
        'F': 0b01110001,  # (70)	F
        'G': 0b00111101,  # (71)	G
        'H': 0b01110110,  # (72)	H
        'I': 0b00000110,  # (73)	I
        'J': 0b00011110,  # (74)	J
        'K': 0b01101001,  # (75)	K
        'L': 0b00111000,  # (76)	L
        'M': 0b00010101,  # (77)	M
        'N': 0b00110111,  # (78)	N
        'O': 0b00111111,  # (79)	O
        'P': 0b01110011,  # (80)	P
        'Q': 0b01100111,  # (81)	Q
        'R': 0b00110001,  # (82)	R
        'S': 0b01101101,  # (83)	S
        'T': 0b01111000,  # (84)	T
        'U': 0b00111110,  # (85)	U
        'V': 0b00101010,  # (86)	V
        'W': 0b00011101,  # (87)	W
        'X': 0b01110110,  # (88)	X
        'Y': 0b01101110,  # (89)	Y
        'Z': 0b01011011,  # (90)	Z
        '[': 0b00111001,  # (91)	[
        '\\':
        0b01100100,  # (92)	\ (this can't be the last char on a line, even in comment or it'll concat)
        ']': 0b00001111,  # (93)	]
        '^': 0b00000000,  # (94)	^
        '_': 0b00001000,  # (95)	_
        '`': 0b00100000,  # (96)	`
        'a': 0b01011111,  # (97)	a
        'b': 0b01111100,  # (98)	b
        'c': 0b01011000,  # (99)	c
        'd': 0b01011110,  # (100)	d
        'e': 0b01111011,  # (101)	e
        'f': 0b00110001,  # (102)	f
        'g': 0b01101111,  # (103)	g
        'h': 0b01110100,  # (104)	h
        'i': 0b00000100,  # (105)	i
        'j': 0b00001110,  # (106)	j
        'k': 0b01110101,  # (107)	k
        'l': 0b00110000,  # (108)	l
        'm': 0b01010101,  # (109)	m
        'n': 0b01010100,  # (110)	n
        'o': 0b01011100,  # (111)	o
        'p': 0b01110011,  # (112)	p
        'q': 0b01100111,  # (113)	q
        'r': 0b01010000,  # (114)	r
        's': 0b01101101,  # (115)	s
        't': 0b01111000,  # (116)	t
        'u': 0b00011100,  # (117)	u
        'v': 0b00101010,  # (118)	v
        'w': 0b00011101,  # (119)	w
        'x': 0b01110110,  # (120)	x
        'y': 0b01101110,  # (121)	y
        'z': 0b01000111,  # (122)	z
        '{': 0b01000110,  # (123)	{
        '|': 0b00000110,  # (124)	|
        '}': 0b01110000,  # (125)	}
        '~': 0b00000001,  # (126)	~
    }

    def __init__(self, clkPin: int, dinPin: int, stbPin: int):
        self.clkPin = Pin(clkPin, Pin.OUT, value=1)
        self.dinPin = Pin(dinPin, Pin.OUT, value=0)
        self.stbPin = Pin(stbPin, Pin.OUT, value=1)
        self.__max_segments = 10
        self.__max_digits = 6

    def initialize_display(self, num_digits: int, active: bool,
                           intensity: int) -> None:

        self.digits = num_digits
        if num_digits <= 4:
            self.send_command(0x00)
        elif num_digits == 5:
            self.send_command(0x01)
        else:
            self.send_command(0x02)

        self.clear_display()
        self.setup_display(active, intensity)

    def send_command(self, command: int) -> None:
        self.__start()
        self.__send_byte(command)
        self.__end()

    def send_data(self, address: int, data: int) -> None:
        self.send_command(TM1620.CMD_DATA_FIXED)
        self.__start()
        self.__send_byte(TM1620.CMD_ADDRESS | address)
        self.__send_byte(data)
        self.__end()

    def setup_display(self, active: bool, intensity: int) -> None:
        self.send_command(TM1620.CMD_DISPLAY | 8 if active else 0
                          | intensity if intensity < 7 else 7)

    def clear_display(self) -> None:
        self.send_command(TM1620.CMD_DATA_AUTO)
        self.__start()
        self.__send_byte(TM1620.CMD_ADDRESS)
        for x in range(self.__max_segments):
            self.__send_byte(0x00)
            if self.__max_segments > 8:
                self.__send_byte(0x00)
        self.__end()

    def set_segments(self, segments: int, position: int) -> None:
        if position < self.__max_digits:
            self.send_data(position << 1, segments)

    def set_segments_16(self, segments: int, position: int) -> None:
        if position < self.__max_digits:
            self.send_data(position << 1, segments & 0xFF)
            self.send_data((position << 1) | 1, (segments >> 8) & 0x30)

    def __send_char(self, position: int, data: int, dot: bool) -> None:
        self.set_segments(data | (0b10000000 if dot else 0), position)

    def send_ascii_char(self, position: int, char: str, dot: bool):
        if char[0] in TM1620.FONT_ASCII.keys():
            self.__send_char(position, TM1620.FONT_ASCII[char[0]], dot)
        else:
            raise ValueError('Invalid Character: ' + char[0])

    def set_display_digit(self, position: int, digit: int, dot: bool):
        if digit >= 0 and digit < 16:
            self.__send_char(position, TM1620.FONT_HEX[digit], dot)
        else:
            raise ValueError('Invalid Character: ' + str(digit))

    # TODO: I expect this is broken
    def set_display_number(self, number: float, dots: int):
        for x in range(1, self.digits + 1):
            self.set_display_digit(self.digits - x, int(number // 10),
                                   bool(dots & (1 << x)))
            number = number / 10

    def set_display(self, bytes: list[int]):
        for idx, byte in enumerate(bytes):
            self.__send_char(idx, byte, False)

    def set_display_string(self, string: str, start: int):
        for pos in range(self.digits - start):
            if string[pos] != '\0':
                self.send_ascii_char(pos + start, string[pos], False)
            else:
                break

    def clear_display_digit(self, position: int, dot: bool):
        self.__send_char(position, 0, dot)

    def __start(self) -> None:
        self.stbPin.value(0)
        delay()

    def __end(self) -> None:
        self.stbPin.value(1)
        delay()

    def __send_byte(self, byte: int) -> None:
        for _ in range(8):
            self.clkPin.value(0)
            delay()
            self.dinPin.value(1 if byte & 1 else 0)
            delay()
            byte = byte >> 1
            self.clkPin.value(1)
            delay()

        delay()
