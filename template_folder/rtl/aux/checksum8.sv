module checksum8 (
    input  logic       i_clk,
    input  logic       i_rst_n,
    input  logic [7:0] i_data_A,
    input  logic [7:0] i_data_B,
    output logic [7:0] o_checksum
);

////////////////////////////////////////
//                signal
////////////////////////////////////////

logic [7:0] r_checksum;

////////////////////////////////////////
//                lfsra
////////////////////////////////////////

always_ff @(posedge i_clk or negedge i_rst_n) begin
    if (i_rst_n == 1'b0) begin
        r_checksum <= 8'h00;
    end else begin
        r_checksum <= i_data_A + i_data_B;
    end
end

////////////////////////////////////////
//                outputs
////////////////////////////////////////

assign o_checksum = r_checksum;

endmodule
