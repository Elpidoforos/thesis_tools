" ---------- Developed by Elpis as part of Master Thesis project elpidoforos@gmail.com ------------------------"
import re
import os
import random
import hashlib
import can
from can import Message
from time import sleep
import subprocess

#Try to receiver  CAN Frames and keep then in file
#If no can frames for 5 mins then run the default file against all the possible data packets (8 bytes)

#Can interface setup for send and receive
can_int = 'can0'
bus = can.interface.Bus(can_int,bustype='socketcan')

def main():
    welcome_screen()
    can_int_check()
    menu_call()
    #can_receive()
    #sleep(5)
    #unique_ids = extract_can_frame_ids()
    #sleep(5)
    #can_send(unique_ids)

def welcome_screen():
    print ("\n")
    print ("--------------------------------------------------------------")
    print ("------------  Welcome to the RPiCanBusFuzzer  ----------------")
    print ("if you have any questions please contact elpidoforos@gmail.com")
    print ("------------------------------------------------------------\n")

#Check the validity of the CAN Bus interface
def can_int_check():
    can_int_name = raw_input("Enter the CAN Bus Interface name: ")
    #Return 1 upon error, and 0 upon succes
    output_canName = subprocess.call(["ifconfig",can_int_name], stdout=open(os.devnull, 'wb'))
    #Check if the interface name exists
    if output_canName == 1:
        print("Wrong interface name, please check the CAN Bus interface name from ifconfig.\n")
        can_int_check()

    elif output_canName == 0:
        #Check if the interface is up
        bashCommandCanInf = "ip a show " + can_int_name
        process = subprocess.Popen(bashCommandCanInf.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if "DOWN" in output:
            print("The CAN Bus interface is DOWN, please activate it and start the RPiCanBusFuzzer again...")
            exit()
    else:
        print ("Something went wrong please restart the application....")
        exit()

def menu_call():
    menu = True
    filename = True
    packets = True
    while menu:
        print ("""
        1.Capture CAN Bus traffic
        2.Capture CAN Bus traffic and extract the Frame IDs
        3.Capture Traffic and Replay on the CAN Bus, with random data
        4.Exit/Quit
        """)
        menu = raw_input("Select one of the actions above:")
        if menu == "1":
            filename = raw_input("Enter filename for the CAN Bus log:")
            packet_count = raw_input("How many packets you would like to capture? (0-1000):")
            try:
                int(packet_count)
            except ValueError:
                print("\n The number of the packets shall be an integer value! (0-1000)")
            else:
                if int(packet_count) > 1000 or int(packet_count) < 0:
                    print("\n Packet range not valid! (0-1000)")
                else:
                    can_receive_adv(filename,int(packet_count))

        elif menu == "2":
            print("\n Run Function xxxxx")
        elif menu == "3":
            print("\n Run Function xxxxx")
        elif menu == "4":
            print("\n Goodbye....")
            exit()
        elif menu != "":
            print("\n Not Valid Choice Try again....")

def can_receive_adv(filename, packet_count):
    count = 0
    no_message_count = 0
    print "Receiving CAN Frame please wait.........."
    while(1):
        message = bus.recv(timeout=2)
        print message

        if message is None:
            no_message_count += 1
            if no_message_count > 20:
                print ('Timeout occured, please check your connection and try again...')
                exit()
        else:
            for message in bus:
                with open(filename, 'a') as afile:
                    afile.write(str(message) + '\n')
                    count += 1
                    continue
                    #print count
                    if count > packet_count:
                       print "Packets have been captured and saved in the filename: " + filename 

def extract_can_frame_ids():
    all_frame_ids = []
    print "Extract CAN Frames....."
    try:
        # Open the kept logfile, if not revert to a default one arbitration_ids
        with open('logfile.txt', 'r') as afile:
            logs = afile.readlines()
            for line_log in logs:
                id = re.search(r"(ID: )([0-9a-fA-F]+)", line_log)
                #Regular expression to extract the data field. README has more info on how the data look like
                data = re.search(r"([0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+ [0-9a-f]+)",
                                 line_log)
                all_frame_ids.append(id.group(2).lstrip('0'))
    except:
        #If there were no valid frame ids because of no frames then create a random one and send it on the bus
        with open('arbitration_ids', 'r') as afile:
            logs = afile.readlines()
            for i in range(0,40):
                all_frame_ids.append(random.choice(logs).rstrip())
    # Keep all the unique frame ids only
    unique_ids = list(set(all_frame_ids))
    return unique_ids


def can_send(unique_ids):
    print "Sending CAN Frames..."
    count_send = 0
    count_err = 0
    while(1):
        for id in unique_ids:
            data_format = [random_hex(), random_hex(), random_hex(), random_hex(), random_hex(), random_hex(), random_hex(),random_hex()]
            arbitration_id_format =  int(id,16)
            #print arbitration_id_format
            #print data_format
            msg = can.Message(extended_id=False, arbitration_id=arbitration_id_format, data=data_format)
            #print msg
            try:
                bus.send(msg)
                count_send += 1
                sleep(0.1)
                if count_send > 40:
                    return
                else:
                    continue
            except:
                print "Error on CAN Frame trasmission"
                count_err += 1
                if count_err>20:
                    return
                else:
                    continue

#Generate a random data field for the CAN frame
def random_hex():
    return random.randint(0,255)
    #randomhex = ''.join([random.choice('0123456789ABCDEF') for x in range(2)])
    #return (hex(int(randomhex, 16) + int("0x20", 16)))

if __name__ == "__main__":
    main()
