module axist_1dpipe (
    input  logic         i_clk,
    input  logic         i_rst_n,

    AXI_ST_iface.sink    if_axist_in,
    AXI_ST_iface.source  if_axist_out
);
  
//##################################
//         SIGNALS
//##################################

localparam DATA_WIDTH = if_axist_in.DATA_WIDTH;
localparam KEEP_WIDTH = if_axist_in.DATA_WIDTH/8;
localparam USER_WIDTH = if_axist_in.USER_WIDTH;

logic [DATA_WIDTH-1:0] r_tdata;
logic [KEEP_WIDTH-1:0] r_tkeep;
logic [USER_WIDTH-1:0] r_tuser;
logic                  r_tlast;
logic                  r_tvalid;

//##################################
//         MEMORY
//##################################

always_ff @(posedge i_clk) begin
    r_tdata <= if_axist_in.if_tdata;
    r_tkeep <= if_axist_in.if_tkeep;
    r_tuser <= if_axist_in.if_tuser;    
    r_tlast <= if_axist_in.if_tlast;    
end

always_ff @(posedge i_clk or negedge i_rst_n) 
begin
    if (i_rst_n == 1'b0) begin
        r_tvalid <= 1'b0;
    end else begin
        if ((if_axist_in.if_tready & if_axist_in.if_tvalid) == 1'b1) begin
            r_tvalid <= if_axist_in.if_tvalid;
        end else begin
            r_tvalid <= 1'b0;
        end
    end
end

//##################################
//         OUTPUT
//##################################

assign if_axist_out.if_tdata  = r_tdata; 
assign if_axist_out.if_tkeep  = r_tkeep;
assign if_axist_out.if_tuser  = r_tuser;
assign if_axist_out.if_tlast  = r_tlast;
assign if_axist_out.if_tvalid = r_tvalid;

assign if_axist_in.if_tready = if_axist_out.if_tready; 


endmodule