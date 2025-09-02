
interface AXI_ST_iface 
#(
    parameter DATA_WIDTH = 512,
    parameter BYTEEN_WIDTH = DATA_WIDTH/8,
    parameter USER_WIDTH = 16
)
(
    input logic i_clk
);
//##################################
//         SIGNALS
//##################################

logic                    if_tvalid;
logic [DATA_WIDTH-1:0]   if_tdata;
logic [BYTEEN_WIDTH-1:0] if_tkeep;
logic                    if_tlast;
logic                    if_tready;

//##################################
//         MODPORT
//##################################

modport source (
    output  if_tvalid,
    output  if_tdata,
    output  if_tkeep,
    output  if_tlast,
    input   if_tready
);

modport sink (
    input  if_tvalid,
    input  if_tdata,
    input  if_tkeep,
    input  if_tlast,
    output if_tready

);

endinterface