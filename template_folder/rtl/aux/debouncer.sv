module debouncer #(
    parameter int unsigned P_WAIT_CYCLES = 1_000_000
)(
    input  logic i_clk,
    input  logic i_rst_n,
    input  logic i_sig_async,
    output logic o_sig_deb,
    output logic o_sig_syn
);

////////////////////////////////////////
//            SIGNALS
////////////////////////////////////////


    localparam int unsigned P_CNT_W = (P_WAIT_CYCLES <= 1) ? 1 : $clog2(P_WAIT_CYCLES);
    logic [1:0]         r_sync;
    logic               w_sig_sync;
    logic [P_CNT_W-1:0] r_cnt;
    logic               r_candidate;
    logic               r_sig_db;

////////////////////////////////////////
//            SYNCHRONIZER
////////////////////////////////////////


    always_ff @(posedge i_clk or negedge i_rst_n) begin
        if (i_rst_n == 1'b0) begin
            r_sync <= 2'b00;
        end else begin
            r_sync <= {r_sync[0], i_sig_async};
        end
    end

    assign w_sig_sync = r_sync[1];

////////////////////////////////////////
//              DEBOUNCE
////////////////////////////////////////


    always_ff @(posedge i_clk or negedge i_rst_n) begin
        if (i_rst_n == 1'b0) begin
            r_cnt       <= '0;
            r_candidate <= 1'b0;
            r_sig_db    <= 1'b0;
        end else begin
            if (w_sig_sync != r_candidate) begin
                r_candidate <= w_sig_sync;
                r_cnt       <= '0;
            end else begin
                if (P_WAIT_CYCLES <= 1) begin
                    r_sig_db <= r_candidate;
                end else if (r_cnt == P_CNT_W'(P_WAIT_CYCLES-1)) begin
                    r_sig_db <= r_candidate;
                end else begin
                    r_cnt <= r_cnt + 1'b1;
                end
            end
        end
    end

////////////////////////////////////////
//              OUTPUT
////////////////////////////////////////

assign o_sig_deb = r_sig_db;
assign o_sig_syn = w_sig_sync;

endmodule
