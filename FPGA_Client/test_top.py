import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.regression import TestFactory
import random

@cocotb.test()
async def test_different_selectors(dut):
    """Test data output for different selector values"""
    
    # Create a clock with 10ns period
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset the DUT
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)
    
    # Mock SPI by directly manipulating selector for testing
    selectors_to_test = [
        0b0000,  # Default
        0b0001,  # Same frequency as base clock
        0b0010,  # Quarter frequency
        0b0100,  # Some other selector value
        0b1010   # Another selector value
    ]
    
    dut._log.info("Starting test of different selector values")
    
    for sel in selectors_to_test:
        # Set the selector value directly for testing
        dut.selector.value = sel
        
        # We need to wait different periods depending on the selector
        # to see the effect of the variable clock
        wait_cycles = 20
        if sel & 0b11 == 0b00:    # Half frequency
            wait_cycles = 40
        elif sel & 0b11 == 0b10:  # Quarter frequency
            wait_cycles = 80
            
        dut._log.info(f"Testing selector value: {sel:04b}")
        
        # Capture data values over multiple clock cycles
        data_values = []
        for _ in range(wait_cycles):
            await RisingEdge(dut.clk)
            data_values.append(int(dut.data.value))
        
        # Log the data pattern
        dut._log.info(f"Data pattern for selector {sel:04b}: {data_values[:10]}...")
        
        # Check if we're getting different values (ensure memory is being read)
        unique_values = set(data_values)
        assert len(unique_values) > 1, f"Data should change for selector {sel:04b}"
        
        # Additional test: verify the memory access patterns based on the clock division
        if sel & 0b11 == 0b00:  # Half frequency
            # Data should change every 2 cycles
            for i in range(2, len(data_values)-2, 2):
                if data_values[i] == data_values[i-2]:
                    dut._log.warning(f"Potential issue: Expected different values at indices {i-2} and {i}")
        
        elif sel & 0b11 == 0b10:  # Quarter frequency
            # Data should change every 4 cycles
            for i in range(4, len(data_values)-4, 4):
                if data_values[i] == data_values[i-4]:
                    dut._log.warning(f"Potential issue: Expected different values at indices {i-4} and {i}")
    
    dut._log.info("Test completed successfully")
