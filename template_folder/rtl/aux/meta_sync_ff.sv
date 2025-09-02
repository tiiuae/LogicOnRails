
module meta_sync_ff #(
    parameter N_STAGE =2,  // number of stages per bit line
    parameter N_WIDTH =1   // number of bit lines

)
(
    input  logic i_rst_n,
    input  logic [N_STAGE-1:0] i_sync_clk,
    input  logic [N_WIDTH-1:0] i_async,
    output logic [N_WIDTH-1:0] o_sync 
);
//------------------------------------------
//VARS
//------------------------------------------
genvar i, j;
//------------------------------------------
// SIGNALS
//------------------------------------------
    logic [N_WIDTH-1:0] meta_ff; 
    logic [N_STAGE-2:0] [N_WIDTH-1:0]sync_ff; 

//------------------------------------------
// HIERHARCHY
//------------------------------------------
generate
for (i = 0; i< N_WIDTH; i++ ) begin: BIT_GEN
     for (j = 0; j< N_STAGE; j++ ) begin: STAGE_GEN
         // META
         if (j == 0) begin : SYNC_0_GEN
             always_ff @(posedge i_sync_clk[j], negedge i_rst_n) begin
                 if (i_rst_n == 1'b0) begin
/* verilator lint_off MULTIDRIVEN */  
                     meta_ff[i] <= 1'b0;
                 end else begin
                     meta_ff[i] <= i_async[i];
/* verilator lint_on MULTIDRIVEN */  
                 end
             end
         // SYNC 1 stage
         end else if (j ==1) begin : SYNC_1_GEN
             always_ff @(posedge i_sync_clk[j], negedge i_rst_n) begin
                 if (i_rst_n == 1'b0) begin
/* verilator lint_off MULTIDRIVEN */  
                     sync_ff[j-1][i] <= 1'b0;
                 end else begin
                     sync_ff[j-1][i] <=meta_ff[i];
/* verilator lint_on MULTIDRIVEN */  
                 end
             end
         // SYNC 2 stage
         end else begin : SYNC_2_GEN
             always_ff @(posedge i_sync_clk[j], negedge i_rst_n) begin
                 if (i_rst_n == 1'b0) begin
/* verilator lint_off MULTIDRIVEN */  
                     sync_ff[j-1][i] <= 1'b0;
                 end else begin
                     sync_ff[j-1][i] <= sync_ff[j-2][i];
/* verilator lint_on MULTIDRIVEN */  
                 end
             end
         end
     end
     assign o_sync[i] = sync_ff[N_STAGE-2][i];
end
endgenerate

endmodule

