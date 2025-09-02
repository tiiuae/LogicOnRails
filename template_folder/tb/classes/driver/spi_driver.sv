
package spi_driver_pkg;
    import generic_driver_pkg::*;

    class SPIDriver extends GenericDriver #(
        .BUS_WIDTH ( 8 )
    );

        //##################################
        //         VARIABLE DECLARATION
        //##################################
        
        virtual interface SPI_iface viface;
        int sclk_period;
        logic [7:0] dout [];
    
        //##################################
        //         CONSTRUCTOR
        //##################################
    
        function new(
            virtual interface SPI_iface iface,
            input int this_period,
            input byte this_arr [][],
            input int this_frm_meta [0:1][]
        );
            super.new(this_arr, this_frm_meta);
            viface      = iface;
            sclk_period = this_period;
        endfunction

        //##################################
        //         SET GET
        //##################################

        function set_period (
            input int this_period
        );
            sclk_period = this_period;
        endfunction

        //##################################
        //         RESET
        //##################################

        task automatic reset_iface (); 
            viface.if_sclk <= 1'b0;
            viface.if_sdi  <= 1'b0;
            viface.if_ss   <= 1'b1;
        endtask

        //##################################
        //         SS
        //##################################

        task automatic select (); 
            viface.if_ss <= 1'b0;
        endtask

        task automatic clear (); 
            viface.if_ss <= 1'b1;
        endtask

        //##################################
        //         DRIVE CLK
        //##################################

        task automatic  drive_trailing (); 
            viface.if_sclk <= 1'b0;
            #500ns;
        endtask       

        task automatic drive_leading (); 
            viface.if_sclk <= 1'b1;
            #500ns;
        endtask                     

        task automatic drive_clk (); 
            drive_trailing();
            drive_leading();
        endtask     

        //##################################
        //         DRIVE MISO MOSI
        //##################################


        task automatic set_bit (
            input logic bit_in,
            output logic bit_out        
        ); 
            viface.if_sdi <= bit_in;
            drive_trailing();
            bit_out = viface.if_sdo;
            drive_leading();
        endtask   

        task automatic set_byte (
            input logic [7:0] din,
            output logic [7:0] dout
        ); 
            for (int i = 0; i < 8; i++) begin
                set_bit(din[7-i], dout[7-i]);
            end 
        endtask

        task automatic drive (
            input logic [7:0] din,
            output logic [7:0] dout
        ); 
            select ();
            set_byte(din, dout);
            viface.if_sclk <= 1'b0;
            viface.if_sdi <= 1'b0;
            //#(sclk_period/2);
            clear (); 
        endtask

        //##################################
        //         BATCH
        //##################################

        task automatic drive_batch ();
            int size;
            size = a_tx.size();
            dout = new[size];
            for (int i = 0; i < size; i++) begin
                drive(a_tx[i], dout[i]);
            end
        endtask

    endclass
endpackage