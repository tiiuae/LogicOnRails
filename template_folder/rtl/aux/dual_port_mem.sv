module dual_port_mem
#(
    parameter DATA_WIDTH=8, 
    parameter ADDR_WIDTH=6
)
(
    input  logic                  i_wr_clk,
    input  logic                  i_rd_clk,
    input  logic                  i_wr,
    input  logic                  i_rd,
    input  logic [ADDR_WIDTH-1:0] i_addr_rd, 
    input  logic [ADDR_WIDTH-1:0] i_addr_wr,    
    input  logic [DATA_WIDTH-1:0] i_wrdata,
    output logic [DATA_WIDTH-1:0] o_rddata
);
//##################################
//         SIGNALS
//##################################

logic [DATA_WIDTH-1:0] a_ram [2**ADDR_WIDTH-1:0];
logic [DATA_WIDTH-1:0] r_rddata;

//##################################
//         MEMORY
//##################################

always_ff @ (posedge i_wr_clk)
begin
    if (i_wr == 1'b1) begin
        a_ram[i_addr_wr] <= i_wrdata;
    end
end

always_ff @ (posedge i_rd_clk)
begin
    if (i_rd == 1'b1) begin
        r_rddata <= a_ram[i_addr_rd];
    end
end

//##################################
//         OUTPUT
//##################################

assign o_rddata = r_rddata;

endmodule