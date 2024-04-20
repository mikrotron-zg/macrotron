# ----------------------------------------------------------------------------
# Created By  : Tomislav Preksavec
# Created Date: 2024-04-18
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
"""Simple example file, sets basic keys functions:
   - copy (CTRL+C)
   - paste (CTRL+V)
   - undo (CTRL+Z)
   - save (CTRL+S)
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

# Set keyes - please note that Adafruit provides US keyboard layout only,
# if you run into problems try changing keycode. In this example we're using
# CTRL+Y instead of CTRL+Z to compensate for QWERTZ vs QWERTY layout
key_command = [
    [Keycode.CONTROL, Keycode.C],
    [Keycode.CONTROL, Keycode.V],
    [Keycode.CONTROL, Keycode.Y],
    [Keycode.CONTROL, Keycode.S],
]

# Set Neopixel colors
base_color = 0x0000FF
for pixel in neokey.pixels:
    pixel = base_color
response_color = [0xFF0000, 0x00FFFF, 0x00FF00, 0xFFFFFF]

# Set debounce period
debounce = 0.15

# Check each button, if pressed, send keystrokes to host
while True:
    for i in range(0, 4):
        if neokey[i]:
            neokey.pixels[i] = response_color[i]
            print('Pressed key #', i + 1)
            keyboard.send(key_command[i][0], key_command[i][1])
            time.sleep(debounce)
            
        neokey.pixels[i] = base_color