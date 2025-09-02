#include <stdio.h>
#include <stdlib.h>
#include "vpi_user.h"

// Recursively print the design hierarchy
void print_hierarchy_recursive(vpiHandle module, int indent) {
    const char *name = vpi_get_str(vpiFullName, module);
    for (int i = 0; i < indent; ++i) vpi_printf("  ");
    vpi_printf("%s\n", name);

    // Recurse into instances inside this module
    vpiHandle inst_iter = vpi_iterate(vpiModule, module);
    if (inst_iter) {
        vpiHandle inst;
        while ((inst = vpi_scan(inst_iter))) {
            print_hierarchy_recursive(inst, indent + 1);
        }
    }
}

// System task callback
PLI_INT32 print_hierarchy_calltf(char *user_data) {
    vpi_printf("=== Design Hierarchy ===\n");

    vpiHandle mod_iter = vpi_iterate(vpiModule, NULL);
    if (mod_iter) {
        vpiHandle mod;
        while ((mod = vpi_scan(mod_iter))) {
            print_hierarchy_recursive(mod, 0);
        }
    }

    return 0;
}

// Register the $print_hierarchy system task
void register_print_hierarchy() {
    s_vpi_systf_data tf_data = {
        .type = vpiSysTask,
        .tfname = "$print_hierarchy",
        .calltf = print_hierarchy_calltf,
        .compiletf = NULL,
        .sizetf = NULL,
        .user_data = NULL
    };

    vpi_register_systf(&tf_data);
}

void xcelium_reg_vpi() {
    register_print_hierarchy();
}


// Required VPI startup table
void (*vlog_startup_routines[])() = {
    register_print_hierarchy,
    0
};
