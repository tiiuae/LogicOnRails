module fractional_rate # (
    parameter int unsigned IN_CLK_HZ,
    parameter int unsigned OUT_RATE
)(
    input  logic       i_clk,
    input  logic       i_rst_n,
    input  logic       i_en,
    output logic       o_trg
);

//##################################
//         SIGNALS
//##################################

    int unsigned r_rate_acc;
    int unsigned w_acc_sum;
    logic        w_trg;


//##################################
//         RATE CALC
//##################################

    assign w_acc_sum = (i_en == 1'b1)? r_rate_acc + OUT_RATE      : '0;   // desired + rest
    assign w_trg     = (i_en == 1'b1)? (w_acc_sum >= IN_CLK_HZ) : 1'b0; // larger then clk? trg

    always_ff @(posedge i_clk or negedge i_rst_n) 
    begin
        if (i_rst_n == 1'b0) begin
            r_rate_acc      <= 0;
        end else begin
            if (i_en == 1'b1) begin
                if (w_trg == 1'b1) begin
                    r_rate_acc <= w_acc_sum - IN_CLK_HZ; //rest
                end else begin
                    r_rate_acc <= w_acc_sum;
                end
            end
        end
    end

//##################################
//         OUTPUT
//##################################

assign o_trg = w_trg;

endmodule