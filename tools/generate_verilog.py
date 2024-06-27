from myhdl import block, always_comb, Signal, intbv
from os import sys
sys.path.append("./")

from src.LIF_neuron_blocks.lif_calcium import lif_calcium

def convert_myhdl_module(module, *args):
    """
    Convert a MyHDL module to Verilog and VHDL.

    Parameters:
    module : function
        The MyHDL module to be converted.
    *args : list
        The arguments to be passed to the MyHDL module.
    """
    # Convert to Verilog
    module(*args).convert(hdl='Verilog')
    # Convert to VHDL
    module(*args).convert(hdl='VHDL')

# Example usage with the lif_calcium module

# Define signals for the lif_calcium module
param_ca_en = Signal(bool(1))
# param_thetamem = Signal(intbv(128)[8:])
# param_ca_theta1 = Signal(intbv(3)[3:])
# param_ca_theta2 = Signal(intbv(6)[3:])
# param_ca_theta3 = Signal(intbv(7)[3:])
param_caleak = Signal(intbv(5)[5:])
state_calcium = Signal(intbv(0)[3:])
state_caleak_cnt = Signal(intbv(0)[5:])
# state_core_next = Signal(intbv(100)[8:])
spike_out = Signal(bool(0))
event_tref = Signal(bool(0))
# v_up_next = Signal(bool(0))
# v_down_next = Signal(bool(0))
state_calcium_next = Signal(intbv(0)[3:])
state_caleak_cnt_next = Signal(intbv(0)[5:])

# Convert the lif_calcium module to Verilog and VHDL using the generic function
convert_myhdl_module(lif_calcium, param_ca_en, param_caleak, state_calcium,
                     state_caleak_cnt,  spike_out, event_tref,
                     state_calcium_next, state_caleak_cnt_next)

# def import_python_files_from_directory(directory):
#     """
#     Import all Python files in the specified directory.
#     """
#     for filename in os.listdir(directory):
#         if filename.endswith(".py") and not filename.startswith("__"):
#             # Create module name from filename
#             module_name = filename[:-3]
#             # Create full module path
#             module_path = os.path.join(directory, filename)
#             # Import module dynamically
#             spec = importlib.util.spec_from_file_location(module_name, module_path)
#             module = importlib.util.module_from_spec(spec)
#             convert_myhdl_module(module, param_ca_en, param_caleak, state_calcium,
#                      state_caleak_cnt,  spike_out, event_tref,
#                      state_calcium_next, state_caleak_cnt_next)

#             # print(f"Imported {module}")
#             spec.loader.exec_module(module)
#             print(f"Imported {module_name} from {module_path}")

# def import_from_all_folders(root_folder):
#     """
#     Traverse all folders in the root directory and import all Python files.
#     """
#     for item in os.listdir(root_folder):
#         item_path = os.path.join(root_folder, item)
#         if os.path.isdir(item_path):
#             print(f"Checking directory: {item_path}")
#             import_python_files_from_directory(item_path)

# # Usage
# root_folder = './src'  # Change this to your root folder path
# import_from_all_folders(root_folder)