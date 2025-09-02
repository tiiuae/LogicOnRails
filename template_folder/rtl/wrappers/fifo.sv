`timescale 1 ps / 1 ps
module fifo 
#(
    parameter DATA_WIDTH = 48,
    parameter ADDR_WIDTH = 13,
    parameter A_FULL = 2,
    parameter A_EMPTY = 2
)(
    input  logic                         i_clk,
    input  logic                         i_rst_sync,
    input  logic                         i_trg_wr,
    input  logic                         i_trg_rd,
    input  logic [DATA_WIDTH-1:0]        i_data,
    output logic                         o_data_vld,
    output logic [DATA_WIDTH-1:0]        o_data,
    output logic [ADDR_WIDTH-1:0]        o_used,
    output logic                         o_full,
    output logic                         o_empty,
    output logic                         o_a_full,
    output logic                         o_a_empty  

);

//##################################
//         SIGNALS
//##################################

localparam DEPTH = 1 << ADDR_WIDTH;


logic                         w_full;
logic                         w_empty;
logic                         w_a_full;
logic                         w_a_empty;
logic [DATA_WIDTH-1:0]        w_data;
logic [ADDR_WIDTH-1:0]        w_used;
logic                         r_data_vld;

//##################################
//         VALID GEN
//##################################

always_ff @(posedge i_clk or posedge i_rst_sync)
begin
    if (i_rst_sync == 1'b1) begin
        r_data_vld <= 1'b0;
    end else begin
        r_data_vld <= i_trg_rd & ~w_empty;
    end 
end 

//##################################
//         INSTATION
//##################################


//


//##################################
//         OUTPUT
//##################################

assign o_full     = w_full;
assign o_empty    = w_empty;
assign o_a_full   = w_a_full;
assign o_a_empty  = w_a_empty;
assign o_used     = w_used;
assign o_data     = w_data;
assign o_data_vld = r_data_vld;
 
endmodule
