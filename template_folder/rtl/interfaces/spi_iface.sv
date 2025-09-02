interface SPI_iface ();

//##################################
//         SIGNALS
//##################################

logic if_ss;
logic if_sclk;
logic if_sdi;
logic if_sdo;

//##################################
//         MODPORT
//##################################

modport master (
   output if_ss,
   output if_sclk,
   output if_sdi,
   input  if_sdo
);

modport slave (
   input  if_ss,
   input  if_sclk,
   input  if_sdi,
   output if_sdo
);

endinterface
