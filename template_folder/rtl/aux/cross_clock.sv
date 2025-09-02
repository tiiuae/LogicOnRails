
module cross_clock #(
  parameter SLOWER_2_FASTER = 1,
  parameter FAST = 1,
  parameter SLOW = 1

  )
  (
    input  logic i_rst_A_n,
    input  logic i_rst_B_n,
    input  logic i_clk_A,
    input  logic i_signal_clk_A,
    input  logic i_clk_B,
    output logic o_signal_clk_B
);

/////////////////////////////////////////////////////////////////////////////////////
// SIGNALS                                                                         //
/////////////////////////////////////////////////////////////////////////////////////
logic w_result;

generate
if (SLOWER_2_FASTER) begin : slow_to_fast
/////////////////////////////////////////////////////////////////////////////////////
// SLOWER TO FASTER                                                                //
/////////////////////////////////////////////////////////////////////////////////////
    //SIGNAL
    logic       r_sync_A;
    logic [1:0] r_meta;

    always_ff @(posedge i_clk_A or negedge i_rst_A_n)
    begin
        if (i_rst_A_n == 1'b0) begin
            r_sync_A <= 1'b0;
        end else begin
            r_sync_A <= i_signal_clk_A;
        end 
    end 

    always_ff @(posedge i_clk_B or negedge i_rst_B_n)
    begin
        if (i_rst_B_n == 1'b0) begin
            r_meta <= '0;
        end else begin
            r_meta[0] <= r_sync_A;
            r_meta[1] <= r_meta[0];
        end 
    end 
    assign w_result = r_meta[1];
    
end else begin : fast_to_slow
/////////////////////////////////////////////////////////////////////////////////////
// FASTER TO SLOWER                                                                //
/////////////////////////////////////////////////////////////////////////////////////

    //SIGNAL
    localparam RATE = (FAST/SLOW)*2;
    localparam RATE_VALUE = RATE-1;
    localparam COUNTER_RATE = $clog2(RATE);
    logic [COUNTER_RATE-1:0] c_counter;
    logic w_faster_stretch;
    logic r_faster_stretch;
    logic [1:0] r_meta;
    logic       r_sync_A;


    //FASTER COUNTER
    always_ff @(posedge i_clk_A or negedge i_rst_A_n)
    begin
        if(i_rst_A_n == 1'b0) begin
             c_counter        <= 'b0;
             r_faster_stretch <= 1'b0;
             r_sync_A         <= 1'b0;
        end else begin
             if(i_signal_clk_A) begin
                 c_counter <= RATE_VALUE[COUNTER_RATE-1:0];
             end else if(c_counter > 0) begin
                 c_counter <= c_counter - 1'b1;
             end
             r_faster_stretch <= w_faster_stretch;
             r_sync_A         <= r_faster_stretch;
        end
    end

    //STRETCH
    assign w_faster_stretch = (c_counter > 0)? 1'b1 : 1'b0;

    always_ff @(posedge i_clk_B or negedge i_rst_B_n)
    begin
        if (i_rst_B_n == 1'b0) begin
            r_meta <= '0;
        end else begin
            r_meta[0] <= r_sync_A;
            r_meta[1] <= r_meta[0];
        end 
    end 
    assign w_result = r_meta[1];

end
endgenerate

/////////////////////////////////////////////////////////////////////////////////////
// OUTPUT                                                                          //
/////////////////////////////////////////////////////////////////////////////////////

assign o_signal_clk_B = w_result;

endmodule
