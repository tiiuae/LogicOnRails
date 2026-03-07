
module cross_clock_bus #(
    parameter DATA_WIDTH = 32,
    parameter SLOWER_2_FASTER = 1,
    parameter FAST = 1,
    parameter SLOW = 1    
)(
    input  logic                  i_clk_A,
    input  logic                  i_rst_A_n,
    input  logic                  i_clk_B,
    input  logic                  i_rst_B_n,
    input  logic                  i_valid_A,
    output logic                  o_ready_A,
    input  logic [DATA_WIDTH-1:0] i_signal_clk_A,
    output logic                  o_valid_B,
    output logic [DATA_WIDTH-1:0] o_signal_clk_B
);

/////////////////////////////////////////////////////////////////////////////////////
// signals                                                                         //
/////////////////////////////////////////////////////////////////////////////////////

localparam INT_AB_SLOW2FAST = (SLOWER_2_FASTER == 1)? 1 : 0;
localparam INT_BA_SLOW2FAST = (SLOWER_2_FASTER == 1)? 0 : 1;

logic                  r_ready_A;
logic [DATA_WIDTH-1:0] r_signal_meta_A;
logic                  w_cc_valid_A;
logic                  r_cc_valid_A [0:2];


logic [DATA_WIDTH-1:0] r_signal_meta_B [0:1];
logic [DATA_WIDTH-1:0] r_signal_B;
logic                  w_rd_B;
logic                  w_cc_valid_B;


/////////////////////////////////////////////////////////////////////////////////////
// A Domain                                                                        //
/////////////////////////////////////////////////////////////////////////////////////


cross_clock #(
    .SLOWER_2_FASTER ( INT_AB_SLOW2FAST ),
    .FAST            ( FAST             ),
    .SLOW            ( SLOW             )
) cross_clock_req_AtoB (
    .i_rst_A_n       ( i_rst_A_n      ),
    .i_rst_B_n       ( i_rst_B_n      ),
    .i_clk_A         ( i_clk_A        ),
    .i_signal_clk_A  ( i_valid_A      ),
    .i_clk_B         ( i_clk_B        ),
    .o_signal_clk_B  ( w_cc_valid_A   )
);


always_ff @(posedge i_clk_A or negedge i_rst_A_n)
begin
    if (i_rst_A_n == 1'b0) begin
        r_ready_A <= 1'b1;
    end else begin
        if (r_ready_A == 1'b1) begin
            r_ready_A <= ~i_valid_A;
        end else if (w_cc_valid_B == 1'b1) begin
            r_ready_A <= ~i_valid_A;
        end else begin
            r_ready_A <= 1'b1;
        end
    end
end


always_ff @(posedge i_clk_A)
begin
    if ((i_valid_A & r_ready_A) == 1'b1) begin
        r_signal_meta_A <= i_signal_clk_A;
    end
end

/////////////////////////////////////////////////////////////////////////////////////
// B Domain                                                                        //
/////////////////////////////////////////////////////////////////////////////////////



cross_clock #(
    .SLOWER_2_FASTER ( INT_BA_SLOW2FAST ),
    .FAST            ( FAST             ),
    .SLOW            ( SLOW             )
) cross_clock_rep_BtoA (
    .i_rst_A_n       ( i_rst_B_n       ),
    .i_rst_B_n       ( i_rst_A_n       ),
    .i_clk_A         ( i_clk_B         ),
    .i_signal_clk_A  ( r_cc_valid_A[2] ),
    .i_clk_B         ( i_clk_A         ),
    .o_signal_clk_B  ( w_cc_valid_B    )
);

always_ff @(posedge i_clk_B or negedge i_rst_B_n)
begin
    if (i_rst_B_n == 1'b0) begin
        r_cc_valid_A[0] <= 1'b0;
        r_cc_valid_A[1] <= 1'b0;
        r_cc_valid_A[2] <= 1'b0;
    end else begin
        r_cc_valid_A[0] <= w_cc_valid_A;
        r_cc_valid_A[1] <= r_cc_valid_A[0];
        r_cc_valid_A[2] <= r_cc_valid_A[1];        
    end
end

always_ff @(posedge i_clk_B)
begin
    r_signal_meta_B[0] <= r_signal_meta_A;
    r_signal_meta_B[1] <= r_signal_meta_B[0];
    r_signal_B         <= r_signal_meta_B[1];
end

/////////////////////////////////////////////////////////////////////////////////////
// output                                                                          //
/////////////////////////////////////////////////////////////////////////////////////

assign o_ready_A      = r_ready_A;
assign o_signal_clk_B = r_signal_B;
assign o_valid_B      = r_cc_valid_A[2];

endmodule