package mss_driver_pkg;
    import mss_cnf_pkg::*;
    import axi_pkg::*;
    import apb_driver_pkg::*;
    import axi4_driver_pkg::*;
    import generic_driver_pkg::*;
    import logger_pkg::*;
   `include "tb_defs.svh"
   `include "mss_cmd.svh"

    class MSSDriver;   
    
    // =============================================================================
    //                           INTERFACES  
    //
    // =============================================================================

        typedef virtual AXI4opt_iface #(
            .DATA_WIDTH ( FIC0_DATA_WIDTH ),
            .ADDR_WIDTH ( FIC0_ADDR_WIDTH ),
            .ID_WIDTH   ( FIC0_ID_WIDTH   ),
            .USER_WIDTH ( FIC0_USER_WIDTH )
        ) t_axi4_if;
        
        AXI4Driver #(
            .DATA_WIDTH( FIC0_DATA_WIDTH  ),
            .ADDR_WIDTH( FIC0_ADDR_WIDTH  ),
            .VIF       ( t_axi4_if        )
        ) ag_axi_fic0_drvr;

        AXI4Driver #(
            .DATA_WIDTH( FIC1_DATA_WIDTH  ),
            .ADDR_WIDTH( FIC1_ADDR_WIDTH  ),
            .VIF       ( t_axi4_if        )
        ) ag_axi_fic1_drvr;

        AXI4Driver #(
            .DATA_WIDTH( SDDR_ADDR_WIDTH  ),
            .ADDR_WIDTH( SDDR_DATA_WIDTH  ),
            .VIF       ( t_axi4_if        )
        ) ag_axi_fic2_drvr;

        APBDriver #(
            .DATA_WIDTH(FIC_APB_DATA_WIDTH),
            .ADDR_WIDTH(FIC_APB_ADDR_WIDTH)
        ) ag_apb_fic3_drvr;

        Logger ag_logger;

    // =============================================================================
    //                           CONSTRUCTOR  
    //
    // =============================================================================

        function new(
            input virtual interface APB_iface #(
                .ADDR_WIDTH(FIC_APB_DATA_WIDTH),
                .DATA_WIDTH(FIC_APB_ADDR_WIDTH)
            ) apb_vif,

            input virtual interface AXI4opt_iface #(
                .DATA_WIDTH ( FIC0_DATA_WIDTH ),
                .ADDR_WIDTH ( FIC0_ADDR_WIDTH ),
                .ID_WIDTH   ( FIC0_ID_WIDTH   ),
                .USER_WIDTH ( FIC0_USER_WIDTH )
            ) axi_vif0,

            input virtual interface AXI4opt_iface #(
                .DATA_WIDTH ( FIC1_DATA_WIDTH ),
                .ADDR_WIDTH ( FIC1_ADDR_WIDTH ),
                .ID_WIDTH   ( FIC1_ID_WIDTH   ),
                .USER_WIDTH ( FIC1_USER_WIDTH )
            ) axi_vif1,

            input virtual interface AXI4opt_iface #(
                .DATA_WIDTH ( SDDR_DATA_WIDTH ),
                .ADDR_WIDTH ( SDDR_ADDR_WIDTH ),
                .ID_WIDTH   ( SDDR_ID_WIDTH   ),
                .USER_WIDTH ( SDDR_USER_WIDTH )
            ) axi_vif2,

            input byte mss_frm [][],
            input int mss_meta [0:1][],
            input t_msg_lvl msg_lvl = LOG_INF 
        );
            ag_axi_fic0_drvr = new(axi_vif0, mss_frm, mss_meta, 1'b1, 0, 255);
            ag_axi_fic1_drvr = new(axi_vif1, mss_frm, mss_meta, 1'b1, 0, 255);
            ag_axi_fic2_drvr = new(axi_vif2, mss_frm, mss_meta, 1'b1, 0, 255);
            ag_apb_fic3_drvr = new(apb_vif,  mss_frm, mss_meta, 1'b1, 0, 255);
            `ifdef GUI
                ag_logger = new( msg_lvl, 1'b0);
            `else
                ag_logger = new( msg_lvl, 1'b1);
            `endif
        endfunction

    // =============================================================================
    //                           RESETS  
    //
    // =============================================================================

        task automatic mss_rst_iface ();
            ag_axi_fic0_drvr.wait_rst();        
            ag_axi_fic1_drvr.wait_rst();        
            ag_apb_fic3_drvr.wait_rst();        
        endtask


    // =============================================================================
    //                           FIC0  
    //
    // =============================================================================

        task automatic fic0_single_cmd (
           input int                         addr,
           input int                         data,
           input logic [FIC0_ADDR_WIDTH-1:0] iter,
           input logic [1:0]                 awburst, 
           input logic [7:0]                 awlen,
           input logic [2:0]                 awprot
        );
            if (addr < 32'h6000_0000 || addr > 32'h6FFF_FFFF) begin
                ag_logger.log(`log(("MSS: Warning: FIC0 addr %h is  out of bound, will be rejected in real hardware", addr)), LOG_CRT);
            end else begin
                ag_logger.log(`log(("MSS: Writes one cmd via fic0")), LOG_INF);
                ag_axi_fic0_drvr.transmit_batch( '{data} , addr,  iter, 1'b1, awburst, awlen, awprot);
            end
        endtask


    // =============================================================================
    //                           FIC1  
    //
    // =============================================================================

        task automatic fic1_single_cmd (
           input int                         addr,
           input int                         data,
           input logic [FIC1_ADDR_WIDTH-1:0] iter,
           input logic [1:0]                 awburst, 
           input logic [7:0]                 awlen,
           input logic [2:0]                 awprot
        );
            if (addr < 32'hE000_0000 || addr > 32'h6EFF_FFFF) begin
                ag_logger.log(`log(("MSS: Warning: FIC1 addr %h is  out of bound, will be rejected in real hardware", addr)), LOG_CRT);
            end else begin
                ag_logger.log(`log(("MSS: Writes one cmd via fic1")), LOG_INF);
                ag_axi_fic1_drvr.transmit_batch( '{data} , addr,  iter, 1'b1, awburst, awlen, awprot);
            end
        endtask

    // =============================================================================
    //                           FIC2 SDDR  
    //
    // =============================================================================



    // =============================================================================
    //                           FIC3  
    //
    // =============================================================================


        task automatic fic3_single_cmd (
            input int addr,
            input int data
        );
            if (addr < 32'h4000_0000 || addr > 32'h4FFF_FFFF) begin
                ag_logger.log(`log(("MSS: Warning: FIC3 addr %h is  out of bound, will be rejected in real hardware", addr)), LOG_CRT);
            end else begin
                ag_logger.log(`log(("MSS: Writes cmd %h to addr %h via fic3",addr, data)), LOG_INF);
                ag_apb_fic3_drvr.transmit_batch( '{data}, addr );
            end 
        endtask

        task automatic fic3_hist_cnf ();
            ag_logger.log(`log(("MSS: Writes histogram cmds via fic3")), LOG_INF);
            ag_apb_fic3_drvr.transmit_batch( '{`CMD_APB_IMG_DATA_COL      }, `CMD_APB_IMG_ADDR_COL      );
            ag_apb_fic3_drvr.transmit_batch( '{`CMD_APB_IMG_DATA_ROW      }, `CMD_APB_IMG_ADDR_ROW      );
            ag_apb_fic3_drvr.transmit_batch( '{`CMD_APB_IMG_DATA_BASEADDR }, `CMD_APB_IMG_ADDR_BASEADDR );
            ag_apb_fic3_drvr.transmit_batch( '{`CMD_APB_IMG_DATA_TRG      }, `CMD_APB_IMG_ADDR_TRG      );
        endtask        

        task automatic fic3_wac_cnf ();
            ag_logger.log(`log(("MSS: Writes wavc camera cmds via fic3")), LOG_INF);
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00001000 }, 32'h4002_1000 );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00001000 }, 32'h4002_1400 );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00000002 }, 32'h4002_0020 );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00000003 }, 32'h4002_1004 );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00000003 }, 32'h4002_1404 );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00000000 }, 32'h4002_1008 );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00000002 }, 32'h4002_1408 );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00000000 }, 32'h4002_100C );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00000000 }, 32'h4002_140C );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00000003 }, 32'h4002_0004 );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00000000 }, 32'h4002_1410 );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h0000FFFC }, 32'h4002_1414 );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h0000FFFC }, 32'h4002_1418 );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00000000 }, 32'h4002_141C );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h0000BFFC }, 32'h4002_1420 );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00000003 }, 32'h4002_0004 );
            ag_apb_fic3_drvr.transmit_batch( '{ 32'h00000011 }, 32'h4002_142C );
        endtask        

    endclass
endpackage