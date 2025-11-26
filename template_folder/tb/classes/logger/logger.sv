package logger_pkg;
    `include "tb_defs.svh"
    typedef enum bit [2:0] { 
        LOG_INF = 3'b000,
        LOG_WRN = 3'b001,
        LOG_CRT = 3'b010,
        LOG_ERR = 3'b011,
        LOG_DBG = 3'b100
    } t_msg_lvl;

    typedef enum bit [2:0] { 
        LOG_GREEN  = 3'b000,
        LOG_BLUE   = 3'b001,
        LOG_YELLOW = 3'b010,
        LOG_RED    = 3'b011,
        LOG_NOCLOR = 3'b100
    } t_msg_clr;    

    string COLOR_ARR [0:4] = '{
        `GREEN_C, `CYAN_C, `YELLOW_C, `RED_C, `NO_C
    };

    class Logger;
        string curr_msg;
        t_msg_lvl msg_lvl;
        bit color_en;

        //##################################
        //         CONSTRUCTOR
        //##################################

        function new(
            input t_msg_lvl this_msg_lvl, 
            input bit this_color_en=1'b0
        );
            this.msg_lvl  = this_msg_lvl;
            this.color_en = this_color_en;
            this.curr_msg = "";
        endfunction 

        //##################################
        //         AUX
        //################################## 

        //##################################
        //         TIME EXECUTION
        //##################################

        //##################################
        //         MESSAGE LEVEL
        //##################################

        function logic check_lvl (
            input t_msg_lvl msg_lvl
        );
            return ( msg_lvl >= this.msg_lvl );
        endfunction 

        function string gen_color (
            input string txt,
            input t_msg_clr clr
        ); 
            return $sformatf("%s%s%s:", COLOR_ARR[int'(clr)], txt, COLOR_ARR[int'(LOG_NOCLOR)]);
        endfunction

        function string gen_timestamp (
            input bit timestamp_en,
            input bit color_en
        ); 
            string str;
            if (timestamp_en == 1'b1) begin
                str = $sformatf("time [%0f]", $realtime);
                return (color_en == 1'b1)? gen_color(str, LOG_BLUE) : str; 
            end else begin
                return "";
            end
        endfunction


        //##################################
        //         LOGGER CONTROLLER
        //##################################

        function void log(
            input string str, 
            input t_msg_lvl msg_lvl=this.msg_lvl,
            input bit timestamp_en=1'b1,
            input bit color_en=this.color_en
        );
            if (check_lvl(msg_lvl)) begin
                this.curr_msg = "";
                this.curr_msg = (color_en == 1'b1)? gen_color(msg_lvl.name(), t_msg_clr'(msg_lvl)) : "";
                this.curr_msg = $sformatf("%s%s", this.curr_msg, gen_timestamp(timestamp_en, color_en));
                this.curr_msg = $sformatf("%s%s", this.curr_msg, str);
                $display(this.curr_msg);            
            end 
        endfunction 
    
        function log2file (
            input string filename, 
            input string str, 
            input t_msg_lvl msg_lvl=this.msg_lvl,
            input bit timestamp_en=1'b1,
            input bit color_en=this.color_en
        );
            integer file;
            file = $fopen(filename, "a");
            if (file == 0) begin
                $display("Error: Could not open file.");
            end else begin
                log(str, msg_lvl, timestamp_en, color_en);
                $fwrite(file, "%s", this.curr_msg);
                $fclose(file);
            end             
        endfunction 

    endclass    
endpackage
