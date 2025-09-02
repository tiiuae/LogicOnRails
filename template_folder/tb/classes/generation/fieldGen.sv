package fieldgen_pkg;

    `include "tb_defs.svh"

    class FieldGen;

        byte  array_s;
        byte  data_range_min;
        byte  data_range_max;
        byte  data_cons;        
        logic data_rnd;

        byte datagen;
        byte a_datagen []; 

        //##################################
        //         CONSTRUCTOR
        //##################################

        function new(
            input byte  this_array_s        = 0,         
            input logic this_data_rnd       = 1'b0,
            input byte  this_data_cons      = 0,
            input byte  this_data_range_min = 0,
            input byte  this_data_range_max = 1
        );
            array_s        = this_array_s;
            data_range_min = this_data_range_min;
            data_range_max = this_data_range_max;
            data_cons      = this_data_cons;
            data_rnd       = this_data_rnd;
        endfunction


        //##################################
        //         SET GET
        //##################################

        function byte get_datagen ();
            return datagen;
        endfunction   

        function void get_arr_datagen (
            output byte arr[]
        );
            arr =  this.a_datagen;
        endfunction   

        function void set_arr_size (
            input byte this_array_s      
        );
            this.array_s = this_array_s;
        endfunction    

        function void set_min (
            input byte this_data_range_min       
        );
            this.data_range_min = this_data_range_min;
        endfunction                                               

        function void set_max (
            input byte this_data_range_max         
        );
            this.data_range_max = this_data_range_max;
        endfunction  

        function void set_cons (
            input byte this_data_cons        
        );
            this.data_cons = this_data_cons;
        endfunction  

        function void set_rnd (
            input logic this_data_rnd       
        );
            this.data_rnd = this_data_rnd;
        endfunction                  

        //##################################
        //         GENERATE
        //##################################

        function void data_gen (
            input byte  this_data_range_min = this.data_range_min,
            input byte  this_data_range_max = this.data_range_max,
            input byte  this_data_cons      = this.data_cons,
            input logic this_data_rnd       = this.data_rnd
        );
            if (this_data_rnd == 1'b1) begin
                datagen = byte'($urandom_range( int'(this_data_range_min), int'(this_data_range_max)));
            end else begin
                datagen = this_data_cons;
            end
        endfunction 

        function void array_gen (
            input byte  this_array_s        = this.array_s,
            input byte  this_data_range_min = this.data_range_min,
            input byte  this_data_range_max = this.data_range_max,
            input byte  this_data_cons      = this.data_cons,
            input logic this_data_rnd       = this.data_rnd
        );
            this.arr_construct(this_array_s);
            for (int i =0; i < int'(this_array_s); i++) begin
                this.data_gen(this_data_range_min,this_data_range_max,this_data_cons,this_data_rnd);
                a_datagen[i] = this.get_datagen();
            end          
        endfunction         

        function void arr_construct (
            input byte this_array_s = this.array_s
        );
            a_datagen = new[int'(this_array_s)];
        endfunction 

    endclass

endpackage
