#include <stdio.h>
#include <string.h>
#include "vpi_user.h"

PLI_INT32 print_str_calltf(PLI_BYTE8 *user_data) {
    vpiHandle arg_iter, arg;
    s_vpi_value val;

    arg_iter = vpi_iterate(vpiArgument, vpi_handle(vpiSysTfCall, NULL));
    arg = vpi_scan(arg_iter);

    val.format = vpiStringVal;
    vpi_get_value(arg, &val);

    vpi_printf("User string: %s\n", val.value.str);

    return 0;
}

void register_print_str() {
    s_vpi_systf_data tf_data;
    tf_data.type = vpiSysTask;
    tf_data.tfname = "$print_str";
    tf_data.calltf = print_str_calltf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    vpi_register_systf(&tf_data);
}

void xcelium_reg_vpi() {
    register_print_str();
}

void (*vlog_startup_routines[])() = {
    register_print_str,
    0
};
