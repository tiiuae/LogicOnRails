
module reset_buffer
#(
    parameter STAGES = 1
)(
    input  logic i_clk,
    input  logic i_rst_n,
    output logic o_rst_n
);

//##################################
//         SIGNALS
//##################################

logic [STAGES-1:0] r_rst_n;

//##################################
//         RST BUFFER
//##################################

always_ff @(posedge i_clk)
begin
    r_rst_n[0] <= i_rst_n;
    for (int i = 1; i < STAGES; i++) begin
        r_rst_n[i] <= r_rst_n[i-1];
    end
end

//##################################
//         OUTPUT
//##################################

assign o_rst_n = r_rst_n[STAGES-1];

endmodule