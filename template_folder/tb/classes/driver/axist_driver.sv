
package axist_driver_pkg;
    import generic_driver_pkg::*;

    class AXISTDriver  #(
        parameter DATA_WIDTH = 32,
        parameter USER_WIDTH = 16
    ) extends GenericDriver #(
        .BUS_WIDTH ( DATA_WIDTH  )
    );

        //##################################
        //         VARIABLE DECLARATION
        //##################################
        
        virtual interface AXI_ST_iface #(
            .DATA_WIDTH(DATA_WIDTH),
            .USER_WIDTH(USER_WIDTH)
        ) viface;

        logic [DATA_WIDTH-1:0] int_tdata;
        logic [USER_WIDTH-1:0] int_tuser;
        logic                  int_tlast;
    
        //##################################
        //         CONSTRUCTOR
        //##################################
    
        function new(
            input virtual interface AXI_ST_iface #(
                .DATA_WIDTH(DATA_WIDTH),
                .USER_WIDTH(USER_WIDTH)
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


        function automatic logic [(DATA_WIDTH/8)-1:0] reverse_groups (
            input logic [(DATA_WIDTH/8)-1:0] in
        ); 
            logic [(DATA_WIDTH/8)-1:0] out;
            for (int i = 0; i < (DATA_WIDTH/8); i ++) begin
                out[i] = in[(DATA_WIDTH/8)-1-i]; 
            end 
            return out;
        endfunction

        //##################################
        //         TASK RX
        //################################## 

        task automatic  rst_sink ();
            viface.if_tready <= 1'b0;
            @(posedge viface.i_clk);
        endtask: rst_sink


        task automatic raise_tready ();
            viface.if_tready <= 1'b1;
            @(posedge viface.i_clk);
        endtask

        task automatic clear_tready ();
            viface.if_tready <= 1'b0;
            @(posedge viface.i_clk);
        endtask

        task automatic wait_sink ();
            if (viface.if_tready == 1'b0) begin
                viface.if_tready = 1'b1;
            end
            @(posedge viface.i_clk iff (viface.if_tvalid && viface.if_tready));
            int_tdata = viface.if_tdata;
            int_tuser = viface.if_tuser;
            int_tlast = viface.if_tlast;        
        endtask

        task automatic one_sink ();
            raise_tready();
            @(posedge viface.i_clk iff (viface.if_tvalid && viface.if_tready));
            int_tdata = viface.if_tdata;
            int_tuser = viface.if_tuser;
            int_tlast = viface.if_tlast;   
            rst_sink();    
        endtask


        //##################################
        //         TASK TX
        //################################## 

        task automatic rst_source ();
            rst_iface();        
        endtask: rst_source


        task automatic  rst_iface ();
            viface.if_tvalid <= 1'b0;
            viface.if_tdata <= 'b0;
            viface.if_tkeep <= 'b0;
            viface.if_tlast <= 1'b0;
            viface.if_tuser <= '0;      
            @(posedge viface.i_clk);
        endtask: rst_iface

        task automatic  transmit (
            input logic [BUS_WIDTH-1:0]  data       = '1, 
            input logic                  last       = 1'b0,
            input logic                  reset      = 1'b0, 
            input logic [USER_WIDTH-1:0] tuser      = '0

        );
            int rst;
            viface.if_tvalid <= 1'b1; 
            if (last == 1'b1) begin
                rst = calc_rst();
                if (rst == 0) begin
                    viface.if_tkeep  <= '1;
                end else begin
                    viface.if_tkeep  <= reverse_groups((1 << (8 - rst)) - 1);
                end
            end else begin
                viface.if_tkeep  <= '1;
            end
            viface.if_tlast  <= last;
            viface.if_tdata  <= data;
            viface.if_tuser  <= tuser;
            @(posedge viface.i_clk);
            while((viface.if_tready & viface.if_tvalid) == 1'b0) begin
                @(posedge viface.i_clk);
            end
            viface.if_tvalid <= 1'b0; 
        endtask: transmit


        task automatic  transmit_batch (
            input logic [BUS_WIDTH-1:0]  a_tx[],
            input logic [USER_WIDTH-1:0] tuser = '0
        );

            $displayh("size of the loop %d", $size(a_tx));
            for (int i = 0; i < $size(a_tx); i++) begin
                logic last = (i == ($size(a_tx) -1));
                transmit(a_tx[i], last, 1'b0, tuser);
            end 
            rst_iface();
        endtask: transmit_batch  


        task automatic init_transfer();
            @(posedge viface.i_clk);
            transmit_batch(a_tx);
        endtask: init_transfer;


        task automatic init_batch_transfer();
            @(posedge viface.i_clk);
            for (int i =0; i < pkt_n; i++ ) begin
                transmit_batch(a_tx);
                gen_delay();
                fit_to_bus();
                ag_framegen.frame_gen();
            end
        endtask: init_batch_transfer;        

    endclass
endpackage