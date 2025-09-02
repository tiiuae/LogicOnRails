package generic_driver_pkg;
    `include "tb_defs.svh"
    import framegen_pkg::*;

    class GenericDriver #(
        parameter BUS_WIDTH = 32
    );
        localparam AUX_WIDTH = 65535; 

        FrameGen ag_framegen;
        logic [BUS_WIDTH-1:0] a_tx[];
        logic [AUX_WIDTH-1:0] aux_bitvector;

        int pkt_n;
        int pkt_rnd_en;
        int pkt_rng_max;
        int pkt_rng_min;
        int pkt_cons;

        int ifg_n;
        int ifg_rnd_en;
        int ifg_rng_max;
        int ifg_rng_min;
        int ifg_cons;        
        
        

        //##################################
        //         CONSTRUCTOR
        //##################################


        function new(
            input byte this_arr [][],
            input int this_frm_meta [0:1][]
        );
            this.ag_framegen = new(this_arr);
            this.ag_framegen.frame_gen();
            config_driver(this_frm_meta);
            fit_to_bus();
        endfunction

        //##################################
        //         PARSE PKT META
        //##################################

        function void config_driver(
            input int this_frm_meta [0:1][]
        );
            this.pkt_rnd_en  = this_frm_meta[0][0];
            this.pkt_cons    = this_frm_meta[0][1];
            this.pkt_rng_max = this_frm_meta[0][2];
            this.pkt_rng_min = this_frm_meta[0][3];
            this.ifg_rnd_en  = this_frm_meta[1][0];
            this.ifg_cons    = this_frm_meta[1][1]; 
            this.ifg_rng_max = this_frm_meta[1][2];
            this.ifg_rng_min = this_frm_meta[1][3];
            generate_pkt();
            generate_ifg();
        endfunction

        function void generate_pkt();
            if(pkt_rnd_en == 1'b1) begin
                this.pkt_n = $urandom_range(pkt_rng_max, pkt_rng_min);
            end else begin
                this.pkt_n = this.pkt_cons;
            end
        endfunction

        function void generate_ifg();
            if(ifg_rnd_en == 1'b1) begin
                this.ifg_n = $urandom_range(ifg_rng_max, ifg_rng_min);
            end else begin
                this.ifg_n = this.ifg_cons;
            end
        endfunction


        //##################################
        //         FIT
        //##################################
 
        function int calc_rst();
            int tx_bit_size = this.ag_framegen.get_total_size_bits();
            int tx_rst = (tx_bit_size % BUS_WIDTH) / 8;
            //$display("-> %d, %d, %d", tx_bit_size, BUS_WIDTH, (tx_bit_size % BUS_WIDTH));
            return tx_rst;
        endfunction

        function int calc_size();
            int bus_iter;
            int tx_bit_size = this.ag_framegen.get_total_size_bits();
            if ((tx_bit_size % BUS_WIDTH) == 0) begin 
                bus_iter = tx_bit_size / BUS_WIDTH;
            end else begin
                bus_iter = (tx_bit_size / BUS_WIDTH) + 1;
            end 
            return bus_iter;
        endfunction

        function void gen_tx_array(
            input int tx_iter
        );
            a_tx = new[tx_iter];
            //this.ag_framegen.print_arr_data(BUS_WIDTH);
            aux_bitvector = AUX_WIDTH'({>>{this.ag_framegen.a_frame_data}}); //quick fix, I don't know why it needs <<1            
            for (int i = 0; i < tx_iter; i++) begin
                a_tx[i] = aux_bitvector[AUX_WIDTH - (i * BUS_WIDTH) - 1 -: BUS_WIDTH];
                //$display("Slice %d: %h", i, a_tx[i]);
            end
        endfunction        

        function void fit_to_bus();
            int bus_iter = calc_size();
            this.gen_tx_array(bus_iter);
        endfunction

    endclass

endpackage
