`timescale 1ns/1ps


module sum (
    input  logic       i_clk,
    input  logic       i_rst_n,
    input  logic [1:0] i_sw,
    output logic [1:0] o_led
);


////////////////////////////////////////
//                signals
////////////////////////////////////////

logic [1:0] r_sync [0:1];
logic [1:0] w_data;

////////////////////////////////////////
//                sync
////////////////////////////////////////

always_ff @(posedge i_clk or negedge i_rst_n)
begin
    if(i_rst_n == 1'b0) begin
        r_sync[0] <= 'b0;
        r_sync[1] <= 'b0;
    end else begin
        r_sync[0] <= i_sw;
        r_sync[1] <= r_sync[0];
    end
end

logic new_clock;
logic not_reset;

assign not_reset = ~i_rst_n; 

`ifdef ALTERA_PLL
pll pll_inst (
        .refclk   ( i_clk     ), 
        .locked   (           ), 
        .rst      ( not_reset ), 
        .outclk_0 ( new_clock )  
    );
`elsif XILINX_PLL
this_pll pll_inst (
        .clk_in1  ( i_clk     ), 
        .locked   (           ), 
        .reset    ( not_reset ), 
        .clk_out1 ( new_clock )  
    );
`else
    assign new_clock = i_clk;
`endif

////////////////////////////////////////
//                instantiation
////////////////////////////////////////

    switch_driver sw (
            .i_clk   (new_clock),
            .i_rst_n (i_rst_n),
            .i_data  (r_sync[1]),
            .o_data  (w_data)
    );

////////////////////////////////////////
//                outputs
////////////////////////////////////////

assign o_led = w_data;

endmodule
