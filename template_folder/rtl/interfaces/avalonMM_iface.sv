
interface avalonMM_iface 
#(
    parameter DATA_WIDTH = 512,
    parameter ADDR_WIDTH = 22,
    parameter BYTEEN_WIDTH = DATA_WIDTH/8,
    parameter BURST_WIDTH = 4, 
    parameter WAIT_REQ_ALLOWANCE = 16
)
(
    input logic i_clk
);
//##################################
//         SIGNALS
//##################################
    logic                    if_wr;
    logic                    if_rd;
    logic                    if_rddata_vld;
    logic                    if_waitreq;
    logic [ADDR_WIDTH-1:0]   if_addr;
    logic [DATA_WIDTH-1:0]   if_wrdata;
    logic [DATA_WIDTH-1:0]   if_rddata;
    logic [BYTEEN_WIDTH-1:0] if_byteen;
    logic [BURST_WIDTH-1:0]  if_burst_c;


//##################################
//         MODPORT
//##################################

modport master (
    output if_wr,
    output if_rd,
    output if_addr,
    output if_wrdata,
    output if_byteen,
    output if_burst_c,
    input  if_waitreq,
    input  if_rddata,
    input  if_rddata_vld
);

modport slave (
    input  if_wr,
    input  if_rd,
    input  if_addr,
    input  if_wrdata,
    input  if_byteen,
    input  if_burst_c,
    output if_waitreq,
    output if_rddata,
    output if_rddata_vld
);

endinterface