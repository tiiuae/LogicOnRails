import axi4_driver_pkg::*;
import logger_pkg::*;

module ext_mem_tb ();

// =============================================================================
//                           SIGNALS
//
// =============================================================================
`define log(ARG) $sformatf ARG
localparam AXI_DATA_WIDTH = 32;
localparam AXI_ADDR_WIDTH = 32;

byte ethernet_frm [][] = '{ 
    '{ 8, 1,  85, 0, 255 }
};
int frm_meta [0:1][] = '{
    '{ 0,  4, 1, 3 },
    '{ 0,  2, 1, 3 }    
};
logic w_clk;
logic w_rst_n;

AXI4_iface #(
    .DATA_WIDTH( AXI_DATA_WIDTH ),
    .ADDR_WIDTH( AXI_ADDR_WIDTH )
) if_axi4 (
    .i_clk   ( w_clk   ),
    .i_rst_n ( w_rst_n )
);
Logger ag_logger;



AXI4Driver #(
    .DATA_WIDTH( AXI_DATA_WIDTH ),
    .ADDR_WIDTH( AXI_ADDR_WIDTH )
) ag_axi4_drvr;





// =============================================================================
//                           CLOCK
//
// =============================================================================

localparam PERIOD = 10;

initial begin
    w_clk = 1'b0;
    forever
    #(PERIOD/2) w_clk = ~w_clk;
end

initial 
begin
    w_rst_n = 1'b0;
    #(PERIOD*6);
    w_rst_n = 1'b1;
end 


// =============================================================================
//                           DRIVER
//
// =============================================================================

localparam PROT     = 0;
localparam ADDR     = 1;
localparam BURST    = 1;
localparam LEN      = 1;
localparam NO_COLOR = 0;

initial
begin
    ag_logger    = new(`MESSAGE_LEVEL, NO_COLOR);
    ag_axi4_drvr = new(if_axi4, ethernet_frm, frm_meta, 1'b0, 0 ,255);        
    ag_logger.log(`log(("initial run")), LOG_INF);
    ag_axi4_drvr.wait_rst();
    wait (w_rst_n == 1'b1);

    ag_logger.log(`log(("write: addr %02h burst %02h len %02h prot %02h", ADDR, BURST, LEN, PROT)), LOG_INF);
    ag_axi4_drvr.drive_tx(ADDR, BURST, LEN, PROT);
    #200;
    ag_axi4_drvr.drive_rx(ADDR, BURST, LEN, PROT);
    #200;
    $stop;    
end 


// =============================================================================
//                           DUT
//
// =============================================================================

ext_mem inst_ext_mem(
    .i_clk      ( w_clk   ),
    .if_axi_mem ( if_axi4 )
);

endmodule