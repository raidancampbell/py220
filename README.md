# py220
A Python VT220 Interface

--------
VT220 Configuration Assumptions:
- baud_rate: 9600
- byte_size: 8 bits
- stop_bits: 1
- parity: none
- newline sent from terminal contains '\n' char
- default configuration is light text on dark background

--------
Usage:
- write() to write a given string, newline not appended.
- read_char(block=False, on_char=None) to read a single character from the buffer. Character is returned. Optional callback to call when character is read
- read_line(block=False, on_char=None, on_line=None) to read a single line (ending in '\n'). Line is built character by character, and returned whole.  Optional callback when character or line is read
- read_forever(on_char=None, on_line=None) for a looped reading of the terminal, passing callbacks for when a character or a line is read.
- clear_and_home() to clear the screen and place the cursor in the upper left corner
- light_on_dark() to set the video to light characters on a dark background
- dark_on_light() to set the video to dark characters on a light background
- flash_screen(wait_time=0.03): flash dark_on_light then light_on_dark, with a given wait in between.  Used as a visual BELL
