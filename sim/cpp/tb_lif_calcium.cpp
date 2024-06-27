#include <fstream>
#include <iostream>
#include "Vlif_calcium.h" // Verilated module header
#include <verilated_vcd_c.h>

int failed_tests_cnt = 0;
int success_tests_cnt = 0;

void state_calcium_next_value_1(Vlif_calcium* top) {
// Setting inputs for the first scenario
    top->param_ca_en = 1;                // Enable calcium concentration
    top->param_caleak = 3;         // Calcium leakage strength parameter
    top->state_calcium = 0;          // Calcium concentration state from SRAM
    top->state_caleak_cnt = 0;     // Calcium leakage state from SRAM
    top->spike_out = 1;                   // Neuron spike event signal
    top->event_tref = 0;                  // Time reference event signal

    Verilated::traceEverOn(true);
    VerilatedVcdC *m_trace = new VerilatedVcdC;
    top->trace(m_trace, 99);
    m_trace->open("waveform.vcd");

    top->eval();

    // Define expected output values for each clock cycle
    int expected_state_calcium_next = 0;

    // Run simulation for multiple clock cycles
    for (int i = 0; i < 10; ++i) {
        expected_state_calcium_next = top->state_calcium + 1;
        m_trace->dump(top->state_calcium_next);
        m_trace->dump(top->state_calcium);
        if (top->state_calcium_next != expected_state_calcium_next) {
            std::cout << "state_calcium_next_value_1 \033[31m KO\033[00m" << std::endl;
            std::cerr << "\033[31m=================================================================== FAILURE =========================================================================\033[00m" << std::endl;
            std::cerr << "Error: state_calcium_next does not match expected value:" << std::endl;
            if (!top->state_calcium_next)
                std::cerr << "\033[32m + Expected Value: " << expected_state_calcium_next << std::endl << "\033[31m - Actual value: None \033[00m" << std::endl;
            else
                std::cerr << "\033[32m + Expected Value: " << expected_state_calcium_next << std::endl << "\033[31m - Actual value: " << top->state_calcium_next << "\033[00m" << std::endl;
            failed_tests_cnt++;
            return;
        }
    }
    m_trace->close();
delete m_trace;
    success_tests_cnt++;
    std::cout << "state_calcium_next_value_1: \033[32mOK\033[00m" << std::endl;
}

void state_calcium_next_value_2(Vlif_calcium* top) {
    // Setting inputs for the scenario
    top->param_ca_en = 1;
    top->param_caleak = 1;
    top->event_tref = 1; // This will cause ca_leak to be set if state_caleak_cnt == (param_caleak - 1)
    top->state_caleak_cnt = 0;
    // top->param_thetamem = 0;
    // top->param_ca_theta1 = 0;
    // top->param_ca_theta2 = 0;
    // top->param_ca_theta3 = 0;
    // top->state_core_next = 0;
    
    // Test the condition where ca_leak && ~spike_out && |state_calcium
    top->spike_out = 0;
    top->state_calcium = 4; // non-zero value

    top->eval();

    // Define expected output values for each clock cycle
    int expected_state_calcium_next = 0;

    // Run simulation for multiple clock cycles
    for (int i = 0; i < 10; ++i) {
        expected_state_calcium_next = top->state_calcium - 0b001;

        if (top->state_calcium_next != expected_state_calcium_next) {
            std::cout << "state_calcium_next_value_2 \033[31m KO\033[00m" << std::endl;
            std::cerr << "\033[31m=================================================================== FAILURE =========================================================================\033[00m" << std::endl;
            std::cerr << "Error: state_calcium_next does not match expected value:" << std::endl;
            if (!top->state_calcium_next)
                std::cerr << "\033[32m + Expected Value: " << expected_state_calcium_next << std::endl << "\033[31m - Actual value: None \033[00m" << std::endl;
            else
                std::cerr << "\033[32m + Expected Value: " << expected_state_calcium_next << std::endl << "\033[31m - Actual value: " << top->state_calcium_next << "\033[00m" << std::endl;
            failed_tests_cnt++;
            return;
        }
    }
    success_tests_cnt++;
    std::cout << "state_calcium_next_value_2: \033[32mOK\033[00m" << std::endl;
}

void state_calcium_next_value_3(Vlif_calcium* top) {
    // Setting inputs for the scenario
    top->param_ca_en = 1;
    top->param_caleak = 1;
    top->event_tref = 1; // This will cause ca_leak to be set if state_caleak_cnt == (param_caleak - 1)
    top->state_caleak_cnt = 0;
    // top->param_thetamem = 0;
    // top->param_ca_theta1 = 0;
    // top->param_ca_theta2 = 0;
    // top->param_ca_theta3 = 0;
    // top->state_core_next = 0;
    
    // Test the condition where ca_leak && ~spike_out && |state_calcium
    top->spike_out = 1;
    top->state_calcium = 0; // non-zero value

    top->eval();

    // Define expected output values for each clock cycle
    int expected_state_calcium_next = 0;

    // Run simulation for multiple clock cycles
    for (int i = 0; i < 10; ++i) {
        expected_state_calcium_next = top->state_calcium;

        if (top->state_calcium_next != expected_state_calcium_next) {
            std::cout << "state_calcium_next_value_3 \033[31m KO\033[00m" << std::endl;
            std::cerr << "\033[31m=================================================================== FAILURE =========================================================================\033[00m" << std::endl;
            std::cerr << "Error: state_calcium_next does not match expected value:" << std::endl;
            if (!top->state_calcium_next)
                std::cerr << "\033[32m + Expected Value: " << expected_state_calcium_next << std::endl << "\033[31m - Actual value: None \033[00m" << std::endl;
            else
                std::cerr << "\033[32m + Expected Value: " << expected_state_calcium_next << std::endl << "\033[31m - Actual value: " << top->state_calcium_next << "\033[00m" << std::endl;
            failed_tests_cnt++;
            return;
        }
    }
    success_tests_cnt++;
    std::cout << "state_calcium_next_value_3: \033[32mOK\033[00m" << std::endl;
}

void state_calcium_next_value_4(Vlif_calcium* top) {
    // Setting inputs for the scenario
    top->param_ca_en = 0;
    top->param_caleak = 0;
    top->event_tref = 0; // This will cause ca_leak to be set if state_caleak_cnt == (param_caleak - 1)
    top->state_caleak_cnt = 0;
    // top->param_thetamem = 0;
    // top->param_ca_theta1 = 0;
    // top->param_ca_theta2 = 0;
    // top->param_ca_theta3 = 0;
    // top->state_core_next = 0;
    
    // Test the condition where ca_leak && ~spike_out && |state_calcium
    top->spike_out = 0;
    top->state_calcium = 0; // non-zero value

    top->eval();

    // Define expected output values for each clock cycle
    int expected_state_calcium_next = 0;

    // Run simulation for multiple clock cycles
    for (int i = 0; i < 10; ++i) {
        expected_state_calcium_next = top->state_calcium;

        if (top->state_calcium_next != expected_state_calcium_next) {
            std::cout << "state_calcium_next_value_4 \033[31m KO\033[00m" << std::endl;
            std::cerr << "\033[31m=================================================================== FAILURE =========================================================================\033[00m" << std::endl;
            std::cerr << "Error: state_calcium_next does not match expected value:" << std::endl;
            if (!top->state_calcium_next)
                std::cerr << "\033[32m + Expected Value: " << expected_state_calcium_next << std::endl << "\033[31m - Actual value: None \033[00m" << std::endl;
            else
                std::cerr << "\033[32m + Expected Value: " << expected_state_calcium_next << std::endl << "\033[31m - Actual value: " << top->state_calcium_next << "\033[00m" << std::endl;
            failed_tests_cnt++;
            return;
        }
    }
    success_tests_cnt++;
    std::cout << "state_calcium_next_value_4: \033[32mOK\033[00m" << std::endl;
}

void state_caleak_cnt_next_1(Vlif_calcium* top) {
    // Setting inputs for the scenario
    top->param_ca_en = 1;
    top->param_caleak = 1;
    top->event_tref = 1;
    top->state_caleak_cnt = top->param_caleak - 1;
    // top->param_thetamem = 0;
    // top->param_ca_theta1 = 0;
    // top->param_ca_theta2 = 0;
    // top->param_ca_theta3 = 0;
    // top->state_core_next = 0;
    
    // Test the condition where ca_leak && ~spike_out && |state_calcium
    top->spike_out = 0;
    top->state_calcium = 0; // non-zero value

    top->eval();

    // Define expected output values for each clock cycle
    int expected_state_caleak_cnt_next = 0;

    // Run simulation for multiple clock cycles
    for (int i = 0; i < 10; ++i) {
        expected_state_caleak_cnt_next = 0;

        if (top->state_caleak_cnt_next != expected_state_caleak_cnt_next) {
            std::cout << "state_caleak_cnt_next_1 \033[31m KO\033[00m" << std::endl;
            std::cerr << "\033[31m=================================================================== FAILURE =========================================================================\033[00m" << std::endl;
            std::cerr << "Error: state_caleak_cnt_next does not match expected value:" << std::endl;
            if (!top->state_caleak_cnt_next)
                std::cerr << "\033[32m + Expected Value: " << expected_state_caleak_cnt_next << std::endl << "\033[31m - Actual value: None \033[00m" << std::endl;
            else
                std::cerr << "\033[32m + Expected Value: " << expected_state_caleak_cnt_next << std::endl << "\033[31m - Actual value: " << top->state_caleak_cnt_next << "\033[00m" << std::endl;
            failed_tests_cnt++;
            return;
        }
    }
    success_tests_cnt++;
    std::cout << "state_caleak_cnt_next_1: \033[32mOK\033[00m" << std::endl;
}

void state_caleak_cnt_next_2(Vlif_calcium* top) {
    // Setting inputs for the scenario
    top->param_ca_en = 0;
    top->param_caleak = 0;
    top->event_tref = 0;
    top->state_caleak_cnt = 0;
    // top->param_thetamem = 0;
    // top->param_ca_theta1 = 0;
    // top->param_ca_theta2 = 0;
    // top->param_ca_theta3 = 0;
    // top->state_core_next = 0;

    // Test the condition where ca_leak && ~spike_out && |state_calcium
    top->spike_out = 0;
    top->state_calcium = 0; // non-zero value

    top->eval();

    // Define expected output values for each clock cycle
    int expected_state_caleak_cnt_next = 0;

    // Run simulation for multiple clock cycles
    for (int i = 0; i < 10; ++i) {
        expected_state_caleak_cnt_next = top->state_caleak_cnt;

        if (top->state_caleak_cnt_next != expected_state_caleak_cnt_next) {
            std::cout << "state_caleak_cnt_next_2 \033[31m KO\033[00m" << std::endl;
            std::cerr << "\033[31m=================================================================== FAILURE =========================================================================\033[00m" << std::endl;
            std::cerr << "Error: state_caleak_cnt_next does not match expected value:" << std::endl;
            if (!top->state_caleak_cnt_next)
                std::cerr << "\033[32m + Expected Value: " << expected_state_caleak_cnt_next << std::endl << "\033[31m - Actual value: None \033[00m" << std::endl;
            else
                std::cerr << "\033[32m + Expected Value: " << expected_state_caleak_cnt_next << std::endl << "\033[31m - Actual value: " << top->state_caleak_cnt_next << "\033[00m" << std::endl;
            failed_tests_cnt++;
            return;
        }
    }
    success_tests_cnt++;
    std::cout << "state_caleak_cnt_next_2: \033[32mOK\033[00m" << std::endl;
}

void state_caleak_cnt_next_3(Vlif_calcium* top) {
    // Setting inputs for the scenario
    top->param_ca_en = 1;
    top->param_caleak = 1;
    top->event_tref = 1;
    top->state_caleak_cnt = 20;
    // top->param_thetamem = 0;
    // top->param_ca_theta1 = 0;
    // top->param_ca_theta2 = 0;
    // top->param_ca_theta3 = 0;
    // top->state_core_next = 0;
    
    // Test the condition where ca_leak && ~spike_out && |state_calcium
    top->spike_out = 0;
    top->state_calcium = 0; // non-zero value

    top->eval();

    // Define expected output values for each clock cycle
    int expected_state_caleak_cnt_next = 0;

    // Run simulation for multiple clock cycles
    for (int i = 0; i < 10; ++i) {
        expected_state_caleak_cnt_next = top->state_caleak_cnt + 1;

        if (top->state_caleak_cnt_next != expected_state_caleak_cnt_next) {
            std::cout << "state_caleak_cnt_next_3 \033[31m KO\033[00m" << std::endl;
            std::cerr << "\033[31m=================================================================== FAILURE =========================================================================\033[00m" << std::endl;
            std::cerr << "Error: state_caleak_cnt_next does not match expected value:" << std::endl;
            if (!top->state_caleak_cnt_next)
                std::cerr << "\033[32m + Expected Value: " << expected_state_caleak_cnt_next << std::endl << "\033[31m - Actual value: None \033[00m" << std::endl;
            else
                std::cerr << "\033[32m + Expected Value: " << expected_state_caleak_cnt_next << std::endl << "\033[31m - Actual value: " << top->state_caleak_cnt_next << "\033[00m" << std::endl;
            failed_tests_cnt++;
            return;
        }
    }
    success_tests_cnt++;
    std::cout << "state_caleak_cnt_next_3: \033[32mOK\033[00m" << std::endl;
}

int main() {
    // Instantiate the Verilated module
    Vlif_calcium* top = new Vlif_calcium;

    std::system("verilator --version > test.txt");
    std::system("uname -rs > test1.txt");
    std::system("pwd > test2.txt");
    std::ifstream f("test.txt");
    std::ifstream f1("test1.txt");
    std::ifstream f2("test2.txt");
    std::string line;
    std::string platform;
    std::string pwd;
    std::getline(f, line);
    std::getline(f1, platform);
    std::getline(f2, pwd);

    std::cout << "\033[1mTest session start (Platform " << platform << ", C++ 17, " << line << ") \033[00m" << std::endl;
    std::cout << "rootdir: " << pwd << " , testpaths: sim/cpp" << std::endl;
    std::cout << "\033[1mcollecting ...\033[00m" << std::endl;

    state_calcium_next_value_1(top);
    state_calcium_next_value_2(top);
    state_calcium_next_value_3(top);
    state_calcium_next_value_4(top);
    state_caleak_cnt_next_1(top);
    state_caleak_cnt_next_2(top);
    state_caleak_cnt_next_3(top);

    std::cout << std::endl << "Results:" << std::endl;

    if (failed_tests_cnt == 0) {
        std::cout << "\033[32m\tSuccess all tests passed \033[00m" << std::endl;
    } else {
        success_tests_cnt == 0 ? std::cout << "\033[31m\t" << failed_tests_cnt << " failed" << "\033[32m" << std::endl :  std::cout << "\t\033[32m"<< success_tests_cnt << " passed\033[00m" << std::endl << "\033[31m\t" << failed_tests_cnt << " failed" << "\033[32m" << std::endl;
    }
    // Delete the Verilated module
    delete top;

    return 0;
}
