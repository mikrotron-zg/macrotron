# Macrotron
DIY macro keypad with USB-C, WiFi and BLE conenctivity.

## Hardware
Hardware list is quite short:
* [Adafruit QT Py S3 with 2MB PSRAM](https://www.diykits.eu/products/p_12501)
* [NeoKey 1x4 QT I2C](https://www.diykits.eu/products/p_12552)
* [4 Cherry MX compatible switches](https://www.diykits.eu/products/p_12553)
* [4 keycaps](https://www.diykits.eu/products/p_12554)
* [Qwiic/StemmaQT/EasyC cable - 10 cm long](https://www.diykits.eu/products/p_11733)
* 3D printed box (see the [model README](model/README.md) for details)

## Software
You'll need [CircuitPython](https://circuitpython.org/) 9.x on board, you can download it [here](https://circuitpython.org/board/adafruit_qtpy_esp32s3_4mbflash_2mbpsram/). 

All libraries used by this project can be found under _src/lib/_, copy this directory to the board after you've installed CircuitPython. The documentation can be found [here](https://docs.circuitpython.org/), e.g. [HID library docs](https://docs.circuitpython.org/projects/hid/en/latest/). If you're using non-US keyboard layout, you might want to add [Circuitpython_Keyboard_Layouts](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts/tree/main) by [Neradoc](https://github.com/Neradoc) to the project.

You'll need some kind of IDE - Adafruit recommends [Mu Editor](https://codewith.mu/).

## Code

First, copy the contents of _src_ directory to QT Py - it'll restart automatically and you should have basic functions working: _copy/paste/undo/save_ (from left to right). You can open _code.py_ file and make some changes - as soon as you save the file the board restarts and your new code is now working.

To try something else, go to _examples/[example_name]_ directory and copy _code.py_ to the board. Each example has a comment block at the beginning explaning what it does, feel free to experiment with it!