    `ifndef MESSAGE_LEVEL
    `define MESSAGE_LEVEL LOG_INF
    `endif

    `ifndef GREEN_C
    `define GREEN_C "\033\[1;32m"
    `endif
    
    `ifndef YELLOW_C
    `define YELLOW_C "\033\[1;33m"
    `endif
    
    `ifndef RED_C
    `define RED_C "\033\[1;31m"
    `endif

    `ifndef CYAN_C        
    `define CYAN_C "\033[1;36m"
    `endif

    `ifndef NO_C
    `define NO_C "\033\[0m"
    `endif

    `define log(ARG) $sformatf ARG
