interface AXI_Lite_iface 
#( 
    parameter ADDR_WIDTH = 16,
    parameter DATA_WIDTH = 64
)
(
    input logic i_clk,
    input logic i_rst_n
);
//##################################
//         SIGNALS
//##################################

// READ ADDRESS CHANNEL
logic [ADDR_WIDTH-1:0]   if_araddr;
logic [2:0]              if_arprot;
logic                    if_arvalid;
logic                    if_arready;

//READ DATA CHANNEL;
logic [DATA_WIDTH-1:0]   if_rdata;
logic [1:0]              if_rresp;
logic                    if_rvalid;
logic                    if_rready; 

// WRITE ADDRESS CHANNEL
logic [ADDR_WIDTH-1:0]   if_awaddr;
logic [2:0]              if_awprot;
logic                    if_awvalid;
logic                    if_awready;

//WRITE DATA CHANNEL;
logic [DATA_WIDTH-1:0]   if_wdata;
logic [DATA_WIDTH/8-1:0] if_wstrb;
logic                    if_wvalid;
logic                    if_wready; 

//WRITE RESPONSE CHANNEL;
logic [1:0]              if_bresp;
logic                    if_bvalid;
logic                    if_bready;


//##################################
//         MODPORT
//##################################

modport master (
    output if_araddr,
    output if_arprot,
    output if_arvalid,
    input  if_arready,  

    input  if_rdata,
    input  if_rresp,
    input  if_rvalid,
    output if_rready, 

    output if_awaddr,
    output if_awprot,
    output if_awvalid,
    input  if_awready,

    input  if_wdata,
    input  if_wstrb,
    input  if_wvalid,
    output if_wready,

    input  if_bresp,
    input  if_bvalid,
    output if_bready
);

modport slave (
    input  if_araddr,
    input  if_arprot,
    input  if_arvalid,
    output if_arready,  

    output if_rdata,
    output if_rresp,
    output if_rvalid,
    input  if_rready, 

    input  if_awaddr,
    input  if_awprot,
    input  if_awvalid,
    output if_awready,

    output if_wdata,
    output if_wstrb,
    output if_wvalid,
    input  if_wready,

    output if_bresp,
    output if_bvalid,
    input  if_bready
);

endinterface