
package avalonst_driver_pkg;
    import generic_driver_pkg::*;

    class AvalonSTDriver  #(
        parameter BUS_WIDTH = 32
    ) extends GenericDriver #(
        .BUS_WIDTH ( BUS_WIDTH  )
    );

        //##################################
        //         VARIABLE DECLARATION
        //##################################
        
        virtual interface avalonST_iface #(
            .DATA_WIDTH(BUS_WIDTH)
        ) viface;
    
        //##################################
        //         CONSTRUCTOR
        //##################################
    
        function new(
            input virtual interface avalonST_iface #(
                .DATA_WIDTH(BUS_WIDTH) 
            ) this_iface,
            input byte this_arr [][],
            input int this_frm_meta [0:1][]
        );
            super.new(this_arr, this_frm_meta);
            viface = this_iface;
        endfunction

        //##################################
        //         DELAY
        //################################## 

        task automatic gen_delay ();
            if (ifg_rnd_en == 1'b1) begin
                generate_ifg();
            end
            for (int i = 0; i < ifg_n; i++) begin
                @(posedge viface.i_clk);
            end
        endtask: gen_delay

        //##################################
        //         TASK
        //################################## 

        task automatic  clear ();
            viface.if_vld   <= 1'b0;
            viface.if_data  <= 'b0;
            @(posedge viface.i_clk);
        endtask: clear

        task automatic  transmit (
            input logic [BUS_WIDTH-1:0]  data       ='1, 
            input logic                  confirm_tx = 1'b0,
            input logic                  reset      = 1'b0
        );
            viface.if_vld   <= '1; 
            viface.if_data  <= data;
            @(posedge viface.i_clk);
            while((viface.if_rdy & viface.if_vld) == 1'b0) begin
                @(posedge viface.i_clk);
            end
            viface.if_vld <= 1'b0; 
        endtask: transmit

        task automatic  transmit_batch (
            input logic [BUS_WIDTH-1:0] a_tx[]
        );
            for (int i = 0; i < $size(a_tx); i++) begin
                transmit(a_tx[i], 1'b1, 1'b0);
            end 
            clear();
        endtask: transmit_batch  

        task automatic init_transfer();
            transmit_batch(a_tx);
        endtask: init_transfer;

        task automatic init_batch_transfer();
            for (int i =0; i < pkt_n; i++ ) begin
                transmit_batch(a_tx);
                gen_delay();
                fit_to_bus();
                ag_framegen.frame_gen();
            end
        endtask: init_batch_transfer;        

    endclass
endpackage