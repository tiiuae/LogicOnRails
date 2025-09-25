
package axi4_driver_pkg;
    import generic_driver_pkg::*;

    class AXI4Driver  #(
        parameter DATA_WIDTH = 32,
        parameter ADDR_WIDTH = 32,
        parameter RX_MEM_DEPTH = 1024,
        type      VIF 
    ) extends GenericDriver #(
        .BUS_WIDTH ( DATA_WIDTH  )
    );

        //##################################
        //         VARIABLE DECLARATION
        //##################################
        
        VIF viface;
   
        //##################################
        //         CONSTRUCTOR
        //##################################

        logic [7:0] arburst; //type of burst
        logic [7:0] arlen; // beats n
        logic [2:0] arprot; //usr defined

        logic addrrnd;
        int addr_rng_min;
        int addr_rng_max;

        event e_pkt_rx;
        event e_pkt_tx;
        event e_pkt_err;

        logic [DATA_WIDTH-1:0] a_rxmem [$:RX_MEM_DEPTH-1];

        function new(
            input VIF this_viface,
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
            ag_framegen.print_stream();
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

        task clear(
            input logic keep_id = 1'b0
        );
            viface.if_awburst <= '0; 
            viface.if_awvalid <= 1'b0; 
            viface.if_awsize  <= '0;
            viface.if_awlen   <= '0;  
            viface.if_awaddr  <= '0;  
            viface.if_awprot  <= '0;  
            viface.if_awburst <= '0;

            viface.if_wdata <= '0;
            viface.if_wstrb <= '0;
            viface.if_wlast <= '0;
            viface.if_wvalid <= 1'b0;

            viface.if_bready <= 1'b0;

            viface.if_arburst <= '0; 
            viface.if_arvalid <= 1'b0; 
            viface.if_arsize  <= '0;
            viface.if_arlen   <= '0;  
            viface.if_araddr  <= '0;  
            viface.if_arprot  <= '0;  
            viface.if_arburst <= '0; 

            viface.if_rready <= 1'b0;

            if (keep_id == 1'b0) begin
                viface.if_arid    <= '0; 
                viface.if_awid    <= '0;  
            end
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
            input logic [1:0]            awburst,
            input logic [7:0]            awlen
        );
            if (this.addrrnd == 1'b1) begin
                return ADDR_WIDTH'($urandom_range( this.addr_rng_min, this.addr_rng_max));
            end else if (awburst == 2'b00) begin
                return addr;
            end else if (awburst == 2'b01) begin
                return addr + (awlen * viface.if_awsize);
            end else begin
                return '0;
            end
        endfunction


        //##################################
        //         WRITE ACTION
        //################################## 

        task automatic rsp_phase ();
            viface.if_bready <= 1'b1;
            do begin
                @(posedge viface.i_clk);
            end while (!viface.if_bvalid);
            viface.if_bready <= 1'b0;
        endtask

        task automatic  write_phase (
            input logic [DATA_WIDTH-1:0]  data  = '1,
            input logic last
        );
            int rst;
            $display("BBBBBBBBBB => %h", data);
            viface.if_wvalid <= 1'b1; 
            if (last == 1'b1) begin
                rst = calc_rst();
                if (rst == 0) begin
                    viface.if_wstrb  <= '1;
                end else begin
                    viface.if_wstrb  <= reverse_groups((1 << (8 - rst)) - 1);
                end
            end else begin
                viface.if_wstrb  <= '1;
            end
            viface.if_wlast  <= last;
            viface.if_wdata  <= data;
            @(posedge viface.i_clk);
            while((viface.if_wready & viface.if_wvalid) == 1'b0) begin
                @(posedge viface.i_clk);
            end
            viface.if_wvalid <= 1'b0; 
        endtask

        task automatic wraddr_phase (
            input logic [ADDR_WIDTH-1:0] addr,
            input logic [1:0]            awburst, 
            input logic [7:0]            awlen,
            input logic [2:0]            awprot
        );
            viface.if_awvalid <= 1'b1;
            viface.if_awsize <= $clog2(ADDR_WIDTH);
            viface.if_awburst <= awburst;
            viface.if_awprot  <= awprot;            
            viface.if_awlen   <= awlen;
            viface.if_awaddr  <= addr;
            do begin
                @(posedge viface.i_clk);
            end while (!viface.if_awready);
            viface.if_awvalid <= 1'b0;
        endtask


        //##################################
        //         READ ACTION
        //##################################


        task automatic read_phase ();
            viface.if_rready <= 1'b1;
            do begin
                @(posedge viface.i_clk);
            end while (viface.if_rvalid == 1'b0);
            if(viface.if_rresp < 2'b10) begin
                a_rxmem.push_front(viface.if_rdata);
                $display("received %h", viface.if_rdata);
            end else begin
                $display("error when reading addr %h", viface.if_araddr);
                ->> e_pkt_err;
            end
            viface.if_rready <= 1'b0;
        endtask

        task automatic rdaddr_phase (
            input logic [ADDR_WIDTH-1:0] addr,
            input logic [1:0]            arburst, 
            input logic [7:0]            arlen,
            input logic [2:0]            arprot
        );
            viface.if_arvalid <= 1'b1;
            viface.if_arsize <= $clog2(ADDR_WIDTH);
            viface.if_arburst <= arburst;
            viface.if_arprot  <= arprot;            
            viface.if_arlen   <= arlen;
            viface.if_araddr  <= addr;
            do begin
                @(posedge viface.i_clk);
            end while (!viface.if_arready);
            viface.if_arvalid <= 1'b0;
        endtask


        //##################################
        //      EXECUTE BATCH
        //################################## 

        task automatic  transmit_batch (
            input logic [BUS_WIDTH-1:0] a_tx[],
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic[ADDR_WIDTH-1:0] iter,
            input logic [1:0]           awburst, 
            input logic [7:0]           awlen,
            input logic [2:0]           awprot
        );
            int tx_pkt_len = $size(a_tx);
            int curr_burst = awlen+1;
            wraddr_phase(addr, awburst, awlen, awprot);
            @(posedge viface.i_clk);
            for (int j = 0; j < curr_burst; j ++) begin
                int idx = ((iter*awlen) + j) % tx_pkt_len;
                logic last = (j == awlen);
                $display("AAAAAAAA => %h", a_tx[idx]);
                write_phase(a_tx[idx], last);
                $display("CCCCC => %h", a_tx[idx]);
            end
            $display("DDDD =>",);
            clear(1'b1);
            rsp_phase ();
            viface.if_awid <= viface.if_awid+1;            
            ->> e_pkt_tx;
        endtask  

        task automatic  receive_batch (
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic [1:0]           arburst, 
            input logic [7:0]           arlen,
            input logic [2:0]           arprot
        );
            logic[ADDR_WIDTH-1:0] init_addr = addr;
            init_addr = handle_addr(init_addr, arburst, arlen);
            viface.if_arsize = $clog2(ADDR_WIDTH);
            rdaddr_phase(init_addr, arburst, arlen, arprot);
            for (int i = 0; i <= arlen; i ++) begin
                read_phase();
            end
            clear(1'b1);
            viface.if_arid <= viface.if_arid+1;            
            ->> e_pkt_rx;
        endtask 


        //##################################
        //      BATCH CALL
        //################################## 


        task automatic drive_tx (
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic [1:0]           awburst, 
            input logic [7:0]           awlen,
            input logic [2:0]           awprot
        );
            logic[ADDR_WIDTH-1:0] init_addr = addr;  
            for (int i =0; i < pkt_n; i++ ) begin
                int iter = (a_tx.size() > (awlen+1))? (a_tx.size() / (awlen+1)) : 1;
                for (int j = 0; j < iter; j++) begin
                    init_addr = handle_addr(init_addr, awburst, awlen);
                    transmit_batch(a_tx, addr, j, awburst, awlen, awprot);
                    gen_delay();
                end
                ag_framegen.frame_gen();
                fit_to_bus();
            end
        endtask


        task automatic drive_rx (
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic [1:0]           arburst, 
            input logic [7:0]           arlen,
            input logic [2:0]           arprot
        );
            for (int i =0; i < pkt_n; i++ ) begin
                receive_batch(addr, arburst, arlen, arprot);
                gen_delay();
            end
        endtask

        //##################################
        //      ASYNC CALL
        //################################## 


        task automatic drive_batch_async (
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic [1:0]           awburst, 
            input logic [7:0]           awlen,
            input logic [2:0]           awprot
        );
            fork
                drive_tx(addr, awburst, awlen, awprot);
            join_none
        endtask        

        task automatic fetch_batch_async (
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic [1:0]           arburst, 
            input logic [7:0]           arlen,
            input logic [2:0]           arprot
        );
            fork
                drive_rx(addr, arburst, arlen, arprot);
            join_none
        endtask  
    endclass
endpackage
