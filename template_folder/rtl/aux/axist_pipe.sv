module axist_pipe (
    input  logic         i_clk,
    input  logic         i_rst_n,

    AXI_ST_iface.sink    if_axist_in,
    AXI_ST_iface.source  if_axist_out
);
  
////////////////////////////////////////
//                signals              
////////////////////////////////////////

localparam DATA_WIDTH = if_axist_in.DATA_WIDTH;
localparam KEEP_WIDTH = if_axist_in.DATA_WIDTH/8;
localparam USER_WIDTH = if_axist_in.USER_WIDTH;

logic [DATA_WIDTH-1:0] r_tdata_head;
logic [DATA_WIDTH-1:0] r_tdata_skid;
logic [USER_WIDTH-1:0] r_tuser_head;
logic [USER_WIDTH-1:0] r_tuser_skid;
logic [KEEP_WIDTH-1:0] r_tkeep_head;
logic [KEEP_WIDTH-1:0] r_tkeep_skid;
logic                  r_tvalid_head;
logic                  r_tvalid_skid;
logic                  r_tlast_head;
logic                  r_tlast_skid;


logic                  w_skid_busy;

logic                  w_full;
logic                  w_pop;
logic                  w_push;

////////////////////////////////////////
//                skid              
////////////////////////////////////////

assign w_empty = ~w_skid_busy;
assign w_pop   = if_axist_out.if_tready & if_axist_out.if_tvalid;
assign w_push  = if_axist_in.if_tready & if_axist_in.if_tvalid;


always_ff @(posedge i_clk or negedge i_rst_n) begin
    if (i_rst_n == 1'b0) begin
        r_tvalid_head <= 1'b0; 
        r_tvalid_skid <= 1'b0; 
    end else begin
        if (w_pop == 1'b1) begin
          if (r_tvalid_skid == 1'b1) begin
            r_tvalid_head <= r_tvalid_skid;
            r_tvalid_skid <= 1'b0;
          end else begin
            r_tvalid_skid <= w_tvalid_skid;
          end
        end else begin
        end
        
    end
end

always_ff @(posedge i_clk) begin
    r_tdata_head  <= w_tdata_head;
    r_tuser_head  <= w_tuser_head;
    r_tkeep_head  <= w_tkeep_head;
    r_tlast_head  <= w_tlast_head;
    r_tdata_skid  <= w_tdata_skid;
    r_tuser_skid  <= w_tuser_skid;
    r_tkeep_skid  <= w_tkeep_skid;
    r_tlast_skid  <= w_tlast_skid;    
end

always_comb begin
    if (w_pop == 1'b1) begin
      if (r_tvalid_skid == 1'b1) begin
        // Move SKID into HEAD
        head_data_n  = skid_data;
        head_valid_n = 1'b1;
        skid_valid_n = 1'b0;
      end else begin
        // No skid: buffer becomes empty
        head_valid_n = 1'b0;
      end
    end

    // ------------------------------------------------------------
    // Step 2) PUSH into tail (head if empty, else skid)
    // ------------------------------------------------------------
    if (push) begin
      if (!head_valid_n) begin
        // Buffer empty after pop/shift -> put new beat in HEAD
        head_data_n  = s_data;
        head_valid_n = 1'b1;
      end else begin
        // HEAD already occupied -> put new beat in SKID
        // (Safe because push implies s_ready=1 implies skid_valid was 0)
        skid_data_n  = s_data;
        skid_valid_n = 1'b1;
      end
    end
  end
////////////////////////////////////////
//                output              
////////////////////////////////////////

assign if_axist_out.if_tdata  = r_tdata_head;
assign if_axist_out.if_tkeep  = r_tkeep_head;
assign if_axist_out.if_tuser  = r_tuser_head;
assign if_axist_out.if_tvalid = r_tvalid_head;
assign if_axist_out.if_tlast  = r_tlast_head;

assign if_axist_in.if_tready  = w_empty;

endmodule




module axis_regslice_skid #(
  parameter int W = 32  // payload width (pack {tlast,tkeep,tuser,tdata} if needed)
) (
  input  logic         clk,
  input  logic         rst,      // synchronous, active-high

  // Upstream (source) side
  input  logic [W-1:0] s_data,
  input  logic         s_valid,
  output logic         s_ready,

  // Downstream (sink) side
  output logic [W-1:0] m_data,
  output logic         m_valid,
  input  logic         m_ready
);

  // Two storage slots: HEAD (output) + SKID (extra)
  logic [W-1:0] head_data, skid_data;
  logic         head_valid, skid_valid;

  // Drive downstream from HEAD
  assign m_data  = head_data;
  assign m_valid = head_valid;

  // Upstream can send if we are not FULL.
  // FULL happens when SKID is occupied (since SKID implies HEAD is also occupied).
  // This breaks the combinational m_ready -> s_ready path.
  assign s_ready = ~skid_valid;

  // Handshake events
  wire pop  = m_ready && head_valid; // sink accepted HEAD this cycle
  wire push = s_valid && s_ready;    // we accepted new beat from source this cycle

  // Next-state signals (keeps the code easy to reason about)
  logic [W-1:0] head_data_n, skid_data_n;
  logic         head_valid_n, skid_valid_n;

  always_comb begin
    // Default: hold state
    head_data_n  = head_data;
    head_valid_n = head_valid;
    skid_data_n  = skid_data;
    skid_valid_n = skid_valid;

    // ------------------------------------------------------------
    // Step 1) POP from head (and shift skid -> head if needed)
    // ------------------------------------------------------------
    if (pop) begin
      if (skid_valid) begin
        // Move SKID into HEAD
        head_data_n  = skid_data;
        head_valid_n = 1'b1;
        skid_valid_n = 1'b0;
      end else begin
        // No skid: buffer becomes empty
        head_valid_n = 1'b0;
      end
    end

    // ------------------------------------------------------------
    // Step 2) PUSH into tail (head if empty, else skid)
    // ------------------------------------------------------------
    if (push) begin
      if (!head_valid_n) begin
        // Buffer empty after pop/shift -> put new beat in HEAD
        head_data_n  = s_data;
        head_valid_n = 1'b1;
      end else begin
        // HEAD already occupied -> put new beat in SKID
        // (Safe because push implies s_ready=1 implies skid_valid was 0)
        skid_data_n  = s_data;
        skid_valid_n = 1'b1;
      end
    end
  end

  always_ff @(posedge clk) begin
    if (rst) begin
      head_valid <= 1'b0;
      skid_valid <= 1'b0;
      head_data  <= '0;
      skid_data  <= '0;
    end else begin
      head_valid <= head_valid_n;
      skid_valid <= skid_valid_n;
      head_data  <= head_data_n;
      skid_data  <= skid_data_n;
    end
  end

endmodule