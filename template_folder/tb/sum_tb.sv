`timescale 1ns/1ps

`ifndef DEFAULT_TEST;
`define DEFAULT_TEST "test";
`endif

module sum_tb ();


////////////////////////////////////////
//                signals
////////////////////////////////////////

localparam PERIOD = 10;

logic [1:0] r_sw;
logic [1:0] w_led;
logic i_clk;
logic i_rst_n; 
logic triger;
string test_name;

////////////////////////////////////////
//                init
////////////////////////////////////////

initial begin
    i_clk = 1'b0;
    forever
    #(PERIOD/2) i_clk = ~i_clk;
end

initial 
begin
    i_rst_n = 1'b0;
    #(PERIOD*4);
    i_rst_n = 1'b1;
end 

////////////////////////////////////////
//              driver
////////////////////////////////////////

always_ff @(posedge i_clk or negedge i_rst_n)
begin
    if(i_rst_n == 1'b0) begin
        r_sw <= 'b0;
        triger <= 1'b0;
    end else begin
        if(r_sw < 2'b11) begin
            r_sw <= r_sw + 2'b01;
        end else begin
            triger <= 1'b1;
        end
    end 
end 

initial
begin
    test_name = `DEFAULT_TEST;
    test_name = test_name.tolower();
    if (test_name == "test2") begin
        $display("Hello, This is test2");
    end else begin
        $display("Hello, This is test1");
    end
    while(~triger) begin
        
    end
    #5000
    $stop;
end 


////////////////////////////////////////
//                dut
////////////////////////////////////////

    sum dut (
            .i_clk   (i_clk),
            .i_rst_n (i_rst_n),
            .i_sw    (r_sw),
            .o_led   (w_led)
    );

////////////////////////////////////////
//                checker
////////////////////////////////////////

  //  check:   assert property (@(posedge i_clk) !$stable(r_sw) |-> ##3 (w_led == {1'b0,r_sw[1]} + {1'b0,r_sw[0]})) else $error("assertion failed - checker");


endmodule
