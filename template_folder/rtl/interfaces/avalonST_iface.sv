
interface avalonST_iface 
#(
    parameter DATA_WIDTH = 512
)
(
    input logic i_clk
);
//##################################
//         SIGNALS
//##################################
    logic                  if_rdy;
    logic                  if_vld;
    logic [DATA_WIDTH-1:0] if_data;

//##################################
//         MODPORT
//##################################

modport source (
    output if_vld,
    output if_data,
    input  if_rdy
);

modport sink (
    input  if_vld,
    input  if_data,
    output if_rdy
);

endinterface