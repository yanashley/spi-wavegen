module var_clk(
    input logic clk,
    input logic rst,
    input logic [3:0] selector,
    output logic clk_out
);
    // Counter for clock division
    logic [1:0] counter;
    
    always_ff @(posedge clk) begin
        if (rst) begin
            counter <= 2'b00;
            clk_out <= 1'b0;
        end
        else begin
            // Update counter
            counter <= counter + 1'b1;
            
            case (selector[1:0])
                2'b00: begin  // Half frequency (toggle every 2 cycles)
                    if (counter[0] == 1'b1)  // Every 2 clock cycles
                        clk_out <= ~clk_out;
                end
                
                2'b01: begin  // Same frequency as input clock
                    clk_out <= ~clk_out;  // Toggle every cycle
                end
                
                2'b10: begin  // Quarter frequency (toggle every 4 cycles)
                    if (counter == 2'b11)  // Every 4 clock cycles
                        clk_out <= ~clk_out;
                end
                
                default: begin  // Default to same as input clock
                    clk_out <= ~clk_out;
                end
            endcase
        end
    end
endmodule
