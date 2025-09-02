module hyper_reg #(
    parameter DATA_WIDTH = 1
) (
    input  logic                  i_clk,      
    input  logic [DATA_WIDTH-1:0] i_data,
    output logic [DATA_WIDTH-1:0] o_data
);

//##################################
//          SIGNALS
//##################################

logic [DATA_WIDTH-1:0] r_data;

//##################################
//          REGS
//##################################

always_ff @(posedge i_clk) begin
    r_data <= i_data;
end 

//##################################
//          OUTPUT
//##################################

assign o_data = r_data;

endmodule