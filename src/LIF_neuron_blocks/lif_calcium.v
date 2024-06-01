// Copyright (C) 2016-2019 Université catholique de Louvain (UCLouvain), Belgium.
// Copyright and related rights are licensed under the Solderpad Hardware
// License, Version 2.0 (the "License"); you may not use this file except in
// compliance with the License.  You may obtain a copy of the License at
// http://solderpad.org/licenses/SHL-2.0/. The software, hardware and materials
// distributed under this License are provided in the hope that it will be useful
// on an as is basis, without warranties or conditions of any kind, either
// expressed or implied; without even the implied warranty of merchantability or
// fitness for a particular purpose. See the Solderpad Hardware License for more
// detailed permissions and limitations.
//------------------------------------------------------------------------------
//
// "lif_calcium.v" - ODIN leaky integrate-and-fire (LIF) neuron update logic (Calcium part)
// 
// Project: ODIN - An online-learning digital spiking neuromorphic processor
//
// Author:  C. Frenkel, Université catholique de Louvain (UCLouvain), 04/2017
//
// Cite/paper: C. Frenkel, M. Lefebvre, J.-D. Legat and D. Bol, "A 0.086-mm² 12.7-pJ/SOP 64k-Synapse 256-Neuron Online-Learning
//             Digital Spiking Neuromorphic Processor in 28-nm CMOS," IEEE Transactions on Biomedical Circuits and Systems,
//             vol. 13, no. 1, pp. 145-158, 2019.
//
//------------------------------------------------------------------------------

//------------------------------------------------------------------------------
// "lif_calcium.v" - ODIN leaky integrate-and-fire (LIF) neuron update logic (Calcium part)
//
// Project: ODIN - An online-learning digital spiking neuromorphic processor
//
// Author:  C. Frenkel, Université catholique de Louvain (UCLouvain), 04/2017
//
//------------------------------------------------------------------------------

module lif_calcium (
    input  wire                 param_ca_en,             // calcium concentration enable parameter
    input  wire [7:0]           param_thetamem,          // membrane threshold parameter
    input  wire [2:0]           param_ca_theta1,         // calcium threshold 1 parameter
    input  wire [2:0]           param_ca_theta2,         // calcium threshold 2 parameter
    input  wire [2:0]           param_ca_theta3,         // calcium threshold 3 parameter
    input  wire [4:0]           param_caleak,            // calcium leakage strength parameter
    input  wire [2:0]           state_calcium,           // calcium concentration state from SRAM
    input  wire [4:0]           state_caleak_cnt,        // calcium leakage state from SRAM
    input  wire [7:0]           state_core_next,         // next membrane potential state to SRAM
    input  wire                 spike_out,               // neuron spike event signal
    input  wire                 event_tref,              // time reference event signal
    output reg  [2:0]           state_calcium_next,      // next calcium concentration state to SRAM
    output reg  [4:0]           state_caleak_cnt_next    // next calcium leakage state to SRAM
);

    reg ca_leak;

    always @(*) begin 
        if (param_ca_en) begin
            if (spike_out && ~ca_leak && state_calcium != 3'b111)
                state_calcium_next = state_calcium + 3'b1;
            else if (ca_leak && ~spike_out && state_calcium != 3'b000)
                state_calcium_next = state_calcium - 3'b1;
            else
                state_calcium_next = state_calcium;
        end else begin
            state_calcium_next = state_calcium;
        end
    end

    always @(*) begin 
        if (param_ca_en && param_caleak != 5'b00000 && event_tref) begin
            if (state_caleak_cnt == (param_caleak - 5'b1)) begin
                state_caleak_cnt_next = 5'b0;
                ca_leak = 1'b1;
            end else begin
                state_caleak_cnt_next = state_caleak_cnt + 5'b1;
                ca_leak = 1'b0;
            end
        end else begin
            state_caleak_cnt_next = state_caleak_cnt;
            ca_leak = 1'b0;
        end
    end

endmodule
