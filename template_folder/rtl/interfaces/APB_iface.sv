interface APB_iface 
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

logic                  if_pclk;
logic                  if_prst_n;
logic [ADDR_WIDTH-1:0] if_paddr;
logic                  if_penable;
logic                  if_psel;
logic                  if_pwrite;
logic [DATA_WIDTH-1:0] if_pwdata;
logic [DATA_WIDTH-1:0] if_prdata;
logic                  if_pready;
logic                  if_pslverr;

//##################################
//         MODPORT
//##################################

modport master (
    output if_pclk,
    output if_prst_n,
    output if_paddr,
    output if_psel,
    output if_penable,
    output if_pwrite,
    output if_pwdata,
    input  if_prdata,
    input  if_pready,
    input  if_pslverr
);

modport slave (
    input  if_pclk,
    input  if_prst_n,
    input  if_paddr,
    input  if_psel,
    input  if_penable,
    input  if_pwrite,
    input  if_pwdata,
    output if_prdata,
    output if_pready,
    output if_pslverr
);

endinterface