# Uno_IR_KMK
This repository contains the code (and compiled circuitpython .uf2) to run KMK on the Uno IR.  This includes the keyboard files for easy remapping, as well as a plugin/module to handle the infrared decoding.

## IR Decoding
The IR Decoding module is, to the best of my knowledge, a novel approach: it should handle most IR protocols and deocde consistently - though it may not always decode in the manner intended by the manufacturer.  It has so far been tested with NEC and Sony IR protocols, but is generic enough that I expect it to work with most consumer remotes.

## Installation
When you plug the Uno IR into your computer, a new drive will mount (like a USB flash drive) named "RPI-RP2".
1. Copy the ```firmware.uf2``` file to this drive.  After the copy finishes (it will take a minute), the drive should automatically unmount, then a new drive will mount named "CIRCUITPY".
2. Delete all the files on the CIRCUITPY drive.
3. Copy all the files inside the "board" directory from this repository into the CIRCUITPY drive.  The file structure should now look like: ```CIRCUITPY/uno.py``` and ```CIRCUITPY/IRModule.py```... etc.
4. Choose which example you want to work from - I've provided an example for the button only, the encoder, or the IR module that should all be fairly self-explanatory - you can build your own version, too.  Depending on which option you want, look in the "options" folder, pick a subfolder, and copy the contents to ```CIRCUITPY/``` - you should now have a ```CIRCUITPY/main.py``` plus, potentially, a couple other files (depending on the example).

## NOTE:
With the boot.py that's included here, the "CIRCUITPY" drive will only mount *if you press the keyswitch down while plugging the uno in* - if you don't want that, don't copy the boot.py over.  If you've done so and you don't have a keyswitch, you can reset to the "RPI-RP2" stage by pressing and holding the button on the back of the uno near the center (I'll call this "BOOT0").  While holding, tap the button closer to the edge (RESET) once.  Then release BOOT0, and you should be back to stage 1 in the "installation" instructions above.

## Modification
```main.py``` contains the keymap (keyboard.keymap) and the IR Map (irHandler.map) (like a keymap, but maps IR codes to functions instead of button presses to functions), as well as the encoder map (encoder_handler.map) if you've soldered an encoder on.  For instructions on how to build macros, etc, I recommend taking a look at the [KMK Documentation](http://kmkfw.io).  The different examples in "options" show how to use the different map options.