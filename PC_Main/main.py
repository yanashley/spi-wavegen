import sys
import time
import threading
from pyftdi.spi import SpiController

# Shared variable and lock
current_command = bytes([0x0])
command_lock = threading.Lock()

def initializeSPI():
    """
    Initializes SPI controller
    """
    spi = SpiController()
    spi.configure('ftdi://::/1')  # Use first FTDI device found
    controller = spi.get_port(cs=0, freq=1_000_000, mode=0)  # CS0, 1 MHz, SPI mode 0
    return spi, controller

def input_thread():
    """
    Thread that waits for user input and updates the command
    """
    global current_command
    while True:
        user_input = input("Enter 4-bit binary command (e.g., 0101): ").strip()
        if len(user_input) != 4 or any(c not in '01' for c in user_input):
            print("Invalid input. Enter exactly 4 bits (e.g., 0101).")
            continue
        nibble = int(user_input, 2)
        full_byte = nibble << 4  # Move to upper nibble
        with command_lock:
            current_command = bytes([full_byte])
            print(f"New command set: {current_command.hex()}")

def main():
    global current_command
    spi, controller = initializeSPI()

    # Start the input thread
    threading.Thread(target=input_thread, daemon=True).start()

    try:
        while True:
            with command_lock:
                tx = current_command
            rx = controller.exchange(tx, duplex=True)
            print(f"Sent: {tx.hex()} | Received: {rx.hex()}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped by user.")
        spi.terminate()

if __name__ == "__main__":
    main()
