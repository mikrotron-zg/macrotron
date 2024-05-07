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
"""Command example file, sends commands* to host (use with caution!):
   #1 - sends 'git status' command
   #2 - sends 'git log --oneline' command
   #3 - sends 'git diff --' command
   #4 - sends 'git branch' command
   * Terminal window should be active and have focus.
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
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Use Stemma QT I2C bus
i2c_bus = board.STEMMA_I2C()

# Create a keyboard object
keyboard = Keyboard(usb_hid.devices)

# Create keyboard layout - see project README if you need to use keyboard 
# layout other than the US layout
layout = KeyboardLayoutUS(keyboard)

# Create a NeoKey object
neokey = NeoKey1x4(i2c_bus, addr=0x30)

# Set Neopixel colors
base_color = 0xFF0077
for i in range(0, 4):
    neokey.pixels[i] = base_color

# Set commands
command = ['git status', 
           'git log --oneline', 
           'git diff --', 
           'git branch']

# Set debounce period
debounce = 0.15

while True:
# Check each button, if pressed, take action
    for i in range(0, 4):
        if neokey[i]:
            layout.write(command[i])
            # Remove next line if you don't want the command to be executed
            keyboard.send(Keycode.ENTER)
            time.sleep(debounce)