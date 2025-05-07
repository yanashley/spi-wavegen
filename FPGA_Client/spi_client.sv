module spi_client(
    input logic     clk, // must be 1.5 x faster than controller (curently at 100 kHz)
    input logic     rst,
    input logic     spi_clk, // can make this _31b
    input logic     mosi,    // can make this _29b
    input logic     cs,      // can make this _37a  

    output logic [7:0] command,
    output logic command_signal
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
            cs_sync   <= {cs_sync[0], cs};
        end
    end

    assign spi_clk_rising = (spi_clk_sync == 2'b01); // 01 referring to rising edge

    // Shift register and bit counter for full byte command
    logic [7:0] shift_reg;
    logic [3:0] bit_count;
    logic receiving;

    always_ff @(posedge clk) begin
        if (rst) begin
            shift_reg <= 8'b0;
            bit_count <= 4'd0;
            command       <= 8'b0;
            command_signal <= 1'b0;
            receiving <= 1'b0;
        end else begin
            command_signal <= 1'b0;

            if (cs_sync[1] == 1'b0) begin  // when CS currently active low
                if (!receiving) begin
                    receiving <= 1'b1; // set high on first 
                    bit_count <= 4'b0;
                end

                if (spi_clk_rising) begin // if SPI clk on a rising edge 
                    shift_reg <= {shift_reg[6:0], mosi};  // Shift in 1 bit
                    bit_count <= bit_count + 1;

                    if (bit_count == 4'd7) begin // once it hits 7
                        command       <= {shift_reg[6:0], mosi};  // Capture full 4-bit command (final one with mosi)
                        command_signal <= 1'b1;
                        bit_count <= 4'd0; // reset 
                    end
                end
            end else begin
                receiving <= 1'b0;
                bit_count <= 4'd0; // reset count on CS deassert
            end
        end
    end

endmodule
