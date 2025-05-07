`include "spi_client_test.sv"

module top(
    input logic     clk,
    input logic     rst,
    input logic     _31b,
    input logic     _29b,
    input logic     _37a,
    output logic    _9b,    // D0
    output logic    _6a,    // D1
    output logic    _4a,    // D2
    output logic    _2a,    // D3
    output logic    _0a,    // D4
    output logic    _5a,    // D5
    output logic    _3b,    // D6
    output logic    _49a,   // D7
);

    logic [3:0] selector = 4'b0000;
    logic [7:0] command;
    logic selector_sig;
    logic clk_out;
    // logic counter = 0;

    spi_client_test spi(
        .clk            (clk),
        .rst            (rst),
        .spi_clk        (_31b),
        .mosi           (_29b),
        .cs             (_37a),
        .command        (command),
        .command_signal (selector_sig)
    );
    
    // 8'b11111111
    // 8'b00000000

    // assign {_49a, _3b, _5a, _0a, _2a, _4a, _6a, _9b} = 8'b00000000;

    always_ff@(posedge clk) begin
        if (selector_sig == 1'b1) begin
            {_49a, _3b, _5a, _0a, _2a, _4a, _6a, _9b} <= command;
        end
    end
    
endmodule
