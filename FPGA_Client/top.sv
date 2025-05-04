`include "memory.sv"
`include "spi_client.sv"
`include "var_clk.sv"

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
    output logic    _45a,   // D8
    output logic    _48b    // D9
);

    logic [9:0] data;
    logic [3:0] selector = 4'b0000;
    logic [3:0] prev_selector;
    logic selector_sig;
    logic clk_out;

    spi_client spi(
        .clk            (clk),
        .spi_clk        (_31b),
        .mosi           (_29b),
        .cs             (_37a),
        .command        (prev_selector),
        .command_signal (selector_sig)
    )

    always_ff @(posedge selector_sig) begin
        selector <= prev_selector;
    end

    var_clk var_clk(
        .clk            (clk),
        .selector       (selector),
        .clk_out        (clk_out)
    )

    memory #(
        .INIT_FILE      ("sine.txt")
    ) u1 (
        .clk            (clk_out), 
        .selector       (selector),
        .read_data      (data)
    );

    assign {_48b, _45a, _49a, _3b, _5a, _0a, _2a, _4a, _6a, _9b} = data;
endmodule
