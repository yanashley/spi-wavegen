module spi_client(
    input logic     clk, // must be 1.5 x faster than controller (curently at 100 kHz)
    input logic     rst,
    input logic     spi_clk, // can make this _31b
    input logic     mosi,    // can make this _29b
    input logic     cs,      // can make this _37a  

    output logic [3:0] command,
    output logic    command_signal
);

    // Synchronize external SPI signals to system clock
    logic [1:0] spi_clk_sync, cs_sync;
    logic spi_clk_rising; 

    // handle clock domain crossing -- flip flops to capture SPI controller edges
    always_ff @(posedge clk) begin
        if (rst) begin // initial values
            spi_clk_sync <= 2'b00;
            cs_sync   <= 2'b11;
        end else begin
            spi_clk_sync <= {spi_clk_sync[0], spi_clk}; // pass SPI clk in
            cs_sync   <= {cs_sync[0], cs_n};
        end
    end

    assign spi_clk_rising = (sclk_sync == 2'b01); // 01 referring to rising edge

    // Shift register and bit counter for 4-bit command
    logic [3:0] shift_reg;
    logic [1:0] bit_count;
    logic receiving;

    always_ff @(posedge clk) begin
        if (rst) begin
            shift_reg <= 4'd0;
            bit_count <= 2'd0;
            command_signal <= 1'b0;
            command       <= 4'd0;
            receiving <= 1'b0;
        end else begin
            command_signal <= 1'b0;

            if (cs_sync[1] == 1'b0) begin  // when CS currently active low
                if (!receiving) begin
                    receiving <= 1'b1;
                    bit_count <= 2'd0;
                end

                if (sclk_rising && bit_count < 2'd4) begin // if SPI clk on a rising edge + only take first 4 bits
                    shift_reg <= {shift_reg[2:0], mosi};  // Shift in 1 bit
                    bit_count <= bit_count + 2'd1;

                    if (bit_count == 2'd3) begin
                        command       <= {shift_reg[2:0], mosi};  // Capture full 4-bit command (final one with mosi)
                        command_signal <= 1'b1;
                        bit_count <= 2'd0; // reset 
                    end
                end
            end else begin
                receiving <= 1'b0;
            end
        end
    end

endmodule
