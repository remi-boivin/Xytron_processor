from myhdl import Signal, intbv
from os import sys

import pytest

sys.path.append("./")

from src.LIF_neuron_blocks.lif_neuron_state import lif_neuron_state
from src.LIF_neuron_blocks.lif_calcium import lif_calcium

import pytest
from myhdl import Signal, intbv

from src.LIF_neuron_blocks.lif_neuron_state import lif_neuron_state

@pytest.fixture
def setup_lif_neuron_state():
    param_leak_str = Signal(intbv(0, min=0, max=64))
    param_leak_en = Signal(bool(1))
    param_thr = Signal(intbv(0, min=0, max=256))
    state_core = Signal(intbv(0, min=-256, max=256))
    event_leak = Signal(bool(0))
    event_inh = Signal(bool(0))
    event_exc = Signal(bool(0))
    syn_weight = Signal(intbv(0, min=-4, max=4))
    state_core_next = Signal(intbv(0, min=-256, max=256))
    event_out = Signal(intbv(0, min=0, max=65))
    state_core_next_i = Signal(intbv(0, min=-256, max=256)) 
    state_leak = Signal(intbv(0, min=-256, max=256))
    state_inh = Signal(intbv(0, min=-256, max=256))
    state_exc = Signal(intbv(0, min=-256, max=256))
    spike_out = Signal(bool(0))
    
    lif_neuron_state_inst = lif_neuron_state(param_leak_str, param_leak_en, param_thr, state_core, event_leak, event_inh, event_exc, syn_weight, state_core_next, event_out)
    return (param_leak_str, param_leak_en, param_thr, state_core, event_leak, event_inh, event_exc, syn_weight, state_core_next, event_out, state_leak, state_inh, state_exc, spike_out, state_core_next_i, lif_neuron_state_inst)
@pytest.fixture
def setup_lif_calcium():
    param_ca_en = Signal(intbv(1))
    param_caleak = Signal(intbv(5)[5:])
    state_calcium = Signal(intbv(0)[3:])
    state_caleak_cnt = Signal(intbv(0)[5:])
    spike_out = Signal(bool(0))
    event_tref = Signal(bool(0))
    ca_leak = Signal(bool(0))
    state_calcium_next = Signal(intbv(0)[3:])
    state_caleak_cnt_next = Signal(intbv(0)[5:])
    state_caleak = Signal(intbv(0)[5:])
    lif_calcium_inst = lif_calcium(param_ca_en, param_caleak, state_calcium, state_caleak_cnt, spike_out, event_tref, state_calcium_next, state_caleak_cnt_next)
    return (param_ca_en, param_caleak, state_calcium, state_caleak_cnt, spike_out, event_tref, ca_leak, state_calcium_next, state_caleak_cnt_next, state_caleak, lif_calcium_inst)
