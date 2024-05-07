# ----------------------------------------------------------------------------
# Created By  : Tomislav Preksavec
# Created Date: 2024-05-07
# version ='1.0'
# This file is part of macrotron project
# (https://github.com/mikrotron-zg/macrotron).
# Developed by Mikrotron d.o.o. (http://mikrotron.hr)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version. See the LICENSE file at the
# top-level directory of this distribution for details
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# ---------------------------------------------------------------------------
"""Dynamic example file, changes key functions on interaction:
   #1 - copy (CTRL+C) -> after first click changes to CTRL+V, then changes back
     to CTRL+C after next click
   #2 - paste (CTRL+V) -> after first click on first key changes to 
     CTRL+SHIFT+ALT+V, reverts to CTRL+V only when the first key reverts to 
     CTRL+C
   #3 - toggles between bold, italic and underline
   #4 - toggles between center, justify, right and left align
   Keys change colors to indicate if they are in the base or alternate state.
   Keys #3 and #4 revert to the base state if not pressed for certain amount
   of time, defined by key_timeout variable.
   Needs Adafruit QT Py ESP32-S3 with Circuit Python 9.x installed to run, see
   https://learn.adafruit.com/adafruit-qt-py-esp32-s3/circuitpython-2
   for instructions.
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import time
import board
from adafruit_neokey.neokey1x4 import NeoKey1x4
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Use Stemma QT I2C bus
i2c_bus = board.STEMMA_I2C()

# Create a keyboard object
keyboard = Keyboard(usb_hid.devices)

# Create a NeoKey object
neokey = NeoKey1x4(i2c_bus, addr=0x30)

# Set starting key states
key_state = [0, 0, 0, 0]

# Set Neopixel colors
base_color = [0x00FF00, 0x0000FF, 0xAA5500, 0xFFFFFF]
alternate_color = [0x0000FF, 0xFF0077, 0xAA0000, 0xFFFF00]
for i in range(0, 4):
    neokey.pixels[i] = base_color[i]

# Set debounce period
debounce = 0.15

# Set toggle key reset timeout
key_timeout = 2
last_key_press = [0, 0, 0, 0]

# Define first key actions
def first_key_action():
    if key_state[0] == 0:
        key_state[0] = 1
        key_state[1] = 1
        neokey.pixels[0] = alternate_color[0]
        neokey.pixels[1] = alternate_color[1]
        keyboard.send(Keycode.CONTROL, Keycode.C)
    elif key_state[0] == 1:
        key_state[0] = 0
        key_state[1] = 0
        neokey.pixels[0] = base_color[0]
        neokey.pixels[1] = base_color[1]
        keyboard.send(Keycode.CONTROL, Keycode.V)

# Define second key actions
def second_key_action():
    if key_state[1] == 0:
        keyboard.send(Keycode.CONTROL, Keycode.V)
    elif key_state[1] == 1:
        # For M$ Word ommit the ALT key!
        keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.ALT, Keycode.V)        

# Define third key actions
def third_key_action():
    if key_state[2] == 0:
        keyboard.send(Keycode.CONTROL, Keycode.B)
        neokey.pixels[2] = alternate_color[2]
        key_state[2] = 1
        last_key_press[2] = time.time()
    elif key_state[2] == 1:
        keyboard.send(Keycode.CONTROL, Keycode.B)
        keyboard.send(Keycode.CONTROL, Keycode.I)
        key_state[2] = 2
        last_key_press[2] = time.time()
    elif key_state[2] == 2:
        keyboard.send(Keycode.CONTROL, Keycode.I)
        keyboard.send(Keycode.CONTROL, Keycode.U)
        key_state[2] = 3
        last_key_press[2] = time.time()
    elif key_state[2] == 3:
        keyboard.send(Keycode.CONTROL, Keycode.U)
        neokey.pixels[2] = base_color[2]
        key_state[2] = 0

# Define fourth key actions
def fourth_key_action():
    if key_state[3] == 0:
        keyboard.send(Keycode.CONTROL, Keycode.E)
        neokey.pixels[3] = alternate_color[3]
        key_state[3] = 1
        last_key_press[3] = time.time()
    elif key_state[3] == 1:
        keyboard.send(Keycode.CONTROL, Keycode.J)
        key_state[3] = 2
        last_key_press[3] = time.time()
    elif key_state[3] == 2:
        keyboard.send(Keycode.CONTROL, Keycode.R)
        key_state[3] = 3
        last_key_press[3] = time.time()
    elif key_state[3] == 3:
        keyboard.send(Keycode.CONTROL, Keycode.L)
        neokey.pixels[3] = base_color[3]
        key_state[3] = 0

while True:
    # Check each button, if pressed, take action
    for i in range(0, 4):
        if neokey[i]:
            if i == 0:
                first_key_action()
            elif i == 1:
                second_key_action()
            elif i == 2:
                third_key_action()
            elif i == 3:
                fourth_key_action()
            print('Pressed key #', i + 1)
            time.sleep(debounce)
            
        # Check timeouts
        if i > 1 and key_state[i] != 0:
            if (time.time() - last_key_press[i]) > key_timeout:
                key_state[i] = 0
                neokey.pixels[i] = base_color[i]