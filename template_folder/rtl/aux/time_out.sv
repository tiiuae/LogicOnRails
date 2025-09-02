module time_out 
#(
    parameter STAGES = 2,
    parameter WIDTH  = 8    
)(
    input  logic i_clk,
    input  logic i_rst_n,
    input  logic i_clear,
    output logic o_timeout
);

//##################################
//         SIGNALS
//##################################

logic [WIDTH-1:0] a_stages [0:STAGES-1];

//##################################
//         CALC
//##################################

always_ff @(posedge i_clk or negedge i_rst_n)
begin
    if (i_rst_n == 1'b0) begin
        for (int i = 0; i < STAGES; i++) begin
            a_stages[i] <= 'b0;
        end 
    end else begin
        if (i_clear == 1'b1) begin
            for (int i = 0; i < STAGES; i++) begin
                a_stages[i] <= 'b0;
            end             
        end else begin
            for (int i = 0; i < STAGES; i++) begin
                if (i > 0) begin
                    if (a_stages[i-1] == '1) begin
                        a_stages[i] <= a_stages[i] + 1'b1;
                    end 
                end else begin
                    a_stages[0] <= a_stages[0] + 1'b1;
                end 
            end 
        end
    end 
end 


//##################################
//         OUTPUT
//##################################

assign o_timeout = &a_stages[STAGES-1];

endmodule