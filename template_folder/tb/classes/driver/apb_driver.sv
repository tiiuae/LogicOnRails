
package apb_driver_pkg;
    import generic_driver_pkg::*;

    class APBDriver  #(
        parameter ADDR_WIDTH = 32,
        parameter DATA_WIDTH = 32
    ) extends GenericDriver #(
        .BUS_WIDTH ( DATA_WIDTH  )
    );

        //##################################
        //         VARIABLE DECLARATION
        //##################################
        
        virtual interface APB_iface #(
            .DATA_WIDTH(DATA_WIDTH),
            .ADDR_WIDTH(ADDR_WIDTH)
        ) viface; 

        logic                  addrrnd;
        int                    addr_rng_min;
        int                    addr_rng_max;
        logic [DATA_WIDTH-1:0] reply;
   
        event e_pkt_rx;
        event e_pkt_tx;
        event e_pkt_err;

        //##################################
        //         CONSTRUCTOR
        //##################################

        function new(
            input virtual interface APB_iface #(
                .ADDR_WIDTH(ADDR_WIDTH),
                .DATA_WIDTH(DATA_WIDTH)
            ) this_viface,
            input byte this_arr [][],
            input int this_frm_meta [0:1][],
            input logic this_addrrnd,
            input int this_addr_rng_min,
            input int this_addr_rng_max
        );
            super.new(this_arr, this_frm_meta);
            viface = this_viface;
            addrrnd = this_addrrnd;
            addr_rng_min = this_addr_rng_min;
            addr_rng_max = this_addr_rng_max;
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
        //         INIT DESIGN
        //################################## 

        task clear();
            viface.if_psel    <= 1'b0;
            viface.if_penable <= 1'b0;
            viface.if_pwrite  <= 1'b0;
            viface.if_paddr   <= '0;
            viface.if_pwdata  <= '0;
            @(posedge viface.i_clk);
        endtask

        task wait_rst();
            clear();
            wait (viface.i_rst_n === 1'b1);
            @(posedge viface.i_clk);
        endtask

        //##################################
        //         ADDR HANDLE
        //################################## 
 
        function automatic logic [ADDR_WIDTH-1:0] handle_addr(
            input logic [ADDR_WIDTH-1:0] addr,
            input logic [ADDR_WIDTH-1:0] offset
        );
            if (this.addrrnd == 1'b1) begin
                return ADDR_WIDTH'($urandom_range( this.addr_rng_min, this.addr_rng_max));
            end else begin
                return addr + offset;
            end 
        endfunction


        //##################################
        //         SETUP
        //################################## 

        task automatic  setup_phase (
            input logic [BUS_WIDTH-1:0] data = '1, 
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic                 wren = 1'b0
        );
            viface.if_psel    <= 1'b1;
            viface.if_pwrite  <= wren;
            viface.if_paddr   <= addr;
            viface.if_pwdata  <= data;
            @(posedge viface.i_clk);
        endtask  


        //##################################
        //         WRITE ACTION
        //################################## 

        task automatic access_phase ();
            viface.if_penable  <= 1'b1;
            @(posedge viface.i_clk);
            while(viface.if_pready !== 1'b1) begin
                @(posedge viface.i_clk);
            end
            reply = viface.if_prdata;
        endtask  

        //##################################
        //         READ ACTION
        //##################################



        //##################################
        //      EXECUTE BATCH
        //################################## 

        task automatic  transmit_batch (
            input logic [BUS_WIDTH-1:0] a_tx[],
            input logic[ADDR_WIDTH-1:0] addr = '0
        );
            for (int i = 0; i < $size(a_tx); i++) begin
                setup_phase(a_tx[i], addr, 1'b1);
                access_phase();
            end 
            clear();
            ->> e_pkt_tx;
        endtask

        task automatic  receive_batch (
            input logic[ADDR_WIDTH-1:0] addr = '0
        );
            setup_phase('0, addr, 1'b0);
            access_phase();
            clear();
            ->> e_pkt_rx;
        endtask 


        //##################################
        //      BATCH CALL
        //################################## 

        task automatic drive_tx (
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic[ADDR_WIDTH-1:0] offset = '0
        );
            logic[ADDR_WIDTH-1:0] init_addr = addr;            
            for (int i = 0; i < pkt_n; i++ ) begin
                init_addr = handle_addr(init_addr, offset);
                transmit_batch(a_tx, addr);
                gen_delay();
                fit_to_bus();
                ag_framegen.frame_gen();
            end
        endtask
        

        //##################################
        //      ASYNC CALL
        //################################## 

        task automatic drive_batch_async (
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic[ADDR_WIDTH-1:0] offset = '0
        );
            fork
                drive_tx(addr, offset);
            join_none
        endtask        

    endclass
endpackage

