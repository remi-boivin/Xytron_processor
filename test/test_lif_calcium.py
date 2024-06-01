from myhdl import Signal, intbv, Simulation, delay, instance
from os import sys
import pytest

sys.path.append("./")

from src.LIF_neuron_blocks.lif_calcium import lif_calcium

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

def test_increase_state_calcium(setup_lif_calcium):
    param_ca_en, param_caleak, state_calcium, state_caleak_cnt, spike_out, event_tref, ca_leak, state_calcium_next, state_caleak_cnt_next, state_caleak, lif_calcium_inst = setup_lif_calcium

    # Define the simulation process
    @instance
    def stimulus():
        # Set initial conditions
        param_ca_en.next = 1  # Enable calcium
        param_caleak.next = 0  # Set leakage parameter
        spike_out.next = 1  # Simulate a spike event
        event_tref.next = 0  # No refractory event
        yield delay(10)  # Wait for 10 simulation steps
        assert spike_out == 1, "Spike out should be 1"
        assert state_calcium_next == 1, "State calcium next should be 1"
        # Create simulation
    sim = Simulation(lif_calcium_inst, stimulus)
    sim.run()

def test_decrease_calcium(setup_lif_calcium):
    param_ca_en, param_caleak, state_calcium, state_caleak_cnt, spike_out, event_tref, ca_leak, state_calcium_next, state_caleak_cnt_next, state_caleak, lif_calcium_inst = setup_lif_calcium

    # Define the simulation process
    @instance
    def stimulus():
        # Set initial conditions
        param_ca_en.next = 1
        param_caleak.next = 1
        event_tref.next = 1
        state_caleak_cnt.next = 0
        spike_out.next = 0
        state_calcium.next = 4
        yield delay(10)  # Wait for 10 simulation steps
        assert state_calcium_next == (state_calcium - 1), f"State calcium next should be eq to {state_calcium - 1}"

    sim = Simulation(lif_calcium_inst, stimulus)
    sim.run()

def test_calcium_unchanged(setup_lif_calcium):
    param_ca_en, param_caleak, state_calcium, state_caleak_cnt, spike_out, event_tref, ca_leak, state_calcium_next, state_caleak_cnt_next, state_caleak, lif_calcium_inst = setup_lif_calcium

    # Define the simulation process
    @instance
    def stimulus():
        # Set initial conditions
        param_ca_en.next = 1
        param_caleak.next = 5
        event_tref.next = 1
        spike_out.next = 0
        state_calcium.next = 4
        state_caleak.next = 23
        state_caleak_cnt_next = 0
        ca_leak = 0

        yield delay(10)  # Wait for 10 simulation steps
        assert state_calcium_next == state_calcium, f"State calcium next should be eq to {state_calcium}"

    sim = Simulation(lif_calcium_inst, stimulus)
    sim.run()

def test_no_param_ca_en(setup_lif_calcium):
    param_ca_en, param_caleak, state_calcium, state_caleak_cnt, spike_out, event_tref, ca_leak, state_calcium_next, state_caleak_cnt_next, state_caleak, lif_calcium_inst = setup_lif_calcium

    # Define the simulation process
    @instance
    def stimulus():
        # Set initial conditions
        param_ca_en.next = 0
        yield delay(10)  # Wait for 10 simulation steps
        assert state_calcium_next == state_calcium, f"State calcium next should be eq to {state_calcium}"

    sim = Simulation(lif_calcium_inst, stimulus)
    sim.run()

def test_set_state_caleak_cnt_next_zero(setup_lif_calcium):
    param_ca_en, param_caleak, state_calcium, state_caleak_cnt, spike_out, event_tref, ca_leak, state_calcium_next, state_caleak_cnt_next, state_caleak, lif_calcium_inst = setup_lif_calcium

    # Define the simulation process
    @instance
    def stimulus():
        # Set initial conditions
        param_ca_en.next = 1
        param_caleak.next = 23
        event_tref.next = 1
        spike_out.next = 0
        state_calcium.next = 0
        state_caleak.next = 22
        state_caleak_cnt.next = param_caleak.next - 1
        state_caleak_cnt_next.next = 3
        ca_leak.next = False
        yield delay(10)  # Wait for 10 simulation steps
        assert state_caleak_cnt_next == 0, f"state_caleak_count_next should be eq to 0"
    sim = Simulation(lif_calcium_inst, stimulus)
    sim.run()

def test_decrease_state_caleak_cnt(setup_lif_calcium):
    param_ca_en, param_caleak, state_calcium, state_caleak_cnt, spike_out, event_tref, ca_leak, state_calcium_next, state_caleak_cnt_next, state_caleak, lif_calcium_inst = setup_lif_calcium

    # Define the simulation process
    @instance
    def stimulus():
        # Set initial conditions
        param_ca_en.next = 1
        param_caleak.next = 1
        event_tref.next = 1
        spike_out.next = 0
        state_caleak_cnt.next = 20

        yield delay(10)  # Wait for 10 simulation steps
        assert state_caleak_cnt_next == state_caleak_cnt + 1
    sim = Simulation(lif_calcium_inst, stimulus)
    sim.run()

def test_state_caleak_cnt_no_param_ca_en(setup_lif_calcium):
    param_ca_en, param_caleak, state_calcium, state_caleak_cnt, spike_out, event_tref, ca_leak, state_calcium_next, state_caleak_cnt_next, state_caleak, lif_calcium_inst = setup_lif_calcium

    # Define the simulation process
    @instance
    def stimulus():
        # Set initial conditions
        param_ca_en.next = 0
        param_caleak.next = 1
        event_tref.next = 1
        spike_out.next = 0
        state_caleak_cnt.next = 20

        yield delay(10)  # Wait for 10 simulation steps
        assert state_caleak_cnt_next == state_caleak_cnt
    sim = Simulation(lif_calcium_inst, stimulus)
    sim.run()