#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "vpi_user.h"

PLI_INT32 print_all_args_calltf(PLI_BYTE8 *user_data) {
    vpiHandle systf_handle = vpi_handle(vpiSysTfCall, NULL);
    vpiHandle arg_iter = vpi_iterate(vpiArgument, systf_handle);
    vpiHandle arg;
    s_vpi_value val;

    int arg_idx = 0;
    while ((arg = vpi_scan(arg_iter)) != NULL) {
        int type = vpi_get(vpiType, arg);

        val.format = vpiStringVal;
        vpi_get_value(arg, &val);
        if (type == vpiConstant || type == vpiParameter || type == vpiNet || type == vpiReg) {
            int format = vpi_get(vpiConstType, arg);
            if (format == vpiRealConst) {
                val.format = vpiRealVal;
                vpi_get_value(arg, &val);
                vpi_printf("[arg %0d] real: %f\n", arg_idx++, val.value.real);
            } else {
                val.format = vpiIntVal;
                vpi_get_value(arg, &val);
                vpi_printf("[arg %0d] int: %d\n", arg_idx++, val.value.integer);
            }
        } else if (type == vpiConstant || type == vpiStringConst) {
            val.format = vpiStringVal;
            vpi_get_value(arg, &val);
            vpi_printf("[arg %0d] string: %s\n", arg_idx++, val.value.str);
        } else {
            val.format = vpiStringVal;
            vpi_get_value(arg, &val);
            vpi_printf("[arg %0d] (unknown type, best guess): %s\n", arg_idx++, val.value.str);
        }
    }

    return 0;
}

void register_print_all_args() {
    s_vpi_systf_data tf_data;
    tf_data.type = vpiSysTask;
    tf_data.tfname = "$print_all_args";
    tf_data.calltf = print_all_args_calltf;
    tf_data.compiletf = 0;
    tf_data.sizetf = 0;
    tf_data.user_data = 0;
    vpi_register_systf(&tf_data);
}

void xcelium_reg_vpi() {
    register_print_all_args();
}


void (*vlog_startup_routines[])() = {
    register_print_all_args,
    0
};
