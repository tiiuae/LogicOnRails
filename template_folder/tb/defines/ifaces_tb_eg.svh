

///////////////////////////////////////////////////
/// FIELDS
///////////////////////////////////////////////////


`ifndef FIELD_MAC_SRC
`define FIELD_MAC_SRC 6
`endif

`ifndef FIELD_MAC_DST
`define FIELD_MAC_DST 6
`endif

`ifndef FIELD_TYPE
`define FIELD_TYPE 2
`endif

`ifndef FIELD_PAYLOAD
`define FIELD_PAYLOAD 46
`endif

`ifndef FIELD_CRC
`define FIELD_CRC 4
`endif

`ifndef FIELD_MIN_RANGE
`define FIELD_MIN_RANGE 0
`endif

`ifndef FIELD_MAX_RANGE
`define FIELD_MAX_RANGE 255
`endif

`ifndef FIELD_CONST_VAL
`define FIELD_CONST_VAL 85
`endif

`ifndef BOOL_RND_EN
`define BOOL_RND_EN 1
`endif

`ifndef BOOL_CONS_EN
`define BOOL_CONS_EN 0
`endif

`define NULL 0

///////////////////////////////////////////////////
/// PACKET NUMBER
///////////////////////////////////////////////////

`ifndef PKT_RND_EN
`define PKT_RND_EN 1
`endif

`ifndef PKT_CONS_EN
`define PKT_CONS_EN 0
`endif

`ifndef PKT_MIN_RANGE
`define PKT_MIN_RANGE 3
`endif

`ifndef PKT_MAX_RANGE
`define PKT_MAX_RANGE 3
`endif

`ifndef PKT_CONS
`define PKT_CONS 3
`endif

///////////////////////////////////////////////////
/// INTER FRAME GAP NUMBER
///////////////////////////////////////////////////

`ifndef IFG_RND_EN
`define IFG_RND_EN 1
`endif

`ifndef IFG_CONS_EN
`define IFG_CONS_EN 0
`endif

`ifndef IFG_MIN_RANGE
`define IFG_MIN_RANGE 2
`endif

`ifndef IFG_MAX_RANGE
`define IFG_MAX_RANGE 200
`endif

`ifndef IFG_CONS
`define IFG_CONS 15
`endif