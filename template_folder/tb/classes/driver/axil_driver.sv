
package axil_driver_pkg;
    import generic_driver_pkg::*;

    class AXI_Lite_Driver  #(
        parameter DATA_WIDTH = 32,
        parameter ADDR_WIDTH = 32,
        parameter RX_MEM_DEPTH = 1024
    ) extends GenericDriver #(
        .BUS_WIDTH ( DATA_WIDTH  )
    );

        //##################################
        //         VARIABLE DECLARATION
        //##################################
        
        virtual interface AXI_Lite_iface #(
            .DATA_WIDTH(DATA_WIDTH),
            .ADDR_WIDTH(ADDR_WIDTH)
        ) viface;

        //##################################
        //         CONSTRUCTOR
        //##################################


        event e_pkt_rx;
        event e_pkt_tx;
        event e_pkt_err;

        logic [DATA_WIDTH-1:0] a_rxmem [$:RX_MEM_DEPTH-1];

        function new(
            input virtual interface AXI_Lite_iface #(
                .DATA_WIDTH(DATA_WIDTH),
                .ADDR_WIDTH(ADDR_WIDTH)
            ) this_iface,
            input byte this_arr [][],
            input int this_frm_meta [0:1][]
        );
            super.new(this_arr, this_frm_meta);
            viface = this_iface;
            if (viface.DATA_WIDTH != DATA_WIDTH) begin
                $display("error, width missmatch between class and interface");
            end
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
            viface.if_arvalid <= '0;
            viface.if_araddr  <= '0;
            viface.if_arprot  <= '0;
            viface.if_awaddr  <= '0;
            viface.if_awprot  <= '0;
            viface.if_awvalid <= '0;
            viface.if_rready  <= '0; 
            viface.if_wdata   <= '0;
            viface.if_wstrb   <= '0;
            viface.if_wvalid  <= '0;
            viface.if_bready  <= '0;
        endtask

        task wait_rst();
            clear();
            wait (viface.i_rst_n === 1'b1);
            @(posedge viface.i_clk);
        endtask



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
            input logic [DATA_WIDTH-1:0]  data  = '1
        );
            int rst;
            viface.if_wvalid <= 1'b1; 
            viface.if_wstrb  <= '1;
            viface.if_wdata  <= data;
            @(posedge viface.i_clk);
            while((viface.if_wready & viface.if_wvalid) == 1'b0) begin
                @(posedge viface.i_clk);
            end
            viface.if_wvalid <= 1'b0; 
        endtask

        task automatic wraddr_phase (
            input logic [ADDR_WIDTH-1:0] addr,
            input logic [2:0]            awprot
        );
            viface.if_awvalid <= 1'b1;
            viface.if_awprot  <= awprot;            
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
            input logic [2:0]            arprot
        );
            viface.if_arvalid <= 1'b1;
            viface.if_arprot  <= arprot;            
            viface.if_araddr  <= addr;
            do begin
                @(posedge viface.i_clk);
            end while (!viface.if_arready);
            viface.if_arvalid <= 1'b0;
        endtask


        //##################################
        //      EXECUTE BATCH
        //################################## 

        task automatic  transmit_one (
            input logic [DATA_WIDTH-1:0] data = '0,
            input logic [ADDR_WIDTH-1:0] addr = '0,
            input logic [2:0]            awprot
        );
            wraddr_phase(addr, awprot);
            @(posedge viface.i_clk);
            write_phase(data);
            clear();
            rsp_phase ();
            ->> e_pkt_tx;
        endtask  

        task automatic  transmit_batch (
            input logic [BUS_WIDTH-1:0] a_tx[],
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic [2:0]           awprot
        );
            int tx_pkt_len = $size(a_tx);
            wraddr_phase(addr, awprot);
            @(posedge viface.i_clk);
            write_phase(a_tx[0]);
            clear();
            rsp_phase ();
            ->> e_pkt_tx;
        endtask  

        task automatic  receive_one (
            input logic [ADDR_WIDTH-1:0] addr = '0,
            input logic [2:0]            arprot
        );
            rdaddr_phase(addr, arprot);
            read_phase();
            clear();
            ->> e_pkt_rx;
        endtask 


        task automatic  receive_batch (
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic [2:0]           arprot
        );
            rdaddr_phase(addr, arprot);
            read_phase();
            clear();
            ->> e_pkt_rx;
        endtask 


        //##################################
        //      BATCH CALL
        //################################## 
        
        task automatic drive_tx (
            input logic [DATA_WIDTH-1:0] data = '0,
            input logic [ADDR_WIDTH-1:0] addr = '0,
            input logic [2:0]            awprot
        );
            transmit_one(data, addr, awprot);
            gen_delay();
        endtask

        task automatic drive_batch (
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic [2:0]           awprot
        );
            for (int i =0; i < pkt_n; i++ ) begin
                transmit_batch(a_tx, addr, awprot);
                gen_delay();
                ag_framegen.frame_gen();
                fit_to_bus();
            end
        endtask

        task automatic drive_rx (
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic [2:0]           arprot
        );
            receive_one(addr, arprot);
            gen_delay();
        endtask


        task automatic read_batch (
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic [2:0]           arprot
        );
            for (int i =0; i < pkt_n; i++ ) begin
                receive_batch(addr, arprot);
                gen_delay();
            end
        endtask

        //##################################
        //      ASYNC CALL
        //################################## 


        task automatic drive_batch_async (
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic [2:0]           awprot
        );
            fork
                drive_batch(addr, awprot);
            join_none
        endtask        

        task automatic fetch_batch_async (
            input logic[ADDR_WIDTH-1:0] addr = '0,
            input logic [2:0]           arprot
        );
            fork
                read_batch(addr, arprot);
            join_none
        endtask  
    endclass
endpackage
