// vpi_track.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "vpi_user.h"

#define ANSI_RED    "\x1B[31m"
#define ANSI_GREEN   "\x1B[32m"    // normal green
#define ANSI_GREEN_B "\x1B[92m"   // bright/high-intensity green
#define ANSI_YELLOW "\x1B[33m"
#define ANSI_BLUE   "\x1B[96m"
#define ANSI_RESET  "\x1B[0m"


// Callback runs on every value‐change of the watched object
static int cb_value_change(p_cb_data cb_data) {
    struct t_vpi_value val_s = { .format = vpiIntVal };
    struct t_vpi_time  time_s = { .type = vpiSimTime };
    vpiHandle          obj    = cb_data->obj;

    vpi_get_time(NULL, &time_s);
    vpi_get_value(obj, &val_s);

    uint64_t t = ((uint64_t)time_s.high << 32) | time_s.low;
    const char *name = vpi_get_str(vpiFullName, obj);

    // cast t to unsigned long long, use ASCII arrow “->”
    vpi_printf("%sTRACK BY VALUE%s : %s[time: %0llu ps]%s %s -> %d\n",
           ANSI_GREEN_B,ANSI_RESET,
           ANSI_BLUE,(unsigned long long)t,ANSI_RESET,
           name,
           val_s.value.integer);

    return 0;
}

// $track callTF: grabs the argument and registers the callback
static int track_calltf(char *userdata) {
    vpiHandle       systf   = vpi_handle(vpiSysTfCall, NULL);
    vpiHandle       args     = vpi_iterate(vpiArgument, systf);
    vpiHandle       sig_h    = vpi_scan(args);

    struct t_cb_data *cb_data = malloc(sizeof(*cb_data));
    cb_data->reason   = cbValueChange;
    cb_data->obj      = sig_h;
    cb_data->cb_rtn   = cb_value_change;
    
    s_vpi_value *value_s = malloc(sizeof(*value_s));
    value_s->format = vpiIntVal;    
    cb_data->value  = value_s;
    
    s_vpi_time *time_s = malloc(sizeof(*time_s));
    time_s->type  = vpiSimTime;     
    cb_data->time = time_s;

    cb_data->user_data = NULL;

    s_vpi_value value_i;
    value_i.format = vpiIntVal;           // integer value
    vpi_get_value(sig_h, &value_i);
    vpi_printf("%sVPI%s: registered %strack-by-value%s request on %s, init value %llx\n", 
        ANSI_YELLOW,ANSI_RESET,ANSI_BLUE,ANSI_RESET,
        vpi_get_str(vpiFullName, sig_h),
        (long long unsigned)value_i.value.integer
    );
    vpi_register_cb(cb_data);
    return 0;
}

// register $track as a system task
void register_track_value() {
    s_vpi_systf_data tf = {
        .type     = vpiSysTask,
        .tfname   = "$trackbyvalue",
        .calltf   = track_calltf,
        .compiletf= NULL,
        .sizetf   = NULL,
        .user_data= NULL
    };
    vpi_register_systf(&tf);
}

void xcelium_reg_vpi() {
    register_track_value();
}



// tell the simulator to run our registration at startup
void (*vlog_startup_routines[])(void) = { register_track_value, 0 };
