interface zynq_i2c_iface ();

//##################################
//         SIGNALS
//##################################

logic if_sda_i;
logic if_sda_o;
logic if_sda_t;
logic if_scl_i;
logic if_scl_o;
logic if_scl_t;

//##################################
//         MODPORT
//##################################

modport master (
   output if_sda_t,
   output if_sda_o,
   input  if_sda_i,
   output if_scl_t,
   output if_scl_o,
   input  if_scl_i
);

modport slave (
   input  if_sda_t,
   input  if_sda_o,
   output if_sda_i,
   input  if_scl_t,
   input  if_scl_o,
   output if_scl_i   
);

endinterface
