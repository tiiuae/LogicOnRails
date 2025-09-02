module hyper_iface_avlnST #(
    parameter DATA_WIDTH = 1
) (
    input  logic              i_clk,      
    input  logic              i_rst_n,      
    avalonST_pkt_iface.sink   if_avlnst_snk,
    avalonST_pkt_iface.source if_avlnst_src
);

//##################################
//          SIGNAL
//##################################

logic [DATA_WIDTH-1:0] w_data;
logic                  w_vld;
logic                  w_sof;
logic                  w_eof;

//##################################
//          REGS
//##################################

hyper_avlnST #(
    .DATA_WIDTH( DATA_WIDTH )
) hyper_avlnST_inst (
    .i_clk   ( i_clk                 ),
    .i_rst_n ( i_rst_n               ),
    .i_data  ( if_avlnst_snk.if_data ),
    .i_vld   ( if_avlnst_snk.if_vld  ),
    .i_sof   ( if_avlnst_snk.if_sof  ),
    .i_eof   ( if_avlnst_snk.if_eof  ),
    .o_data  ( w_data                ),
    .o_vld   ( w_vld                 ),
    .o_sof   ( w_sof                 ),
    .o_eof   ( w_eof                 )
);

//##################################
//          OUTPUT
//##################################

assign if_avlnst_src.if_vld  = w_vld;
assign if_avlnst_src.if_data = w_data;
assign if_avlnst_src.if_sof  = w_sof;
assign if_avlnst_src.if_eof  = w_eof;
assign if_avlnst_snk.if_rdy  = if_avlnst_src.if_rdy;

endmodule