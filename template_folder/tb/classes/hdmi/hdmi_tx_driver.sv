package hdmi_tx_driver_pkg;
    import axist_driver_pkg::*;
    import generic_driver_pkg::*;
    import hdmi_pkg::*;
    import verif_pkg::*;
    import logger_pkg::*;
   `include "tb_defs.svh"

    class HDMITXDriver  #(
        parameter DATA_WIDTH = 32,
        parameter USER_WIDTH = 16
    );   
    
    // =============================================================================
    //                           INTERFACES  
    //
    // =============================================================================
        
        AXISTDriver #(
            .DATA_WIDTH( DATA_WIDTH ),
            .USER_WIDTH( USER_WIDTH )        
        ) ag_axist_drvr;

        Logger ag_logger;
        int    x_resolution;
        int    y_resolution;
        int    curr_x;
        int    curr_y;
        int    pxlperclock;
        logic  skip_column;
        logic  skip_line;

        mailbox #(st_hdmi_pxl) mb;


    // =============================================================================
    //                           CONSTRUCTOR  
    //
    // =============================================================================

        function new(
            input virtual interface AXI_ST_iface #(
                .DATA_WIDTH( DATA_WIDTH  ),
                .USER_WIDTH( USER_WIDTH  )        
            ) axist_vif,

            input byte frm [][],
            input int  meta [0:1][],
            input int this_x_resolution,
            input int this_y_resolution,
            input int this_pxlperclock,
            input logic this_skip_column,
            input logic this_skip_line,
            mailbox #(st_hdmi_pxl) this_mb,

            input t_msg_lvl msg_lvl = LOG_INF 
        );
            ag_axist_drvr = new(axist_vif, frm, meta);
            mb            = this_mb;
            skip_column   = this_skip_column;
            skip_line     = this_skip_line;
            `ifdef GUI
                ag_logger = new( msg_lvl, 1'b1);
            `else
                ag_logger = new( msg_lvl, 1'b0);
            `endif
            x_resolution = this_x_resolution;
            y_resolution = this_y_resolution;
            pxlperclock  = this_pxlperclock;
        endfunction

    // =============================================================================
    //                           RESETS  
    //
    // =============================================================================

        task automatic rst_sink ();
            ag_axist_drvr.rst_sink();        
        endtask

    // =============================================================================
    //                           DELAY  
    //
    // =============================================================================


        task automatic gen_delay (
            input int delay
        );
            for (int i = 0; i < delay; i++) begin
                @(posedge ag_axist_drvr.viface.i_clk);
            end
        endtask: gen_delay

    // =============================================================================
    //                             TRANSFORM  
    //
    // =============================================================================

    function automatic logic [DATA_WIDTH-1:0] hdmi_reduce(
        input logic [DATA_WIDTH-1:0] data,
        input logic                  sof,
        input logic                  eol
    );
        $display("%h, %b, %b", data, sof, eol);
        for (int i = 0; i < DATA_WIDTH; i++) begin
            if ((i % 8) == '0 || (i % 8) == 1) begin
                if (i == PXL_SOF_POS) begin
                    hdmi_reduce[i] = sof;
                end else if (i == PXL_SOF_POS+1) begin
                    hdmi_reduce[i] = sof;
                end else if (i == PXL_EOL_POS) begin
                    hdmi_reduce[i] = eol;
                end else if (i == PXL_EOL_POS+1) begin
                    hdmi_reduce[i] = eol;
                end else if (i == PXL_VLD_POS) begin
                    hdmi_reduce[i] = 1'b1;
                end else if (i == PXL_VLD_POS+1) begin
                    hdmi_reduce[i] = 1'b1;
                end else begin
                    hdmi_reduce[i] = 1'b0;
                end
            end else begin
                hdmi_reduce[i] = data[i];
            end    
        end   
        return hdmi_reduce;
    endfunction


    // =============================================================================
    //                           HDMI TX  
    //
    // =============================================================================

        function automatic inc_pxl(
            input logic                  sof,
            input logic                  eol
        );
            if (sof == 1) begin
                curr_x = 0;
                curr_y = 0;
            end else if (curr_x >= x_resolution) begin
                ag_logger.log(`log(("ERROR: extra columns, current column %d", curr_x)), LOG_WRN);
                //$stop;
            end else if (eol == 1'b1) begin
                curr_x = 0;
                if (curr_y >= y_resolution) begin
                    ag_logger.log(`log(("ERROR: extra lines, current line %d", curr_y)), LOG_WRN);
                    //$stop;
                end else begin
                    curr_y++;
                end
            end else begin
                curr_x++;
            end 
        endfunction

        task automatic compare_val ();
            st_hdmi_pxl st_pxl; 
            mb.get(st_pxl);
            st_pxl.data = hdmi_reduce(st_pxl.data, st_pxl.sof, st_pxl.eol);
            if ( st_pxl.data != ag_axist_drvr.int_tdata )begin
                ag_logger.log(`log(("ERROR: Different TDATA")), LOG_WRN);
                ag_logger.log(`log(("transmitted %h received %h", st_pxl.data, ag_axist_drvr.int_tdata)), LOG_WRN);
                //$stop;
            end 
            if ( st_pxl.sof  != ag_axist_drvr.int_tuser )begin
                ag_logger.log(`log(("ERROR: Different TUSER")), LOG_WRN);
                ag_logger.log(`log(("transmitted %b received %b", st_pxl.sof, ag_axist_drvr.int_tuser)), LOG_WRN);
                //$stop;
            end
            if ( st_pxl.eol  != ag_axist_drvr.int_tlast )begin
                ag_logger.log(`log(("ERROR: Different TLAST")), LOG_WRN);
                ag_logger.log(`log(("transmitted %b received %b", st_pxl.eol, ag_axist_drvr.int_tlast)), LOG_WRN);
                //$stop;
            end
        endtask

        task automatic rec_compare (
            input logic single_comp
        );
            ag_axist_drvr.wait_sink();
            inc_pxl(ag_axist_drvr.viface.if_tuser, ag_axist_drvr.viface.if_tlast);
            if (!(skip_column && (curr_x % 2 == 1))) begin
                if (!(skip_line & (curr_y % 2 == 1))) begin
                    compare_val();
                end
            end
            if (single_comp == 1'b1) begin
                ag_axist_drvr.rst_sink();
            end 
        endtask

        task automatic tx_compare (
            int threshold,
            int delay
        );
            curr_x = 0;
            curr_y = 0;
            while(1'b1) begin
                ag_logger.log(`log(("initial receiver behaviour - always on")), LOG_INF);
                for (int i = 0; i < threshold; i++) begin
                    rec_compare(1'b0);
                end 
                ag_logger.log(`log(("change receiver behaviour - %d delay", delay)), LOG_INF);
                ag_axist_drvr.rst_sink();
                while (1'b1) begin
                    gen_delay(delay);
                    rec_compare(1'b1);
                end
            end
        endtask


    endclass
endpackage