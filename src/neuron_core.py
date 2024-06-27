from myhdl import block, always_seq, always_comb, Signal, intbv, modbv, concat

@block
def SRAM_256x128_wrapper(rstn, clock_sig, chip_select_signal, write_enable_signal,
                        address_input, data_input, data_output):
    """
    @brief A 256x128 SRAM wrapper in MyHDL.
    @param rstn Asynchronous reset signal.
    @param clock_sig Clock signal.
    @param chip_select_signal Chip select signal.
    @param write_enable_signal Write enable signal.
    @param address_input Address input.
    @param data_input Data input.
    @param data_output Data output.
    """
    SRAM = [Signal(intbv(0)[128:]) for _ in range(256)]
    Qr = Signal(intbv(0)[128:])

    @always_seq(CK.posedge, reset=rstn)
    def sram_logic():
        """
        @brief Sequential logic for SRAM read/write operations.
        """
        if chip_select_signal:
            Qr.next = SRAM[int(A)]
            if write_enable_signal:
                SRAM[int(A)].next = D

    @always_comb
    def assign_data_output():
        """
        @brief Combinational logic to assign output data_output.
        """
        data_output.next = Qr

    return sram_logic, assign_data_output

@block
def neuron_core(RSTN_syncn, CLK, SPI_GATE_ACTIVITY_sync, SPI_PROPAGATE_UNMAPPED_SYN,
                SYNARRAY_RDATA, SYN_SIGN, CTRL_NEUR_EVENT, CTRL_NEUR_TREF, 
                CTRL_NEUR_VIRTS, CTRL_NEURMEM_CS, CTRL_NEURMEM_WE, CTRL_NEURMEM_ADDR,
                CTRL_PROG_DATA, CTRL_SPI_ADDR, CTRL_NEUR_BURST_END, NEUR_STATE,
                NEUR_EVENT_OUT, NEUR_V_UP, NEUR_V_DOWN, NEUR_STATE_MONITOR
):
    neur_rstn = Signal(intbv(0, min=-256, max=256))
    syn_weight = Signal(intbv(0, min=-256, max=256)[2:])
    syn_weight_int = Signal(intbv(0, min=-256, max=256)[31:])
    syn_sign  = Signal(intbv(0, min=-256, max=256))
    syn_event = Signal(intbv(0, min=-256, max=256))
    time_ref = Signal(intbv(0, min=-256, max=256))
    
    LIF_neuron_v_up_next = Signal(intbv(0, min=-256, max=256))
    IZH_neuron_v_up_next = Signal(intbv(0, min=-256, max=256))
    LIF_neuron_v_down_next = Signal(intbv(0, min=-256, max=256))
    IZH_neuron_v_down_next = Signal(intbv(0, min=-256, max=256))

    LIF_neuron_event_out = Signal(intbv(0, min=-256, max=256)[:6])
    IZH_neuron_event_out = Signal(intbv(0, min=-256, max=256)[6:])
    
    LIF_neuron_next_NEUR_STATE = Signal(intbv(0, min=-256, max=256)[15:])
    IZH_neuron_next_NEUR_STATE = Signal(intbv(0, min=-256, max=256)[54:])
    
    neuron_data_int = Signal(intbv(0, min=-256, max=256)[54:])
    neuron_data =Signal(intbv(0, min=-256, max=256)[54:])
    
    i = 0;

    @block
    def process_inputs(
        SYNARRAY_RDATA,
        CTRL_NEURMEM_ADDR,
        CTRL_NEUR_VIRTS,
        SPI_PROPAGATE_UNMAPPED_SYN,
        SYN_SIGN,
        CTRL_NEUR_EVENT,
        CTRL_NEUR_TREF,
        syn_weight_int,
        syn_weight,
        syn_sign,
        syn_event,
        time_ref
    ):
        @always_comb
        def logic():
            syn_weight_int.next = SYNARRAY_RDATA >> concat(0, CTRL_NEURMEM_ADDR[2:0]) << 2
            syn_weight.next = CTRL_NEUR_VIRTS[4:2] if CTRL_NEUR_VIRTS else (syn_weight_int[2:0] & concat(syn_weight_int[3], SPI_PROPAGATE_UNMAPPED_SYN))
            syn_sign.next = CTRL_NEUR_VIRTS[1] if CTRL_NEUR_VIRTS else SYN_SIGN
            syn_event.next = CTRL_NEUR_EVENT
            time_ref.next = CTRL_NEUR_VIRTS[0] if CTRL_NEUR_VIRTS else CTRL_NEUR_TREF

        return logic
    # Instantiate SRAM wrapper
    # sram_inst = SRAM_256x128_wrapper(
    #     rstn, clock_sig, chip_select_signal=Signal(bool(1)), write_enable_signal=sram_write_enable_sig, addr_in=sram_addr_in, 
    #     data_in=sram_data_in, data_out=sram_data_out
    # )

    # # Instantiate lif neuron
    # lif_neuron_inst = lif_neuron(
    #     param_leak_str=Signal(intbv(0)[16:]), param_leak_en=Signal(bool(0)), 
    #     param_thr=Signal(intbv(0)[16:]), param_ca_en=Signal(bool(0)), 
    #     param_thetamem=Signal(intbv(0)[16:]), param_ca_theta1=Signal(intbv(0)[16:]), 
    #     param_ca_theta2=Signal(intbv(0)[16:]), param_ca_theta3=Signal(intbv(0)[16:]), 
    #     param_caleak=Signal(intbv(0)[16:]), state_core=lif_neuron_state_core, 
    #     state_core_next=lif_neuron_state_core_next, state_calcium=Signal(intbv(0)[16:]), 
    #     state_calcium_next=Signal(intbv(0)[16:]), state_caleak_cnt=Signal(intbv(0)[16:]), 
    #     state_caleak_cnt_next=Signal(intbv(0)[16:]), syn_weight=Signal(intbv(0)[16:]), 
    #     syn_sign=Signal(bool(0)), syn_event=Signal(bool(0)), time_ref=Signal(intbv(0)[16:]), 
    #     v_up_next=lif_neuron_v_up_next, v_down_next=lif_neuron_v_down_next, event_out=lif_neuron_event_out
    # )

    # # Instantiate izh neuron
    # izh_neuron_inst = izh_neuron(
    #     param_leak_str=Signal(intbv(0)[16:]), param_leak_en=Signal(bool(0)), 
    #     param_fi_sel=Signal(intbv(0)[16:]), param_spk_ref=Signal(intbv(0)[16:]), 
    #     param_isi_ref=Signal(intbv(0)[16:]), param_reson_sharp_en=Signal(bool(0)), 
    #     param_thr=Signal(intbv(0)[16:]), param_rfr=Signal(intbv(0)[16:]), 
    #     param_dapdel=Signal(intbv(0)[16:]), param_spklat_en=Signal(bool(0)), 
    #     param_dap_en=Signal(bool(0)), param_stim_thr=Signal(intbv(0)[16:]), 
    #     param_phasic_en=Signal(bool(0)), param_mixed_en=Signal(bool(0)), 
    #     param_class2_en=Signal(bool(0)), param_neg_en=Signal(bool(0)), 
    #     param_rebound_en=Signal(bool(0)), param_inhin_en=Signal(bool(0)), 
    #     param_bist_en=Signal(bool(0)), param_reson_en=Signal(bool(0)), 
    #     param_thrvar_en=Signal(bool(0)), param_thr_sel_of=Signal(intbv(0)[16:]), 
    #     param_thrleak=Signal(intbv(0)[16:]), param_acc_en=Signal(bool(0)), 
    #     param_ca_en=Signal(bool(0)), param_thetamem=Signal(intbv(0)[16:]), 
    #     param_ca_theta1=Signal(intbv(0)[16:]), param_ca_theta2=Signal(intbv(0)[16:]), 
    #     param_ca_theta3=Signal(intbv(0)[16:]), param_caleak=Signal(intbv(0)[16:]), 
    #     param_burst_incr=Signal(intbv(0)[16:]), param_reson_sharp_amt=Signal(intbv(0)[16:]), 
    #     state_inacc=Signal(intbv(0)[16:]), state_inacc_next=Signal(intbv(0)[16:]), 
    #     state_refrac=Signal(intbv(0)[16:]), state_refrac_next=Signal(intbv(0)[16:]), 
    #     state_core=izh_neuron_state_core, state_core_next=izh_neuron_state_core_next, 
    #     state_dapdel_cnt=Signal(intbv(0)[16:]), state_dapdel_cnt_next=Signal(intbv(0)[16:]), 
    #     state_stim_str=Signal(intbv(0)[16:]), state_stim_str_next=Signal(intbv(0)[16:]), 
    #     state_stim_str_tmp=Signal(intbv(0)[16:]), state_stim_str_tmp_next=Signal(intbv(0)[16:]), 
    #     state_phasic_lock=Signal(intbv(0)[16:]), state_phasic_lock_next=Signal(intbv(0)[16:]), 
    #     state_mixed_lock=Signal(intbv(0)[16:]), state_mixed_lock_next=Signal(intbv(0)[16:]), 
    #     state_spkout_done=Signal(intbv(0)[16:]), state_spkout_done_next=Signal(intbv(0)[16:]), 
    #     state_stim0_prev=Signal(intbv(0)[16:]), state_stim0_prev_next=Signal(intbv(0)[16:]), 
    #     state_inhexc_prev=Signal(intbv(0)[16:]), state_inhexc_prev_next=Signal(intbv(0)[16:]), 
    #     state_bist_lock=Signal(intbv(0)[16:]), state_bist_lock_next=Signal(intbv(0)[16:]), 
    #     state_inhin_lock=Signal(intbv(0)[16:]), state_inhin_lock_next=Signal(intbv(0)[16:]), 
    #     state_reson_sign=Signal(intbv(0)[16:]), state_reson_sign_next=Signal(intbv(0)[16:]), 
    #     state_thrmod=Signal(intbv(0)[16:]), state_thrmod_next=Signal(intbv(0)[16:]), 
    #     state_thrleak_cnt=Signal(intbv(0)[16:]), state_thrleak_cnt_next=Signal(intbv(0)[16:]), 
    #     state_calcium=Signal(intbv(0)[16:]), state_calcium_next=Signal(intbv(0)[16:]), 
    #     state_caleak_cnt=Signal(intbv(0)[16:]), state_caleak_cnt_next=Signal(intbv(0)[16:]), 
    #     state_burst_lock=Signal(intbv(0)[16:]), state_burst_lock_next=Signal(intbv(0)[16:]), 
    #     syn_weight=Signal(intbv(0)[16:]), syn_sign=Signal(bool(0)), syn_event=Signal(bool(0)), 
    #     time_ref=Signal(intbv(0)[16:]), burst_end=Signal(bool(0)), v_up_next=izh_neuron_v_up_next, 
    #     v_down_next=izh_neuron_v_down_next, event_out=izh_neuron_event_out
    # )

    # @always_comb
    # def process_inputs():
    #     """
    #     @brief Process input signals and select neuron type.
    #     """
    #     if neur_type == neur_izh:
    #         izh_neuron_state_core.next = neur_event_in_sig
    #     elif neur_type == neur_lif:
    #         lif_neuron_state_core.next = neur_event_in_sig

    # @always_comb
    # def generate_outputs():
    #     """
    #     @brief Generate output signals based on neuron type.
    #     """
    #     if neur_type == neur_izh:
    #         neur_event_out.next = izh_neuron_event_out
    #     elif neur_type == neur_lif:
    #         neur_event_out.next = lif_neuron_event_out

    # return sram_inst, lif_neuron_inst, izh_neuron_inst, process_inputs, generate_outputs