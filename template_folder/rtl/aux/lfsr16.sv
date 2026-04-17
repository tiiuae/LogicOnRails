module lfsr16 (
    input  logic        i_clk,
    input  logic        i_rst_n,
    input  logic        i_en,
    input  logic        i_load,
    input  logic [15:0] i_seed,
    output logic [15:0] o_lfsr
);

////////////////////////////////////////
//                signal
////////////////////////////////////////

logic        w_feedback;
logic        w_lfeedback;
logic [15:0] r_lfsr;

////////////////////////////////////////
//                lfsra
////////////////////////////////////////

// Max-length polynomial: x^16 + x^14 + x^13 + x^11 + 1
assign w_feedback = r_lfsr[15] ^ r_lfsr[13] ^ r_lfsr[12] ^ r_lfsr[10];
assign w_lfeedback = i_seed[15] ^ i_seed[13] ^ i_seed[12] ^ i_seed[10];

always_ff @(posedge i_clk or negedge i_rst_n) begin
    if (i_rst_n == 1'b0) begin
        r_lfsr <= 16'h0001;
    end else begin
        if (i_load == 1'b1) begin
            r_lfsr <= {i_seed[14:0], w_lfeedback};
        end else begin
            if (i_en == 1'b1) begin
                r_lfsr <= {r_lfsr[14:0], w_feedback};
            end
        end
    end
end

////////////////////////////////////////
//                outputs
////////////////////////////////////////

assign o_lfsr = r_lfsr;

endmodule
