module reset_sync #(
    parameter RST_LEVEL
)(
    input  logic i_clk,
    input  logic i_rst,
    output logic o_rst
);

//##################################
//    SIGNALS
//##################################

logic r_rst;
logic r_rst_sync [0:2];

//##################################
//    RESET
//##################################

generate 
    if (RST_LEVEL == 1'b1) begin
        
        always_ff @(posedge i_clk or posedge i_rst)
        begin
            if (i_rst == 1'b1) begin
        		r_rst <= 1'b1;
        	end else begin
        		r_rst <= 1'b0;
        	end
        end

    end else begin
        
        always_ff @(posedge i_clk or negedge i_rst)
        begin
            if (i_rst == 1'b0) begin
        		r_rst <= 1'b0;
        	end else begin
        		r_rst <= 1'b1;
        	end
        end

    end  
endgenerate

//##################################
//    SYNCHRONIZER
//##################################

always_ff @(posedge i_clk)
begin
    r_rst_sync[0] <= r_rst;
	r_rst_sync[1] <= r_rst_sync[0];
	r_rst_sync[2] <= r_rst_sync[1];
end

//##################################
//    OUTPUT
//##################################

assign o_rst = r_rst_sync[2];

endmodule
