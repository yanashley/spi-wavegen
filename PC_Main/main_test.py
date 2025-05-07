import time
from pyftdi.spi import SpiController

def initializeSPI():
    """
    Initializes SPI controller
    """
    spi = SpiController()
    spi.configure('ftdi://::/1')  # Use first FTDI device found
    controller = spi.get_port(cs=0, freq=1_000_000, mode=0)  # CS0, 1 MHz, SPI mode 0
    return spi, controller

def main():
    spi, controller = initializeSPI()

    tx = bytes([0xFF]) #    send 11111111
    rx = controller.exchange(tx, duplex=True)
    print(f"Sent: {tx.hex()} | Received: {rx.hex()}")

    spi.close(freeze=False)

    # try:
    #     while True:
    #         tx = bytes([0xFF]) # send 11111111
    #         rx = controller.exchange(tx, duplex=True)
    #         print(f"Sent: {tx.hex()} | Received: {rx.hex()}")
    #         # time.sleep(1) # every 1 second
    # except KeyboardInterrupt:
    #     spi.close(freeze=True)

if __name__ == "__main__":
    main()
