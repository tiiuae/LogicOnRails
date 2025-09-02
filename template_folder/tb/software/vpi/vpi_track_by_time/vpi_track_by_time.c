// vpi_track_by_time.c
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


// -----------------------------------------------------------------------------
// Callback that fires after each delay interval
static int cb_time_tick(p_cb_data cb_data)
{
    // 1) Get current simulation time
    s_vpi_time  cur_time = { .type = vpiSimTime };
    vpi_get_time(NULL, &cur_time);
    uint64_t now_ps = ((uint64_t)cur_time.high << 32) | cur_time.low;

    // 2) Read the watched signal’s value
    vpiHandle   obj = cb_data->obj;
    s_vpi_value val = { .format = vpiIntVal };
    vpi_get_value(obj, &val);

    // 3) Print time and value
    const char *name = vpi_get_str(vpiFullName, obj);
    vpi_printf("%sTRACK BY TIME%s : %s[time %0llu ps]%s %s -> %d\n", 
        ANSI_GREEN,ANSI_RESET,
        ANSI_BLUE,(unsigned long long)now_ps,ANSI_RESET, 
        name, 
        val.value.integer
    );

    // 4) Re‐schedule the same callback after the same interval
    //    We copy the cb_data struct (pointer fields only) so it lives on the heap
    p_cb_data next_cb = malloc(sizeof(*next_cb));
    *next_cb = *cb_data;     // shallow copy: copies obj, reason, time ptr, cb_rtn, user_data
    next_cb->value = NULL;   // not used for time callbacks
    vpi_register_cb(next_cb);

    return 0;
}

// -----------------------------------------------------------------------------
// $track(signal, delay) registration routine
static int track_calltf(char *userdata)
{
    // grab the two arguments from the SV call
    vpiHandle systf = vpi_handle(vpiSysTfCall, NULL);
    vpiHandle args  = vpi_iterate(vpiArgument, systf);
    vpiHandle sig_h = vpi_scan(args);
    vpiHandle t_h   = vpi_scan(args);

    // fetch the delay as a vpiTimeVal
    s_vpi_value tv = { .format = vpiTimeVal };
    vpi_get_value(t_h, &tv);

    // allocate and initialise the callback‐data
    p_cb_data cb = malloc(sizeof(*cb));
    cb->reason    = cbAfterDelay;     // fire after the given delay
    cb->obj       = sig_h;            // the signal handle
    cb->cb_rtn    = cb_time_tick;     // callback function
    cb->user_data = NULL;
    cb->time      = tv.value.time;    // reuse simulator’s time‐struct pointer
    cb->value     = NULL;             // unused for this kind of callback

    // print a quick confirmation
    uint64_t delay_ps = ((uint64_t)cb->time->high << 32) | cb->time->low;
    vpi_printf("%sVPI:%s registered %strack-by-time%s on %s, interval = %0llu ps\n",
               ANSI_YELLOW,ANSI_RESET,ANSI_BLUE,ANSI_RESET,
               vpi_get_str(vpiFullName, sig_h),
               (unsigned long long)delay_ps);

    // register the one‐shot; cb_time_tick will re‐register itself
    vpi_register_cb(cb);
    return 0;
}

// -----------------------------------------------------------------------------
// Tell the simulator about $track
void register_track_time()
{
    s_vpi_systf_data tf = {
        .type      = vpiSysTask,
        .tfname    = "$trackbytime",
        .calltf    = track_calltf,
        .compiletf = NULL,
        .sizetf    = NULL,
        .user_data = NULL
    };
    vpi_register_systf(&tf);
}

void xcelium_reg_vpi() {
    register_track_time();
}


// Hook into simulator startup
void (*vlog_startup_routines[])(void) = { register_track_time, 0 };
