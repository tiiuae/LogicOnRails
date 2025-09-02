
interface avalonST_pkt_iface 
#(
    parameter DATA_WIDTH = 512
)
();
//##################################
//         SIGNALS
//##################################

    logic                  if_rdy;
    logic                  if_vld;
    logic [DATA_WIDTH-1:0] if_data;
    logic                  if_sof;
    logic                  if_eof;


//##################################
//         MODPORT
//##################################

modport source (
    output if_vld,
    output if_data,
    output if_sof,
    output if_eof,
    input  if_rdy
);

modport sink (
    input  if_vld,
    input  if_data,
    input  if_sof,
    input  if_eof,
    output if_rdy
);

endinterface