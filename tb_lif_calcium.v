module tb_lif_calcium;

reg param_ca_en;
reg [4:0] param_caleak;
reg [2:0] state_calcium;
reg [4:0] state_caleak_cnt;
reg spike_out;
reg event_tref;
wire [2:0] state_calcium_next;
wire [4:0] state_caleak_cnt_next;

initial begin
    $from_myhdl(
        param_ca_en,
        param_caleak,
        state_calcium,
        state_caleak_cnt,
        spike_out,
        event_tref
    );
    $to_myhdl(
        state_calcium_next,
        state_caleak_cnt_next
    );
end

lif_calcium dut(
    param_ca_en,
    param_caleak,
    state_calcium,
    state_caleak_cnt,
    spike_out,
    event_tref,
    state_calcium_next,
    state_caleak_cnt_next
);

endmodule
