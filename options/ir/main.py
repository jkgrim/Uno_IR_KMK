# This example demonstrates how to use the IR Demodulator - it has a slot for a button, but if you don't want to use it you can ignore it.
# This example is built around a random sony blu-ray player remote I had laying around, but should be easily adaptable to anything.

# We'll be referencing the make_key, send_string, and simple_key_sequence functions KMK provides.
from kmk.keys import make_key, KC
from kmk.handlers.sequences import send_string, simple_key_sequence

# We'll also be using the uno keyboard definition
from uno import Uno_IR
keyboard = Uno_IR()

# If you want volume up/down buttons, play/pase, you'll need media keys.
from kmk.extensions.media_keys import MediaKeys
keyboard.extensions.append(MediaKeys())

# We'll use the RGB LED to incidate stuff about what's going on
from kmk.extensions.rgb import RGB, AnimationModes
import microcontroller
rgb = RGB(pixel_pin=microcontroller.pin.GPIO4, num_pixels=1)
rgb.val = 10
keyboard.extensions.append(rgb)

# This example also shows how layers work
from kmk.modules.layers import Layers
keyboard.modules.append(Layers())

# Here, we're loading the text from the "macro.txt" file into the key
fp = open("macro.txt", "r")
typeText = fp.read()
print("Loaded text to write:\n", typeText)
macroKey = send_string(typeText)

# And, just to spice things up, we'll make it so that the RGB LED chnages to blue while it types
def setColorKey(color):
    def setColorFunc(key, keyboard, *args, **kwargs):
        nonlocal color
        rgb.hue = color
        rgb.animation_mode = AnimationModes.STATIC
        rgb.animate()
    return make_key(on_press=setColorFunc)
myKey = simple_key_sequence((
    setColorKey((255*2)//3),
    macroKey,
    setColorKey(0),
))

# The keymap for the button is very simple: it's just the letter A.  Feel free to adapt.
keyboard.keymap = [[myKey]]

# We're going to set up everything so the RGB LED can work as a layer indicator
def layerFactory(hue=None, layer=None):
    def colorFunc(key, keyboard, *args, **kwargs):
        nonlocal hue
        rgb.hue = rgb.hue if hue is None else hue
    newKey = make_key(on_press=colorFunc)
    return simple_key_sequence((newKey, KC.RGB_MODE_RAINBOW if hue is None else KC.RGB_MODE_PLAIN, KC.TO(layer)))

# Now we'll build out the keys we'll use in the keymap
R0 = layerFactory(0, 0)
G1 = layerFactory(255//3, 1)
B2 = layerFactory((255*2)//3, 2)
Y3 = layerFactory(None, 3)

# A couple extra keys for special volume effects on MacOS
def addModsSA(key, keyboard, *args):
    keyboard.add_key(KC.LSFT)
    keyboard.add_key(KC.LALT)
def removeModsSA(key, keyboard, *args):
    keyboard.remove_key(KC.LSFT)
    keyboard.remove_key(KC.LALT)

SMALL_VOLU = KC.VOLU.clone()
SMALL_VOLU.before_press_handler(addModsSA)
SMALL_VOLU.after_release_handler(removeModsSA)
SMALL_VOLD = KC.VOLD.clone()
SMALL_VOLD.before_press_handler(addModsSA)
SMALL_VOLD.after_release_handler(removeModsSA)

# The IR Module below is what actually handles listening for codes and mapping them to functions.
from IRModule import IR_Handler
irHandler = IR_Handler()
keyboard.modules.append(irHandler)
irHandler.pin = microcontroller.pin.GPIO25
SEND_IR_CODE = irHandler.newIRKey

irHandler.map = { # Note that transparent keys don't work on the mapping here, every layer just have a value.  transparent might have undefined behavior.
                 "new": (SEND_IR_CODE, SEND_IR_CODE, SEND_IR_CODE, SEND_IR_CODE), # Most people don't have a way to activate the other layers unless they happen to have the exact same remote, so... let's do this: it'll spit it out on every layer (used to only be the last one)
                 "FF1AE5": (R0, R0, R0, R0), # Layer 1
                 "FF9A65": (G1, G1, G1, G1), # Layer 2
                 "FFA25D": (B2, B2, B2, B2), # Layer 3
                 "FF22DD": (Y3, Y3, Y3, Y3), # Layer 4
                 "FF827D": (G1, B2, Y3, R0), # Layer shift
                 "FF3AC5": (KC.VOLU, KC.BRIGHTNESS_UP, SMALL_VOLU, SEND_IR_CODE),
                 "FFBA45": (KC.VOLD, KC.BRIGHTNESS_DOWN, SMALL_VOLD, SEND_IR_CODE),
                 "FF02FD": (KC.LCMD(KC.LCTL(KC.Q)), KC.LCMD(KC.LCTL(KC.Q)), KC.LCMD(KC.LCTL(KC.Q)), SEND_IR_CODE),
                 "FF30CF": (KC.MPRV, KC.MPRV, KC.MPRV, SEND_IR_CODE),
                 "FFB04F": (KC.MPLY, KC.MPLY, KC.MPLY, SEND_IR_CODE),
                 "FF708F": (KC.MNXT, KC.MNXT, KC.MNXT, SEND_IR_CODE),
                 "FFA857": (KC.UP, KC.UP, KC.UP, SEND_IR_CODE),
                 "FF08F7": (KC.LEFT, KC.LEFT, KC.LEFT, SEND_IR_CODE),
                 "FF8877": (KC.DOWN, KC.DOWN, KC.DOWN, SEND_IR_CODE),
                 "FF48B7": (KC.RGHT, KC.RGHT, KC.RGHT, SEND_IR_CODE),
                 "FFE817": (KC.PGUP, KC.PGUP, KC.PGUP, SEND_IR_CODE),
                 "FFC837": (KC.PGDN, KC.PGDN, KC.PGDN, SEND_IR_CODE),
                 "FFE01F": (myKey, myKey, myKey, SEND_IR_CODE),
                 "FF28D7": (KC.LCTL(KC.LEFT), KC.LCTL(KC.LEFT), KC.LCTL(KC.LEFT), SEND_IR_CODE),
                 "FF6897": (KC.LCTL(KC.RGHT), KC.LCTL(KC.RGHT), KC.LCTL(KC.RGHT), SEND_IR_CODE),
                 "FFF807": (KC.F13, KC.F13, KC.F13, SEND_IR_CODE),
                 "FFD827": (KC.LSFT(KC.F13), KC.LSFT(KC.F13), KC.LSFT(KC.F13), SEND_IR_CODE)
}

keyboard.debug_enabled = True

if __name__ == '__main__':
    keyboard.go()
