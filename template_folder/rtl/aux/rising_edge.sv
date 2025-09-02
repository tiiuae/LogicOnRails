module rising_edge
  #(
    parameter REGISTER = 0
    )(
    input  logic i_rst_n,
    input  logic i_clk,
    input  logic i_data,
    output logic o_data
);

//##################################
//         RISING EDGE
//##################################

generate
    if(REGISTER) begin : data_registering
        logic r_d0;
        logic r_d1;

        always_ff @(posedge i_clk or negedge i_rst_n) begin
            if(i_rst_n == 1'b0) begin
                r_d0 <= 1'b0;
                r_d1 <= 1'b0;
            end else begin
                r_d0 <= i_data;
                r_d1 <= r_d0;
            end
        end

        assign o_data = r_d0 & ~r_d1;

    end else begin : no_data_registering
        logic r_d0;

        always_ff @(posedge i_clk or negedge i_rst_n) begin
            if(i_rst_n == 1'b0) begin
                r_d0 <= 1'b0;
            end else begin
                r_d0 <= i_data;
            end
        end

        assign o_data = i_data & ~r_d0;

    end
endgenerate

endmodule