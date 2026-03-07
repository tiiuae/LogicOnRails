package hdmi_rx_driver_pkg;
    import axist_driver_pkg::*;
    import generic_driver_pkg::*;
    import logger_pkg::*;
   `include "tb_defs.svh"

    class HDMIRXDriver  #(
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

        task automatic rst_source ();
            ag_axist_drvr.rst_source();        
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
    //                           HDMI RX  
    //
    // =============================================================================

        task automatic rx_send_line (
            input logic sof = 1'b0
        );
            for (int i = 0; i < x_resolution/pxlperclock; i++) begin
                logic tlast = (i >= x_resolution/pxlperclock-1);
                logic tuser = (sof == 1'b1 && i == 0);
                ag_axist_drvr.transmit(ag_axist_drvr.a_tx[0], tlast, 1'b0, tuser);
                ag_axist_drvr.rst_iface();
                ag_axist_drvr.gen_delay();
                ag_axist_drvr.fit_to_bus();
                ag_axist_drvr.ag_framegen.frame_gen();
            end
        endtask

        task automatic rx_send_frame (
            input int line_delay = 5
        );
            for (int i = 0; i < y_resolution; i++) begin
                logic sof = (i == 0);
                rx_send_line(sof);
                gen_delay(line_delay);
                ag_axist_drvr.fit_to_bus();
            end
        endtask        

        task automatic rx_send_video (
            input int frame_n,
            input int frm_delay = 5,
            input int line_delay = 5
        );
            for (int i = 0; i < frame_n; i++) begin
                rx_send_frame(frm_delay);
                for (int j =0; j < line_delay; j++) begin
                    gen_delay(6667);
                end 
            end
        endtask      

 
        

    endclass
endpackage