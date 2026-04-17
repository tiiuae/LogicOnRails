module ext_mem 

`ifndef MESSAGE_LEVEL
`define MESSAGE_LEVEL LOG_INF
`endif

import logger_pkg::*;
#(
    parameter MIN_AW_RDY_DLY  = 1,
    parameter MAX_AW_RDY_DLY  = 1,
    parameter MIN_AR_RDY_DLY  = 1,
    parameter MAX_AR_RDY_DLY  = 1,
    parameter MIN_W_RDY_DLY   = 1,
    parameter MAX_W_RDY_DLY   = 1,
    parameter MIN_R_RDY_DLY   = 1,
    parameter MAX_R_RDY_DLY   = 1,
    parameter MIN_B_RDY_DLY   = 1,
    parameter MAX_B_RDY_DLY   = 1,
    parameter MIN_R_LTNCY_DLY = 1,
    parameter MAX_R_LTNCY_DLY = 1,
    parameter MIN_B_LTNCY_DLY = 1,
    parameter MAX_B_LTNCY_DLY = 1,
    parameter MEM_DEPTH       = 64,
    parameter RESET_STARTUP   = 1,
    parameter RND_STARTUP     = 1
)(
    input logic         i_clk,
    AXI4opt_iface.slave if_axi_mem
);
// =============================================================================
//                           SIGNALS
//
// =============================================================================

`define log(ARG) $sformatf ARG

localparam MIN_DEL = 0;
localparam MAX_DEL = 1;

localparam READ_CH   = 0;
localparam REPLY_CH  = 1;
localparam ADDRWR_CH = 2;
localparam ADDRRD_CH = 3;
localparam WRITE_CH  = 4;

int rdy_del_arr [][] = '{
    '{ MIN_R_RDY_DLY  , MAX_R_RDY_DLY  },
    '{ MIN_B_RDY_DLY  , MAX_B_RDY_DLY  },
    '{ MIN_AW_RDY_DLY , MAX_AW_RDY_DLY },
    '{ MIN_AR_RDY_DLY , MAX_AR_RDY_DLY },
    '{ MIN_W_RDY_DLY  , MAX_W_RDY_DLY  }
};

int ltncy_del_arr [][] = '{
    '{ MIN_R_LTNCY_DLY , MAX_R_LTNCY_DLY },
    '{ MIN_B_LTNCY_DLY , MAX_B_LTNCY_DLY }
};

typedef struct packed {
    logic [if_axi_mem.ADDR_WIDTH-1:0] addr;
    logic [7:0]                       len;
    logic [1:0]                       burst;
    logic [if_axi_mem.ID_WIDTH-1:0]   id;
} t_axi_addr;
//t_axi_addr axi_ar_dict [logic [if_axi_mem.ID_WIDTH-1:0]];
t_axi_addr axi_ar_queue [$:1];
t_axi_addr axi_aw_queue [$:1];

logic [if_axi_mem.DATA_WIDTH-1:0] a_mem [MEM_DEPTH-1:0]; 
Logger ag_logger;

// =============================================================================
//                           PRINT
//
// =============================================================================

function print_mem();
    $display("\n///////////////////////////////////");
    for (int i = 0; i < MEM_DEPTH; i++) begin
        $display("addr %02h: %02h", i, a_mem[i]);
    end
endfunction

// =============================================================================
//                           DELAY
//
// =============================================================================

task automatic gen_delay (
    input int channel 
);
    int rnd_del = $urandom_range(rdy_del_arr[channel][MIN_DEL], rdy_del_arr[channel][MAX_DEL]);     
    for (int i = 0; i < rnd_del; i++) begin
        @(posedge i_clk);
    end
endtask

task automatic gen_resp_delay (
    input int channel 
);
    int rnd_del = $urandom_range(ltncy_del_arr[channel][MIN_DEL], ltncy_del_arr[channel][MAX_DEL]);     
    for (int i = 0; i < rnd_del; i++) begin
        @(posedge i_clk);
    end
endtask

task reset_signals ();
    if_axi_mem.if_arready = 1'b0;  
    if_axi_mem.if_rdata   = '0;
    if_axi_mem.if_rresp   = '0;
    if_axi_mem.if_rvalid  = 1'b0;
    if_axi_mem.if_rlast   = 1'b0;
    if_axi_mem.if_rid     = '0;
    if_axi_mem.if_ruser   = '0;
    if_axi_mem.if_awready = 1'b0;
    if_axi_mem.if_wready  = 1'b0;
    if_axi_mem.if_bresp   = '0;
    if_axi_mem.if_bvalid  = 1'b0;
    if_axi_mem.if_bid     = '0;
    @(posedge i_clk);
endtask

function automatic reset_mem();
    for (int i = 0; i < MEM_DEPTH; i++) begin
        if (RND_STARTUP == 1) begin
            a_mem[i] = $urandom_range(0, ((1 << if_axi_mem.DATA_WIDTH-1) - 1));
        end else begin
            a_mem[i] = '1;
        end
    end
endfunction

// =============================================================================
//                           ADDRESS
//
// =============================================================================

function automatic logic [if_axi_mem.ADDR_WIDTH-1:0] handle_addr(
    input logic [if_axi_mem.ADDR_WIDTH-1:0] addr,
    input logic [1:0]                       awburst,
    input logic [7:0]                       awlen
);
    if (awburst == 2'b00) begin
        return addr;
    end else if (awburst == 2'b01) begin
        return addr + 1;
    end else begin
        return '0;
    end
endfunction



// =============================================================================
//                           WRITE MEM
//
// =============================================================================

task cnfg_wraddr_ch ();
    t_axi_addr this_axi_awprofile;
    while (if_axi_mem.if_awvalid !== 1'b1) begin
        @(posedge i_clk);
    end
    this_axi_awprofile.addr  = if_axi_mem.if_awaddr;
    this_axi_awprofile.len   = if_axi_mem.if_awlen;
    this_axi_awprofile.burst = if_axi_mem.if_awburst;
    this_axi_awprofile.id    = if_axi_mem.if_awid;
    if (axi_aw_queue.size() == 0) begin
        axi_aw_queue.push_front(this_axi_awprofile);
    end else begin
        ag_logger.log(`log(("received two aw req in sequence", )), LOG_WRN);
    end 
    gen_delay(ADDRWR_CH);
    if_axi_mem.if_awready = 1'b1;
    @(posedge i_clk);
    if_axi_mem.if_awready = 1'b0;
endtask;

task cnfg_wr_ch (
    output logic [1:0]                     bresp,
    output logic [if_axi_mem.ID_WIDTH-1:0] bid
);
    t_axi_addr                        this_axi_wprofile;
    logic [if_axi_mem.ADDR_WIDTH-1:0] this_addr;
    while (if_axi_mem.if_wvalid !== 1'b1) begin
        @(posedge i_clk);
    end
    if (axi_aw_queue.size() > 0) begin
        this_axi_wprofile = axi_aw_queue.pop_back();
        this_addr = this_axi_wprofile.addr % MEM_DEPTH;
        bid = this_axi_wprofile.id;
        gen_delay(WRITE_CH);
        for (int i = 0; i < this_axi_wprofile.len+1; i++) begin
            #100ps;
            ag_logger.log(`log(("memory: received id %h, value %h addr %h", bid, if_axi_mem.if_wdata, this_addr)), LOG_INF);
            a_mem[this_addr] = if_axi_mem.if_wdata;
            this_addr = (handle_addr(this_addr, this_axi_wprofile.burst, this_axi_wprofile.len) % MEM_DEPTH);
            if_axi_mem.if_wready <= 1'b1;
            @(posedge i_clk);
        end
        bresp = 2'b00;
    end else begin
        ag_logger.log(`log(("no matching aw req for this write req")), LOG_CRT);
        bresp = 2'b10;
        bid = '0;
    end 
    ag_logger.log(`log(("memory: end write batch id %h", bid)), LOG_INF);
    if_axi_mem.if_wready <= 1'b0;
endtask;

task cnfg_bresp_ch (
    input logic [1:0]                     bresp,
    input logic [if_axi_mem.ID_WIDTH-1:0] bid

);
    gen_resp_delay(REPLY_CH);
    if_axi_mem.if_bvalid <= 1'b1;
    if_axi_mem.if_bresp  <= bresp;
    if_axi_mem.if_bid    <= bid;
    @(posedge i_clk);
    while (if_axi_mem.if_bready !== 1'b1) begin
        @(posedge i_clk);
    end        
    if_axi_mem.if_bvalid <= 1'b0;
    @(posedge i_clk);
endtask;

task store_data ();
    logic [1:0]                     bresp;
    logic [if_axi_mem.ID_WIDTH-1:0] bid;
    cnfg_wraddr_ch();
    cnfg_wr_ch(bresp, bid);
    cnfg_bresp_ch(bresp, bid);
endtask;

// =============================================================================
//                           READ MEM
//
// =============================================================================

task cnfg_rdaddr_ch ();
    t_axi_addr this_axi_arprofile;
    while (if_axi_mem.if_arvalid !== 1'b1) begin
        @(posedge i_clk);
    end
    this_axi_arprofile.addr  = if_axi_mem.if_araddr;
    this_axi_arprofile.len   = if_axi_mem.if_arlen;
    this_axi_arprofile.burst = if_axi_mem.if_arburst;
    this_axi_arprofile.id    = if_axi_mem.if_arid;
    if (axi_ar_queue.size() == 0) begin
        axi_ar_queue.push_front(this_axi_arprofile);
    end else begin
        axi_ar_queue.push_front(this_axi_arprofile);
        ag_logger.log(`log(("received two ar req in sequence", )), LOG_WRN);
    end 
    gen_delay(ADDRRD_CH);
    if_axi_mem.if_arready = 1'b1;
    @(posedge i_clk);
    if_axi_mem.if_arready = 1'b0;
endtask;

task cnfg_rd_ch (
    output logic [if_axi_mem.ID_WIDTH-1:0] rid
);
    t_axi_addr                        this_axi_rprofile;
    logic [if_axi_mem.ADDR_WIDTH-1:0] this_addr;
    gen_resp_delay(READ_CH);
    if (axi_ar_queue.size() > 0) begin
        this_axi_rprofile = axi_ar_queue.pop_back();
        this_addr = this_axi_rprofile.addr % MEM_DEPTH;
        rid = this_axi_rprofile.id;
        gen_delay(READ_CH);
        for (int i = 0; i < this_axi_rprofile.len+1; i++) begin
            while (if_axi_mem.if_rready !== 1'b1) begin
                @(posedge i_clk);
            end
            if_axi_mem.if_rdata  <= a_mem[this_addr];
            if_axi_mem.if_rvalid <= 1'b1;
            if_axi_mem.if_rid    <= rid;
            if (i == this_axi_rprofile.len) begin
                if_axi_mem.if_rlast <= 1'b1;
            end 
            this_addr <= (handle_addr(this_addr, this_axi_rprofile.burst, this_axi_rprofile.len) % MEM_DEPTH);
            @(posedge i_clk);
        end
    end else begin
        ag_logger.log(`log(("critical tb error, read triggered without correspondent ar req")), LOG_ERR);
        $stop;
    end 
    if_axi_mem.if_rlast <= 1'b0;
    if_axi_mem.if_rvalid <= 1'b0;
endtask;


task fetch_data ();
    logic [if_axi_mem.ID_WIDTH-1:0] rid;
    cnfg_rdaddr_ch();
    cnfg_rd_ch(rid);
endtask;


// =============================================================================
//                           INIT
//
// =============================================================================

task init_mem ();
    ag_logger = new(`MESSAGE_LEVEL, 1'b1);
    reset_signals();
    if (RESET_STARTUP == 1) begin
        reset_mem();
    end
endtask;

initial
begin
    init_mem();
    fork
        forever begin
            store_data();
        end
        forever begin
            fetch_data();
        end
    join_none
end

endmodule