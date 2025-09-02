package verif_pkg;

    localparam NS     = 1;
    localparam US     = 1000;
    localparam MS     = (1000*1000);
    localparam S      = (1000*1000*1000);
    localparam TRUE   = 1'b1;
    localparam FALSE  = 1'b0;

    localparam SYS_PERIOD          = 10;

    localparam LOG_RESULTS         = 1'b0;
    localparam HEART_BEAT          = 1'b1;
    localparam STOP_AT_ERROR       = 1'b0;
    localparam VERBOSE             = 1'b1;
    localparam MAX_LOOP_COUNT      = 3;

endpackage
