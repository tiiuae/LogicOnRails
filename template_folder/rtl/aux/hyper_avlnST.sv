module hyper_avlnST #(
    parameter DATA_WIDTH = 1
)( 
    input  logic                  i_clk,
    input  logic                  i_rst_n,

    input  logic [DATA_WIDTH-1:0] i_data,
    input  logic                  i_vld,
    input  logic                  i_sof,
    input  logic                  i_eof,
    output logic [DATA_WIDTH-1:0] o_data,
    output logic                  o_vld,
    output logic                  o_sof,
    output logic                  o_eof
);

//##################################
//          SIGNALS
//##################################

logic [DATA_WIDTH-1:0] w_data;
logic                  w_sof;
logic                  w_eof;
logic                  r_vld;

//##################################
//          REGS
//##################################

hyper_reg #(
    .DATA_WIDTH(DATA_WIDTH)
) hyper_reg_data_inst (
    .i_clk(i_clk),
    .i_data(i_data),
    .o_data(w_data)
);

hyper_reg #(
    .DATA_WIDTH(1)
) hyper_reg_sof_inst (
    .i_clk(i_clk),
    .i_data(i_sof),
    .o_data(w_sof)
);

hyper_reg #(
    .DATA_WIDTH(1)
) hyper_reg_eof_inst (
    .i_clk(i_clk),
    .i_data(i_eof),
    .o_data(w_eof)
);

always_ff @(posedge i_clk or negedge i_rst_n) begin
    if (i_rst_n == 1'b0) begin
        r_vld <= 1'b0;
    end else begin
        r_vld <= i_vld;
    end 
end 

//##################################
//          OUTPUT
//##################################

assign o_data = w_data;
assign o_sof  = w_sof;
assign o_eof  = w_eof;
assign o_vld  = r_vld;

endmodule