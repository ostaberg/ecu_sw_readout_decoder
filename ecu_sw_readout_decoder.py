import sys
import argparse
import re


def decode_array(arg_str, lpc_enabled, viu_enabled):
    # find first instance of '32' in array
    sw_readout_start = 0
    for x in re.finditer("32", arg_str):
        sw_readout_start = x.start()  # store first index of instance where '32' was found
        #print("32 found at", x.start(), x.end())
        break   # first instance found, stop

    array_cleaned = arg_str[sw_readout_start: ]     # extract useful part of the array
    array_cleaned = array_cleaned.replace('-', "")      # remove '-' symbol from the array
    #print(array_cleaned)

    # split string into separate "SW Part Number" slices
    sw_list = []
    sw_length = 14      # number of characters used for specification of each of the SW Part Numbers
    for i in range(0, len(array_cleaned), sw_length):
        sw_list.append(array_cleaned[i:i+sw_length])
    #print(sw_list)

    # convert sw number to same format as used in confighub: NNNNNNNNAAA; N == hex, A == ascii
    sw_hex_length = 8
    sw_ascii_length = 6
    i = 0
    for sw_array in sw_list:
        temp = sw_array[sw_hex_length:sw_hex_length+sw_ascii_length]    # extract part of array that will be converted to ascii characters
        ascii_part = bytearray.fromhex(temp).decode()
        #print(ascii_part)
        sw_array = sw_array[0: sw_hex_length]
        sw_list[i] = sw_array + ascii_part  # replace SW Part Number array with hex and ascii part of the SW
        #print(sw_array)
        i += 1
    #print(sw_list)
            
    # merge two lists into one SW Part Number dictionary containing sw label and sw identifier
    # if lpc flag (-lpc) is set, merge sw_list with other list than the default hpa sw list 
    if lpc_enabled == True:
        sw_type_list = ["SWLM", "SWE1", "SWBL", "SWP2", "SWM1"]
        
        print("\n LPC")
        sw_app_dict_confighub = dict(zip(sw_type_list, sw_list))
        for key,value in sw_app_dict_confighub.items():
            print("  " + key + " : " + value)

    elif viu_enabled == True:
        sw_type_list = ["SWLM[EXE] / SWBT[PBL] (FuncProg + 22F125)", "SWP1[RT]","SWBL [SBL]", "SWE1 [ESS]", "SWL2 [ESM]"]
        
        print("\n VIU")
        sw_app_dict_confighub = dict(zip(sw_type_list, sw_list))
        for key,value in sw_app_dict_confighub.items():
            print("  " + key + " : " + value)

    else:
        sw_type_list = ["SWL2", "SWLM", "SWM1", "SWP2", "CCFG", "SWE1", "SWBL", "SWLM", "SWL3", "SWP2"]
    
        print("\n HPA App")
        sw_app_dict_confighub = dict(zip(sw_type_list[0:5], sw_list))
        for key,value in sw_app_dict_confighub.items():
            print("  " + key + " : " + value)

        print("\n HPA Platform")
        sw_platform_dict_confighub = dict(zip(sw_type_list[5:], sw_list[5:]))
        for key,value in sw_platform_dict_confighub.items():
            print("  " + key + " : " + value)
    
    print("\n")
    #print(sys.argv[0])
    #print(sys.argv[1])
    print(sys.argv[2])


def argument_parse_handler():
    text = "this program decodes the SW Part Numbers array readout response from ParallellDiag and DSA tools in SPA2\n-paste the array as argument. The script will print out the SW Part Numbers individually in same format as presented in ConfigHub"
    parser = argparse.ArgumentParser(
        prog="readout decoder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=text, epilog="---------------------------")

    parser.add_argument('-lpc', '--lpc', action="store_true", help='set flag only if argument is the response from a LPC SW Part Number readout. If -lpc flag not set, given argument (SW Part Number) is intepretated HPA SW Part Number')  # add flag without any argument
    parser.add_argument('-viu', '--viu', action="store_true", help='set flag only if argument is the response from a VIU SW Part Number readout. If no flag set, given argument (SW Part Number) is intepretated HPA SW Part Number')  # add flag without any argument
    parser.add_argument('string', nargs='+', help='paste readout array response from ParallellDiag tool as argument')   #  argument to pass SW Part Number readout response
    
    args = parser.parse_args()
    arg_str = ' '.join(args.string)     #  argument containing blank spaces will be merged and treated as one argument
    
    lpc_flag_enabled = False
    viu_flag_enabled = False
    if args.lpc == True:
        lpc_flag_enabled = True
    elif args.viu == True:
        viu_flag_enabled = True
    else:
        lpc_flag_enabled = False
    #print(arg_str)
    return arg_str, lpc_flag_enabled, viu_flag_enabled

def print_intro():
    print("\n//// ECU SW Readout Decoder 0.0.2, creator Oliver Staberg, date 2023-10-09 ////")

def main():
    print_intro()
    sw_array_raw, lpc_enabled, viu_enabled = argument_parse_handler()
    decode_array(sw_array_raw, lpc_enabled, viu_enabled)

if __name__ == "__main__":
    main()
