from myhdl import block, always_seq, always_comb, Signal, intbv

@block
def lif_calcium(param_ca_en, param_caleak,
                state_calcium, state_caleak_cnt, 
                spike_out, event_tref,
                state_calcium_next, state_caleak_cnt_next):
    ca_leak = Signal(bool(0))
    # v_up_next   = Signal(bool(0))#param_ca_en and (state_core_next >= param_thetamem) and (param_ca_theta1 <= state_calcium_next) and (state_calcium_next < param_ca_theta3)
    # v_down_next = Signal(bool(0))#param_ca_en and (state_core_next <  param_thetamem) and (param_ca_theta1 <= state_calcium_next) and (state_calcium_next < param_ca_theta2)

    @always_comb
    def update_calcium():
        if param_ca_en:
            if spike_out and not ca_leak and state_calcium == 0:
                state_calcium_next.next = state_calcium + 1
            elif ca_leak and not spike_out and state_calcium > 0:
                state_calcium_next.next = state_calcium - 1
            else:
                state_calcium_next.next = state_calcium
        else:
            state_calcium_next.next = state_calcium

    @always_comb
    def update_caleak():
        if param_ca_en and param_caleak > 0 and event_tref:
            if state_caleak_cnt == param_caleak - 1:
                state_caleak_cnt_next.next = 0
                ca_leak.next = True
            else:
                state_caleak_cnt_next.next = state_caleak_cnt + 1
                ca_leak.next = False
        else:
            state_caleak_cnt_next.next = state_caleak_cnt
            ca_leak.next = False

    return update_calcium, update_caleak
