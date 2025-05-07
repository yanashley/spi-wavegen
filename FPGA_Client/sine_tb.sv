`timescale 10ms/10ms
`include "top.sv"

module sine_tb;

    logic clk = 0;
    logic _9b, _6a, _4a, _2a, _0a, _5a, _3b, _49a, _45a, _48b;
    logic [3:0] selector = 4'b0000;

    top u0 (
        .clk    (clk), 
        ._9b    (_9b), 
        ._6a    (_6a), 
        ._4a    (_4a), 
        ._2a    (_2a), 
        ._0a    (_0a), 
        ._5a    (_5a), 
        ._3b    (_3b), 
        ._49a   (_49a), 
        ._45a   (_45a), 
        ._48b   (_48b)
    );

    initial begin
        $dumpfile("sine.vcd");
        $dumpvars(0, sine_tb);
        u0.selector = 4'b0000;
        #10000
        $finish;
    end

    always begin
        #4
        clk = ~clk;
    end

endmodule

