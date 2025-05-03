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
    controller = spi.get_port(cs=0, freq=100_000, mode=0)  # CS0, 100 kHz, SPI mode 0
    return spi, controller

def input_thread():
    """
    Thread that waits for user input and updates the command
    """
    global current_command
    while True:
        user_input = input("Enter 1-digit hex command (0-F): ").strip().lower()
        if len(user_input) != 1 or user_input not in "0123456789abcdef":
            print("Invalid input. Enter a single hex digit (0-F).")
            continue
        with command_lock:
            # Send the 4-bit command in the lower nibble (e.g., 0x0A for command A)
            current_command = bytes([int(user_input, 16)])
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
            time.sleep(1)  # Adjust for faster/slower sending
    except KeyboardInterrupt:
        print("\nStopped by user.")
        spi.terminate()

if __name__ == "__main__":
    main()
