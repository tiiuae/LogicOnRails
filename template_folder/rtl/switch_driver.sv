`timescale 1ns/1ps

module switch_driver (
    input  logic       i_clk,
    input  logic       i_rst_n,
    input  logic [1:0] i_data,
    output logic [1:0] o_data
);


////////////////////////////////////////
//                signals
////////////////////////////////////////

logic [1:0] r_data;

////////////////////////////////////////
//                sum
////////////////////////////////////////

always_ff @(posedge i_clk or negedge i_rst_n)
begin
    if(i_rst_n == 1'b0) begin
        r_data <= 'b0;
    end else begin
        r_data <= {1'b0, i_data[0]} + {1'b0, i_data[1]};
    end
end


////////////////////////////////////////
//                outputs
////////////////////////////////////////

assign o_data = r_data;

endmodule
