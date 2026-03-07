package hdmi_driver_pkg;
    import hdmi_rx_driver_pkg::*;
    import hdmi_tx_driver_pkg::*;
    import logger_pkg::*;
   `include "tb_defs.svh"

    class HDMIDriver  #(
        parameter DATA_WIDTH = 32,
        parameter USER_WIDTH = 16
    );   
    
    // =============================================================================
    //                           INTERFACES  
    //
    // =============================================================================
        
        HDMIRXDriver #(
            .DATA_WIDTH ( DATA_WIDTH  ),
            .USER_WIDTH ( USER_WIDTH  )
        ) ag_hdmi_rx_drvr;

        HDMITXDriver #(
            .DATA_WIDTH ( DATA_WIDTH  ),
            .USER_WIDTH ( USER_WIDTH  )
        ) ag_hdmi_tx_drvr;

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
            ) axist_vif_tx,

            input byte frm_tx [][],
            input int  meta_tx [0:1][],

            input virtual interface AXI_ST_iface #(
                .DATA_WIDTH( DATA_WIDTH  ),
                .USER_WIDTH( USER_WIDTH  )        
            ) axist_vif_rx,

            input byte frm_rx [][],
            input int  meta_rx [0:1][],

            input int this_x_resolution,
            input int this_y_resolution,
            input int this_pxlperclock,
            input t_msg_lvl msg_lvl = LOG_INF 
        );
            ag_hdmi_rx_drvr = new(axist_vif_rx, frm_rx, meta_rx, this_x_resolution, this_y_resolution, this_pxlperclock);
            ag_hdmi_tx_drvr = new(axist_vif_tx, frm_tx, meta_tx, this_x_resolution, this_y_resolution, this_pxlperclock);
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

        task automatic rst_iface ();
            ag_hdmi_rx_drvr.rst_source();        
            ag_hdmi_tx_drvr.rst_sink();        
        endtask

    // =============================================================================
    //                           DELAY  
    //
    // =============================================================================


        task automatic gen_delay_rx (
            input int delay
        );
            for (int i = 0; i < delay; i++) begin
                @(posedge ag_hdmi_rx_drvr.ag_axist_drvr.viface.i_clk);
            end
        endtask: gen_delay_rx


        task automatic gen_delay_tx (
            input int delay
        );
            for (int i = 0; i < delay; i++) begin
                @(posedge ag_hdmi_tx_drvr.ag_axist_drvr.viface.i_clk);
            end
        endtask: gen_delay_tx


    // =============================================================================
    //                           HDMI  
    //
    // =============================================================================

        task automatic run_hdmi (
            input int frame_n,
            input int frm_delay = 5,
            input int line_delay = 5
        );
            fork
                ag_hdmi_rx_drvr.rx_send_video(frame_n, frm_delay, line_delay);
                ag_hdmi_tx_drvr.tx_compare();
            join
        endtask


    endclass
endpackage