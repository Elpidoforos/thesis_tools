import sys
from SupportFuncCalls import *
from can import Message
from InfCheck import *
import argparse

def main():
    args = parse_arguments()

    welcome_screen()
    #Instanciate the Support Functions Class
    supp_func = SupportFuncCalls()
    inf_chk = InfCheck()

    #Get interface name
    inf_name = args.inf
    #Check that the CAN Interface it is up
    bus_obj = inf_chk.inf_status(inf_name)

    '''
    help = sys.argv[1]
    if help == "--help":
        print("This will be a help menu!!")
    else:
        try:
            #Add interface name for data capturing
            #(inf_name,inf_opr) = (0,None) # Default Values
            inf_opr = sys.argv[1]
            inf_name =sys.argv[2]
        except (NameError,IndexError):
            print("ERROR: You shall provide an interface name. For help type CanBusFuzzer.py --help")
        try:
            #This argument will be used either to replay or save traffic.
            save_replay = sys.argv[3]
            log_file_name_save_replay = sys.argv[4]
            #Save Log file
            if save_replay == '-s':
                save_file_name = log_file_name_save_replay
            elif save_replay == '-r':
                replay_file_name = log_file_name_save_replay
            elif save_replay == '-sr':
                save_replay_file_name = log_file_name_save_replay
        except (NameError,IndexError):
            print("ERROR: You shall provide a file name")
'''


def parse_arguments():
    parser = argparse.ArgumentParser()
    #Adding Arguments
    parser.add_argument("--inf_name","-i",dest="inf", help="Add the needed CAN Bus Interface", type=str, required=True)
    parser.add_argument("--save_log","-s",dest="save", help="Capture the traffic and save it in a file", type=str, required=False)
    parser.add_argument("--replay_log","-r", dest="replay",help="Replay the traffic from a file", type=str, required=False)
    parser.add_argument("--save_replay_log","-sr", dest="save_replay",help="Capture the traffic and replay it with random data", type=str, required=False)
    return parser.parse_args()


#Welcome screen during the script initialization
def welcome_screen():
    print ("\n" + "---------------------------------------------------------------" 
        + "\n" + "-------------  Welcome to the RPiCanBusFuzzer  ----------------" 
        + "\n" + "if you have any questions please contact elpidoforos@gmail.com" 
        + "\n" + "---------------------------------------------------------------\n")

if __name__ == "__main__":
    main()


'''
        1.Capture CAN Bus traffic
        2.Capture CAN Bus traffic and extract the Frame IDs
        3.Capture Traffic and Replay on the CAN Bus with random CAN data
        4.Replay Traffic from captured or random ID list (if ID list exist replay, otherwise generate IDs and replay)
        5.Persistent attack with random data (if ID list exist replay, otherwise generate IDs and replay)
        6.Restart the CAN Bus Interface
'''