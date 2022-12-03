import sys
import time
from random import randint

import nxbt
from nxbt import Buttons
from nxbt import Sticks

# Get number of items to clone from command line
num_items = sys.argv[1]

MACRO_LOOP = f"""
LOOP {num_items}
    A 0.1s
    0.2s
    DPAD_UP 0.2s
    0.2s
    DPAD_UP 0.2s
    0.2s
    A 0.1s
    2.0s
    A 0.1s
    2.0s
    A 0.1s
    3.5s
    A 0.1s
    2.0s
    DPAD_DOWN 0.2s
    0.2s
    DPAD_DOWN 0.2s
    0.2s
    DPAD_RIGHT 0.2s
    0.2s
    A 0.1s
    4.0s
    X 0.1s
    0.2s
    X 0.1s
    0.2s
    L 0.1s
    0.2s
    A 0.1s
    0.2s
    DPAD_DOWN 0.2s
    0.2s
    DPAD_DOWN 0.2s
    0.2s
    DPAD_DOWN 0.2s
    0.2s
    A 0.1s
    2.0s
    B 0.1s
    3.0s
    DPAD_LEFT 0.2s
    2.0s
"""

MACRO = """
A 0.75s
0.2s
DPAD_UP 0.1s
0.2s
DPAD_UP 0.1s
0.2s
A 0.75s
1.5s
A 0.75s
1.5s
A 0.75s
3.0s
A 0.75s
1.5s
DPAD_DOWN 0.1s
0.2s
DPAD_DOWN 0.1s
0.2s
DPAD_RIGHT 0.1s
0.2s
A 0.75s
3.5s
X 0.75s
0.2s
X 0.75s
0.2s
L 0.75s
0.2s
A 0.75s
0.2s
DPAD_DOWN 0.1s
0.2s
DPAD_DOWN 0.1s
0.2s
DPAD_DOWN 0.1s
0.2s
A 0.75s
1.5s
B 0.75s
2.5s
DPAD_LEFT 0.1s
0.2s
"""

def random_colour():
    return [
        randint(0, 255),
        randint(0, 255),
        randint(0, 255),
    ]


if __name__ == "__main__":

    # Init NXBT
    nx = nxbt.Nxbt()

    # Get a list of all available Bluetooth adapters
    print("Setting up Bluetooth...")
    adapters = nx.get_available_adapters()
    # Prepare a list to store the indexes of the
    # created controllers.
    controller_idxs = []
    # Loop over all Bluetooth adapters and create
    # Switch Pro Controllers
    for i in range(0, len(adapters)):
        index = nx.create_controller(
            nxbt.PRO_CONTROLLER,
            adapter_path=adapters[i],
            colour_body=random_colour(),
            colour_buttons=random_colour())
        controller_idxs.append(index)

    # Select the last controller for input
    controller_idx = controller_idxs[-1]

    # Wait for the switch to connect to the controller
    print("Awaiting connection... ", end="")
    nx.wait_for_connection(controller_idx)
    print("Connected")

    # Begin macro
    print(f"Macro Started: clone items ({num_items})")
    time.sleep(2)
    print("Returning to home menu...")
    nx.press_buttons(controller_idx, [Buttons.HOME])
    time.sleep(2)
    print("Returning to game...")
    nx.press_buttons(controller_idx, [Buttons.HOME])
    time.sleep(2)
    print("Begin inputs...")
    start = time.time()
    temp_time = start

    try:
        for i in range(int(num_items)):
            macro_id = nx.macro(controller_idx, MACRO)
            elapsed = time.time() - temp_time
            temp_time = time.time()
            print(f"loop complete: {elapsed:.2f}s ({i + 1}/{num_items})", end="\r")

            # reset the macro every few loops in case it misses an input?
            if (i + 1) % 50 == 0:
                print(f"resetting position: cancelling...", end="\r")
                for j in range(15):
                    nx.press_buttons(controller_idx, [Buttons.B])
                    time.sleep(0.5)
                print(f"resetting position: finishing up...", end="\r")
                nx.press_buttons(controller_idx, [Buttons.X])
                time.sleep(0.2)
                nx.press_buttons(controller_idx, [Buttons.DPAD_LEFT])
                time.sleep(0.2)
                nx.press_buttons(controller_idx, [Buttons.DPAD_UP], 3)
                time.sleep(0.2)
                nx.press_buttons(controller_idx, [Buttons.DPAD_DOWN])
                time.sleep(0.2)
                print(f"resetting position: done            ", end="\r")
    except:
        print(f"Macro failed; ", end="")
    finally:
        print(f"\nExiting... ({time.time() - start:.2f}s)")
