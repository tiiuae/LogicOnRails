package framegen_pkg;
    `include "tb_defs.svh"
    import fieldgen_pkg::*;

    class FrameGen;

        FieldGen ag_fieldGen;
        byte a_frame_arg [][];
        byte a_frame_data [][];

        //##################################
        //         CONSTRUCTOR
        //##################################

        function new(
            input byte this_arr [][]
        );
            a_frame_arg = this_arr;
            ag_fieldGen = new();
        endfunction


        //##################################
        //         PRINT
        //##################################

        function void print_arr_arg ();
            for (int i =0; i < $size(this.a_frame_arg); i++) begin
                $display("SIZE %s%d%s: %s%d%s", `GREEN_C, $size(this.a_frame_arg), `NO_C,`YELLOW_C, $size(this.a_frame_arg[i]), `NO_C );
            end
        endfunction

        function void print_arr_data (
            input int threshold
        );
            for (int i = 0; i < $size(this.a_frame_data); i++) begin
                $write("\nfield %0d\n", i);
                for (int j = 0; j < $size(this.a_frame_data[i]); j++) begin
                    if ((j % threshold) == 0) begin
                        $write("\n");
                    end
                    $write("%02h ", this.a_frame_data[i][j]);
                end
            end    
            $write("\n");
        endfunction        

        function void print_frame ();
            $displayh("%p", this.a_frame_data);
        endfunction        

        function void print_stream ();
            $displayh("%p", {>>{this.a_frame_data}});
        endfunction        


        //##################################
        //         SIZE AUX FUNC
        //##################################

        function int get_field_n ();
            return $size(this.a_frame_data);
        endfunction

        function int get_field_size ();
            int acc = 0;
            for (int i = 0; i < get_field_n(); i++) begin
                acc += $size(this.a_frame_data[i]);
            end
            return acc;
        endfunction

        function int get_total_size_bits ();
            return get_field_size() * 8;
        endfunction                

        //##################################
        //         GENERATE
        //##################################

        function void frame_gen();
            int fields_size = $size(this.a_frame_arg);
            a_frame_data = new[fields_size];
            for (int i = 0; i < fields_size; i++) begin
                this.ag_fieldGen.set_arr_size(this.a_frame_arg[i][0]);
                this.ag_fieldGen.set_rnd(logic'(this.a_frame_arg[i][1]));
                this.ag_fieldGen.set_cons(this.a_frame_arg[i][2]);
                this.ag_fieldGen.set_min(this.a_frame_arg[i][3]);
                this.ag_fieldGen.set_max(this.a_frame_arg[i][4]);
                a_frame_data[i] = new[int'(this.a_frame_arg[i][0])];
                this.ag_fieldGen.array_gen();
                this.ag_fieldGen.get_arr_datagen(a_frame_data[i]);
            end               
        endfunction


    endclass

endpackage
