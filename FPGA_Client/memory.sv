module memory #(
    parameter INIT_FILE = ""
)(
    input logic     clk, rst, 
    input logic     [3:0] selector,
    output logic    [9:0] read_data
);

    // Declare memory array for storing 512 10-bit samples of a sine function
    logic [9:0] sample_memory [0:2047];
    logic [8:0] read_address = 0;

    initial if (INIT_FILE) begin
        $readmemh(INIT_FILE, sample_memory);
    end

    always_ff @(posedge clk) begin
        // Different waveforms
        case (selector[3:2])
        2'b00: begin
            read_data <= sample_memory[read_address];
        end
        2'b01: begin
            read_data <= sample_memory[read_address + 512];
        end
        2'b10: begin
            read_data <= sample_memory[read_address + 1024];
        end
        2'b11: begin
            read_data <= sample_memory[read_address + 1536];
        end
        default: read_data <= sample_memory[read_address];
        endcase
    end

    always_ff @(posedge clk) begin
        if (rst) begin
            read_address <= 0;
        end 
        else begin
        read_address <= read_address + 1;
        end
    end

endmodule

