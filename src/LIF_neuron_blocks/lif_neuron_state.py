from myhdl import block, always_comb, Signal, intbv, concat

@block
def lif_neuron_state(param_leak_str, param_leak_en, param_thr, state_core,
                     event_leak, event_inh, event_exc, syn_weight,
                     state_core_next, event_out):
    state_core_next_i = Signal(intbv(0, min=-256, max=256))
    state_leak = Signal(intbv(0, min=-256, max=256))
    state_inh = Signal(intbv(0, min=-256, max=256))
    state_exc = Signal(intbv(0, min=-256, max=256))
    spike_out = Signal(bool(0))

    @always_comb
    def comb_logic():
        spike_out.next = (state_core_next_i >= param_thr)
        event_out.next = concat(spike_out, intbv(0)[6:])
        state_core_next.next = 0 if spike_out else state_core_next_i

        state_leak.next = state_core - concat(False, param_leak_str)
        state_inh.next = state_core - concat(intbv(0, min=-256, max=256)[5:], syn_weight)
        state_exc.next = state_core + concat(intbv(0, min=-256, max=256)[5:], syn_weight)

    @always_comb
    def update_core():
        if event_leak and param_leak_en:
            state_core_next_i.next = state_leak if state_core >= state_leak else 0b00000000
        elif event_inh:
            state_core_next_i.next = state_inh if state_core >= state_inh else 0b00000000
        elif event_exc:
            state_core_next_i.next = state_exc if state_core <= state_exc else 0xFF
        else:
            state_core_next_i.next = state_core

    return update_core, comb_logic