`timescale 1 ps / 1 ps
module fifo_manager #(
    parameter DATA_WIDTH       = 512,
    parameter ADDRESS_WIDTH    = 64,
    parameter A_FULL_WATERMARK = 42
)(
	// fifo controll
    input  logic                     i_clk_wr,
	input  logic                     i_clk_rd,
	input  logic                     i_rst_n,
    input  logic                     i_fifo_wr,
    input  logic                     i_fifo_rd,
    input  logic [DATA_WIDTH-1:0]    i_fifo_data,
    output logic                     o_empty,
    output logic                     o_full,
    output logic                     o_error_rd,
    output logic                     o_error_wr,    
    output logic [DATA_WIDTH-1:0]    o_fifo_data,
    output logic                     o_fifo_rddata_vld,
    output logic                     o_a_full,

    // memory wr
    output logic [DATA_WIDTH-1:0]    o_mem_data,
    output logic                     o_mem_wr,
    output logic [ADDRESS_WIDTH-1:0] o_used,
    output logic                     o_mem_rd,
    output logic [ADDRESS_WIDTH-1:0] o_mem_addr_wr,
    output logic [ADDRESS_WIDTH-1:0] o_mem_addr_rd,
    input  logic [DATA_WIDTH-1:0]    i_mem_data

);

//##################################
//         SIGNALS
//##################################
// parameters {
localparam  DEPTH=(1<<ADDRESS_WIDTH);
//}

// io {
logic                  w_empty;
logic                  r_empty;
logic                  w_aux_full;
logic                  w_full;
logic                  w_error_rd;
logic                  w_error_wr;
// }

// bypass {
logic [DATA_WIDTH-1:0] w_fifo_data;
logic                  w_fifo_wr;
logic                  w_fifo_rd;
logic [DATA_WIDTH-1:0] w_mem_data;
// }


// write {
logic                     r_wr;
logic [DATA_WIDTH-1:0]    r_mem_data;
logic [ADDRESS_WIDTH-1:0] r_mem_addr_wr;
logic [ADDRESS_WIDTH-1:0] r_mem_addr_wr_dly;
logic [ADDRESS_WIDTH-1:0] r_wr_ptr; 
logic [ADDRESS_WIDTH-1:0] w_wr_ptr_nxt; 
logic [ADDRESS_WIDTH-1:0] w_wr_ptr_gray; 
logic [ADDRESS_WIDTH-1:0] w_cc_rd_ptr_gray; 
logic [ADDRESS_WIDTH-1:0] r_meta_wr [0:1];
// }

// read {
logic                     r_rd;
logic [ADDRESS_WIDTH-1:0] r_mem_addr_rd;
logic [ADDRESS_WIDTH-1:0] r_mem_addr_rd_dly;
logic [2:0]               r_delay_vld;
logic [ADDRESS_WIDTH-1:0] r_rd_ptr;
logic [ADDRESS_WIDTH-1:0] w_rd_ptr_gray; 
logic [ADDRESS_WIDTH-1:0] w_rd_ptr_bin; 
logic [ADDRESS_WIDTH-1:0] w_cc_wr_ptr_gray; 
logic [ADDRESS_WIDTH-1:0] r_meta_rd [0:1];
//}

// used {
logic [ADDRESS_WIDTH-1:0] w_used;
logic [ADDRESS_WIDTH-1:0] r_used_sub;
logic [ADDRESS_WIDTH-1:0] r_used_sub_fix;
logic [ADDRESS_WIDTH-1:0] r_used;
logic [ADDRESS_WIDTH-1:0] r_used_dly;  
logic                     r_a_full; 
//}

genvar i;
//##################################
//         BYPASS
//##################################

assign w_fifo_data = i_fifo_data;
assign w_mem_data  = i_mem_data;
assign w_fifo_wr   = (w_full == 1'b1)? 1'b0  : i_fifo_wr;
assign w_fifo_rd   = (w_empty == 1'b1)? 1'b0 : i_fifo_rd;

//##################################
//         POINTER WR
//##################################

always_ff @(posedge i_clk_wr or negedge i_rst_n) begin
	if (i_rst_n == 1'b0) begin
		r_wr_ptr <= 'b0;
	end else if (i_fifo_wr == 1'b1 && w_full == 1'b0 ) begin
		r_wr_ptr <= r_wr_ptr+1'b1;
	end
end



//##################################
//        WR GRAY CONVERSION
//##################################

assign w_wr_ptr_gray = (r_wr_ptr >>1) ^ r_wr_ptr;
assign w_wr_ptr_nxt  = r_wr_ptr+1'b1;


//##################################
//        SYNC DOMAINS
//##################################

always_ff @(posedge i_clk_rd or negedge i_rst_n)
begin
    if (i_rst_n == 1'b0) begin
        r_meta_rd[0] <= '0;
        r_meta_rd[1] <= '0;
    end else begin
        r_meta_rd[0] <= w_wr_ptr_gray;
        r_meta_rd[1] <= r_meta_rd[0];
    end 
end 

assign w_cc_wr_ptr_gray = r_meta_rd[1];

always_ff @(posedge i_clk_wr or negedge i_rst_n)
begin
    if (i_rst_n == 1'b0) begin
        r_meta_wr[0] <= '0;
        r_meta_wr[1] <= '0;
    end else begin
        r_meta_wr[0] <= w_rd_ptr_gray;
        r_meta_wr[1] <= r_meta_wr[0];
    end 
end 

assign w_cc_rd_ptr_gray = r_meta_wr[1];

//##################################
//        READ
//##################################

always_ff @(posedge i_clk_rd or negedge i_rst_n) 
begin
	if (i_rst_n == 1'b0) begin
		r_rd_ptr <= 'b0;
	end else if (w_fifo_rd == 1'b1  && w_empty == 1'b0) begin
		r_rd_ptr <= r_rd_ptr + 1'b1;
    end
end

//##################################
//        VALID DATA GEN
//##################################

always_ff @(posedge i_clk_rd or negedge i_rst_n)
begin
    if (i_rst_n == 1'b0) begin
        r_delay_vld <= 'b0;
    end else begin
        r_delay_vld[0] <= w_fifo_rd;
        r_delay_vld[1] <= r_delay_vld[0];
        r_delay_vld[2] <= r_delay_vld[1];
    end
end 


//##################################
//        RD GRAY CONVERSION
//##################################

assign w_rd_ptr_gray = (r_rd_ptr>>1) ^ r_rd_ptr;

generate
    for (i=0; i<ADDRESS_WIDTH; i = i+1'b1) begin : gray2dec
        assign w_rd_ptr_bin[i] = ^(w_cc_rd_ptr_gray >> i);
    end : gray2dec
endgenerate


//##################################
//        FULL - EMPTY
//##################################

assign w_aux_full  = (r_wr_ptr == w_rd_ptr_bin)? 1'b1 : 1'b0;
assign w_full      = (w_aux_full == r_empty)? 1'b0 : w_aux_full;
assign w_empty     = (w_rd_ptr_gray == w_cc_wr_ptr_gray)? 1'b1 & ~w_full: 1'b0;

always_ff @(posedge i_clk_rd or negedge i_rst_n) begin
	if (i_rst_n == 1'b0) begin
		r_empty <= 'b1;
	end else begin
        if (w_full == 1'b1) begin
            r_empty <= 1'b0;
        end else begin
            r_empty <= w_empty;
        end 
	end
end

//##################################
//         ERROR CONTROLL
//##################################

assign w_error_rd = i_fifo_rd & w_empty;
assign w_error_wr = i_fifo_wr & w_full;


//##################################
//         REGISTER OUTPUTS
//##################################

always_ff @(posedge i_clk_wr or negedge i_rst_n) 
begin
    if (i_rst_n == 1'b0) begin
        r_wr <= 1'b0;
    end else begin
        if (w_full == 1'b0) begin
            r_wr <= w_fifo_wr;
        end
    end 
end 

always_ff @(posedge i_clk_wr)
begin
    if (w_full == 1'b0) begin
        r_mem_addr_wr <= r_wr_ptr;
        r_mem_data    <= w_fifo_data;    
    end
end 

always_ff @(posedge i_clk_rd)
begin
    r_rd          <= w_fifo_rd;
    r_mem_addr_rd <= r_rd_ptr;
end 

//##################################
//         PIPELINE
//##################################

always_ff @(posedge i_clk_wr)
begin
    r_mem_addr_wr_dly <= r_mem_addr_wr; 
    r_mem_addr_rd_dly <= r_mem_addr_rd;
    r_used_sub        <= r_mem_addr_wr - r_mem_addr_rd ;
    r_used_sub_fix    <= (1 << ADDRESS_WIDTH) + r_mem_addr_wr - r_mem_addr_rd -1;    
end 

assign w_used = (r_mem_addr_wr_dly >= r_mem_addr_rd_dly)? r_used_sub  : r_used_sub_fix;

always_ff @(posedge i_clk_wr)
begin
    r_used     <= w_used;
    r_used_dly <= r_used;
end 

always_ff @(posedge i_clk_wr or negedge i_rst_n)
begin
    if (i_rst_n == 1'b0) begin
        r_a_full <= 1'b0;
    end else begin
        r_a_full <= (r_used_dly >= ADDRESS_WIDTH'(A_FULL_WATERMARK));
    end 
end 

//##################################
//         OUTPUT
//##################################

assign o_fifo_data        = w_mem_data;
assign o_fifo_rddata_vld  = r_delay_vld[2];

assign o_mem_wr        = r_wr;
assign o_mem_addr_wr   = r_mem_addr_wr;
assign o_mem_data      = r_mem_data;
assign o_mem_rd        = r_rd;
assign o_mem_addr_rd   = r_mem_addr_rd;

assign o_empty         = w_empty;
assign o_a_full        = r_a_full;
assign o_full          = w_full;

assign o_error_rd      = w_error_rd;
assign o_error_wr      = w_error_wr;
assign o_used          = r_used_dly;

endmodule
