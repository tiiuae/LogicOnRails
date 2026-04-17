module axi_frontend #(
    parameter DATA_WIDTH,
    parameter ADDR_WIDTH,
    parameter ADDR_ALIGNMENT_UPPER,
    parameter ADDR_ALIGNMENT_BOTTOM,
    parameter ADDR_REQ_WIDTH = ADDR_ALIGNMENT_UPPER - ADDR_ALIGNMENT_BOTTOM + 1
)(
    input  logic                           i_clk,
    input  logic                           i_rst_n,
    
    output logic [DATA_WIDTH-1:0]          o_wr_data,
    output logic [ADDR_REQ_WIDTH-1:0]      o_wr_addr,
    output logic                           o_wr_vld,
    input  logic [DATA_WIDTH-1:0]          i_rd_data,
    output logic [ADDR_REQ_WIDTH-1:0]      o_rd_addr,

    AXI4opt_iface.slave                    if_axil_zynq
);

////////////////////////////////////////
//            signal
////////////////////////////////////////


typedef enum logic [1:0] { 
    S_IDLE      = 2'b00,
    S_WAIT_WR   = 2'b01,
    S_GEN_BRESP = 2'b10,
    S_GEN_READ  = 2'b11
} t_state;

t_state s_curr;

// axi {
logic [ADDR_WIDTH-1:0] r_awaddr;
logic [ADDR_WIDTH-1:0] r_araddr;
logic                  r_arready;
logic                  r_awready;
logic [DATA_WIDTH-1:0] w_rdata;
logic                  r_rvalid;
logic [1:0]            r_rresp;
logic                  r_wready;
logic                  r_bvalid;
logic [1:0]            r_bresp;
// }

logic [ADDR_REQ_WIDTH-1:0] w_wraddr;
logic [ADDR_REQ_WIDTH-1:0] w_rdaddr;
// }

////////////////////////////////////////
//            axi handling
////////////////////////////////////////

always_ff @(posedge i_clk) 
begin
    if ((if_axil_zynq.if_awvalid & r_awready) == 1'b1) begin
        r_awaddr  <= if_axil_zynq.if_awaddr;
    end
    if ((if_axil_zynq.if_arvalid & r_arready) == 1'b1) begin
        r_araddr  <= if_axil_zynq.if_araddr;
    end    
    r_rresp   <= '0;
    r_bresp   <= '0;        
end

always_ff @(posedge i_clk or negedge i_rst_n) begin
    if (i_rst_n == 1'b0) begin
        s_curr    <= S_IDLE;
        r_arready <= 1'b0;
        r_awready <= 1'b0;
        r_rvalid  <= 1'b0;
        r_wready  <= 1'b0;
        r_bvalid  <= 1'b0;
    end else begin
        case(s_curr)
        S_IDLE : begin
            r_rvalid  <= 1'b0;
            r_bvalid  <= 1'b0;
            r_wready  <= 1'b0;
            if (if_axil_zynq.if_awvalid == 1'b1) begin
                s_curr <= S_WAIT_WR;
                r_awready <= 1'b1;
                r_arready <= 1'b0;
            end else if (if_axil_zynq.if_arvalid == 1'b1) begin
                s_curr <= S_GEN_READ;
                r_awready <= 1'b0;
                r_arready <= 1'b1;
            end else begin
                r_awready <= 1'b0;
                r_arready <= 1'b0;
            end
        end
        S_WAIT_WR : begin
            r_awready <= 1'b0;
            if (if_axil_zynq.if_wvalid == 1'b1) begin
                s_curr    <= S_GEN_BRESP;
                r_wready  <= 1'b1;
            end
        end 
        S_GEN_BRESP : begin
            r_wready  <= 1'b0;
            if (if_axil_zynq.if_bready == 1'b1) begin
                s_curr   <= S_IDLE;
                r_bvalid <= 1'b1;
            end else begin
            end
        end 
        S_GEN_READ : begin
            r_arready <= 1'b0;
            if (if_axil_zynq.if_rready == 1'b1 ) begin
                s_curr   <= S_IDLE;
                r_rvalid <= 1'b1;
            end
        end
        endcase
    end
    
end

////////////////////////////////////////
//            axi data write
////////////////////////////////////////

assign w_wraddr = r_awaddr[ADDR_ALIGNMENT_UPPER:ADDR_ALIGNMENT_BOTTOM];

////////////////////////////////////////
//            axi date read
////////////////////////////////////////

assign w_rdaddr = r_araddr[ADDR_ALIGNMENT_UPPER:ADDR_ALIGNMENT_BOTTOM];

////////////////////////////////////////
//            output
////////////////////////////////////////

assign if_axil_zynq.if_arready = r_arready;  
assign if_axil_zynq.if_awready = r_awready;
assign if_axil_zynq.if_rdata   = i_rd_data;
assign if_axil_zynq.if_rvalid  = r_rvalid;
assign if_axil_zynq.if_rresp   = r_rresp;
assign if_axil_zynq.if_wready  = r_wready;
assign if_axil_zynq.if_bvalid  = r_bvalid;
assign if_axil_zynq.if_bresp   = r_bresp;
assign if_axil_zynq.if_rlast   = 1'b1;
assign if_axil_zynq.if_ruser   = '0;
assign if_axil_zynq.if_rid     = if_axil_zynq.if_arid;
assign if_axil_zynq.if_bid     = if_axil_zynq.if_awid;
assign if_axil_zynq.if_buser   = '0;

assign o_wr_data = if_axil_zynq.if_wdata;
assign o_wr_addr = w_wraddr;
assign o_rd_addr = w_rdaddr;
assign o_wr_vld  = if_axil_zynq.if_wvalid & r_wready;

endmodule