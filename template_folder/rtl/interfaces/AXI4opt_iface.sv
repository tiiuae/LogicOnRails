//#####################################################################
//# File Name : AXI4opt_iface.sv
//# Purpose : AXI4 + aditional optional Interface
//# Format : System Verilog
//# Creation Date : 2025-08
//# Created By : Matheus Ferronato
//#####################################################################
interface AXI4opt_iface 
#( 
    parameter ADDR_WIDTH = 16,
    parameter DATA_WIDTH = 64,
    parameter ID_WIDTH   = 4,
    parameter USER_WIDTH = 8
)
(
    input logic i_clk,
    input logic i_rst_n
);
//##################################
//         SIGNALS
//##################################

// READ ADDRESS CHANNEL
logic [1:0]              if_arburst; 
logic [7:0]              if_arlen;  
logic [2:0]              if_arsize; 
logic [ADDR_WIDTH-1:0]   if_araddr;
logic                    if_arvalid;
logic                    if_arready;
logic [ID_WIDTH-1:0]     if_arid;
logic [USER_WIDTH-1:0]   if_aruser;
logic [1:0]              if_arlock;
logic [3:0]              if_arcache;
logic [2:0]              if_arprot;
logic [3:0]              if_arqos;
logic [3:0]              if_arregion;

//READ DATA CHANNEL;
logic [DATA_WIDTH-1:0]   if_rdata;
logic [1:0]              if_rresp;
logic                    if_rlast; 
logic                    if_rvalid;
logic                    if_rready; 
logic [USER_WIDTH-1:0]   if_ruser;
logic [ID_WIDTH-1:0]     if_rid;

// WRITE ADDRESS CHANNEL
logic [1:0]              if_awburst;
logic [7:0]              if_awlen;  
logic [2:0]              if_awsize; 
logic [ADDR_WIDTH-1:0]   if_awaddr;
logic                    if_awvalid;
logic                    if_awready;
logic [ID_WIDTH-1:0]     if_awid;
logic [USER_WIDTH-1:0]   if_awuser;
logic [1:0]              if_awlock;
logic [3:0]              if_awcache;
logic [2:0]              if_awprot;
logic [3:0]              if_awqos;
logic [3:0]              if_awregion;


//WRITE DATA CHANNEL;
logic [DATA_WIDTH-1:0]   if_wdata;
logic [DATA_WIDTH/8-1:0] if_wstrb;
logic [USER_WIDTH-1:0]   if_wuser;
logic                    if_wlast;
logic                    if_wvalid;
logic                    if_wready; 

//WRITE RESPONSE CHANNEL;
logic [1:0]              if_bresp;
logic                    if_bvalid;
logic                    if_bready;
logic [USER_WIDTH-1:0]   if_buser;
logic [ID_WIDTH-1:0]     if_bid;


//##################################
//         MODPORT
//##################################

modport master (
    output if_arburst,
    output if_arlen,
    output if_arsize,    
    output if_araddr,
    output if_arvalid,
    output if_arid,
    output if_arlock,
    output if_arcache,
    output if_arprot,
    output if_arqos,
    output if_arregion,
    output if_aruser,
    input  if_arready,  

    input  if_rdata,
    input  if_rresp,
    input  if_rvalid,
    input  if_rlast,
    input  if_rid,
    input  if_ruser,
    output if_rready, 

    output if_awburst,
    output if_awlen,
    output if_awsize,
    output if_awaddr,
    output if_awvalid,
    output if_awid,
    output if_awlock,
    output if_awcache,
    output if_awprot,
    output if_awqos,
    output if_awregion,
    output if_awuser,    
    input  if_awready,

    output if_wdata,
    output if_wstrb,
    output if_wvalid,
    output if_wlast,
    output if_wuser,    
    input  if_wready,

    input  if_bresp,
    input  if_bvalid,
    input  if_bid,
    input  if_buser,
    output if_bready
);

modport slave (
    input  if_arburst,
    input  if_arlen,
    input  if_arsize,     
    input  if_araddr,
    input  if_arvalid,
    input  if_arid,
    input  if_arlock,
    input  if_arcache,
    input  if_arprot,
    input  if_arqos,
    input  if_arregion,
    input  if_aruser,        
    output if_arready,  

    output if_rdata,
    output if_rresp,
    output if_rvalid,
    output if_rlast,
    output if_rid,
    output if_ruser,
    input  if_rready, 

    input  if_awburst,
    input  if_awlen,
    input  if_awsize,
    input  if_awaddr,
    input  if_awvalid,
    input  if_awid,
    input  if_awlock,
    input  if_awcache,
    input  if_awprot,
    input  if_awqos,
    input  if_awregion,
    input  if_awuser,    
    output if_awready,

    input  if_wdata,
    input  if_wstrb,
    input  if_wvalid,
    input  if_wlast,
    input  if_wuser,
    output if_wready,

    output if_bresp,
    output if_bvalid,
    output if_bid,
    output if_buser,
    input  if_bready
);



endinterface