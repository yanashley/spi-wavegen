import sys
import time
from pyftdi.spi import SpiController

# runs in a loop; take command line input to change --> store in variable (starts with a default)

def initializeSPI():
    """
    Initializes SPI controller

    Returns:
        A controller
    """
    spi = SpiController()
    spi.configure('ftdi://::/1')  # Use first FTDI device found

    controller = spi.get_port(cs=0, freq=100_000, mode=0)  # CS0, 100 kHz, SPI mode 0
    return spi, controller

def handleInput():
    """
    Handles user input to change the frequency options

    Returns:
        The bytes to send
    """
    # input should be in hex
    user_input = input("Enter hex string (e.g. DEADBEEF): ")
    try:
        tx_bytes = bytes.fromhex(user_input)
    except ValueError:
        print("Invalid hex string")
        exit(1)
    # parse input (TODO: correspond to options later; for now actually use input from CLI)

    print(f"Input is: {tx_bytes}")
    return tx_bytes

def main():
    # Initialize SPI
    spi, controller = initializeSPI()

    tx_bytes = 0x00 # set to a default 
    tx_bytes = handleInput()

    try:
        while True:
            # Send the SPI command and receive the response
            rx_bytes = controller.exchange(tx_bytes, duplex=True)
            print(f"Sent: {tx_bytes.hex()} | Received: {rx_bytes.hex()}")
            time.sleep(1)  # Send every second, adjust for faster/slower
    except KeyboardInterrupt:
        print("\nContinuous sending stopped by user.")

    spi.terminate()

if __name__ == "__main__":
    main()
