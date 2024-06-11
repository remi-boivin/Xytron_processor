from myhdl import block, always_comb, instance, delay, Signal, intbv, Simulation, StopSimulation, concat
from os import sys, path

import pytest

from utils.setup_simulation import setup_lif_neuron_state
from src.LIF_neuron_blocks.lif_neuron_state import lif_neuron_state

class TestLifNeuronState:
    class TestEventLeak:
        def test_set_to_state_leak_state_core_next_i_if_event_leak_param_leak_en_activated(self, setup_lif_neuron_state):
            param_leak_str, param_leak_en, param_thr, state_core, event_leak, event_inh, event_exc, syn_weight, state_core_next, event_out, state_leak, state_inh, state_exc, spike_out, state_core_next_i, lif_neuron_state_inst = setup_lif_neuron_state

            # Define the simulation process
            @instance
            def stimulus():
                # Set initial conditions
                event_leak.next = 0b00000001  # Enable calcium
                param_leak_en.next = 0b00000001  # Set leakage parameter
                state_core.next = 0b00001001      # Simulate a spike event
                param_leak_str.next = 0b00000011
                param_thr.next = 0b00001001
                yield delay(10)  # Wait for 10 simulation steps
                state_leak = (state_core - concat(False, param_leak_str))
                # Create simulation
                assert state_core_next.next == state_leak, f"state_core_next_i should be eq to {state_leak} instead of {state_core_next}"

            sim = Simulation(lif_neuron_state_inst, stimulus)
            sim.run()

        # TODO: Test if when state_core eq state_leak state_core_next_i == state_leak
    
    class TestEventInh:

        def test_set_to_state_leak_state_core_next_i_if_event_inh_activated(self, setup_lif_neuron_state):
            param_leak_str, param_leak_en, param_thr, state_core, event_leak, event_inh, event_exc, syn_weight, state_core_next, event_out, state_leak, state_inh, state_exc, spike_out, state_core_next_i, lif_neuron_state_inst = setup_lif_neuron_state

            # Define the simulation process
            @instance
            def stimulus():
                # Set initial conditions
                event_inh.next = 0b00000001  # Enable calcium
                param_leak_en.next = 0b00000001  # Set leakage parameter
                state_core.next = 0b00001001      # Simulate a spike event
                param_leak_str.next = 0b00000011
                param_thr.next = 0b01000001
                syn_weight.next = 0b00000001
                yield delay(10)  # Wait for 10 simulation steps
                state_inh = state_core - concat(intbv(0)[5:], syn_weight)

                # Create simulation
                assert state_core_next.next == state_inh, f"state_core_next_i should be eq to {state_inh} instead of {state_core_next}"

            sim = Simulation(lif_neuron_state_inst, stimulus)
            sim.run()

        # TODO: Test if when state_core eq state_inh state_core_next_i == state_inh


    class TestEventExc:

        def test_set_to_state_leak_state_core_next_i_if_event_exc_activated(self, setup_lif_neuron_state):
            param_leak_str, param_leak_en, param_thr, state_core, event_leak, event_inh, event_exc, syn_weight, state_core_next, event_out, state_leak, state_inh, state_exc, spike_out, state_core_next_i, lif_neuron_state_inst = setup_lif_neuron_state

            # Define the simulation process
            @instance
            def stimulus():
                # Set initial conditions
                event_exc.next = 0b00000001  # Enable calcium
                param_leak_en.next = 0b00000001  # Set leakage parameter
                state_core.next = 0b00001001      # Simulate a spike event
                param_leak_str.next = 0b00000011
                param_thr.next = 0b01000001
                syn_weight.next = 0b00000001
                yield delay(10)  # Wait for 10 simulation steps
                state_exc = state_core + concat(intbv(0, min=-256, max=256)[5:], syn_weight)

                # Create simulation
                assert state_core_next.next == state_exc, f"state_core_next_i should be eq to {state_exc} instead of {state_core_next}"

            sim = Simulation(lif_neuron_state_inst, stimulus)
            sim.run()

        # TODO: Test if when state_core eq state_inh state_core_next_i == state_inh

    class TestCommonCases:

        def test_spike_out_state_core_next_eq_zero(self, setup_lif_neuron_state):
            param_leak_str, param_leak_en, param_thr, state_core, event_leak, event_inh, event_exc, syn_weight, state_core_next, event_out, state_leak, state_inh, state_exc, spike_out, state_core_next_i, lif_neuron_state_inst = setup_lif_neuron_state

            # Define the simulation process
            @instance
            def stimulus():
                # Set initial conditions
                event_leak.next = 0b00000001  # Enable calcium
                param_leak_en.next = 0b00000001  # Set leakage parameter
                state_core.next = 0b00001001      # Simulate a spike event
                param_leak_str.next = 0b00000011
                param_thr.next = 0b00000001
                yield delay(10)  # Wait for 10 simulation steps
                # Create simulation
                assert state_core_next.next == 0, f"state_core_next_i should be eq to 0 instead of {state_core_next}"

            sim = Simulation(lif_neuron_state_inst, stimulus)
            sim.run()

        def test_set_to_state_core_state_core_next(self, setup_lif_neuron_state):
            param_leak_str, param_leak_en, param_thr, state_core, event_leak, event_inh, event_exc, syn_weight, state_core_next, event_out, state_leak, state_inh, state_exc, spike_out, state_core_next_i, lif_neuron_state_inst = setup_lif_neuron_state

            # Define the simulation process
            @instance
            def stimulus():
                # Set initial conditions
                event_leak.next = 0b00000001  # Enable calcium
                param_leak_en.next = 0b00000000  # Set leakage parameter
                state_core.next = 0b00001001      # Simulate a spike event
                param_leak_str.next = 0b00000011
                param_thr.next = 0b01000001
                yield delay(10)  # Wait for 10 simulation steps
                state_leak = (state_core - concat(False, param_leak_str))
                # Create simulation
                assert state_core_next.next == state_core.next, f"state_core_next_i should be eq to {state_core.next} instead of {state_core_next}"

            sim = Simulation(lif_neuron_state_inst, stimulus)
            sim.run()
        
        # TODO: Test if event_out eq to spike_out