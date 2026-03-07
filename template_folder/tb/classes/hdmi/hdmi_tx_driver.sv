package hdmi_tx_driver_pkg;
    import axist_driver_pkg::*;
    import generic_driver_pkg::*;
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
        int x_resolution;
        int y_resolution;
        int pxlperclock;

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
            input t_msg_lvl msg_lvl = LOG_INF 
        );
            ag_axist_drvr = new(axist_vif, frm, meta);
            `ifdef GUI
                ag_logger = new( msg_lvl, 1'b0);
            `else
                ag_logger = new( msg_lvl, 1'b1);
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
    //                           HDMI TX  
    //
    // =============================================================================

        task automatic tx_compare ();
           ag_axist_drvr.wait_sink();
           $display("------> %h", ag_axist_drvr.int_tdata);  
        endtask


    endclass
endpackage