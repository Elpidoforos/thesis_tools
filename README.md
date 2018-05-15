# RPiCanBus
This repository will keep the scripts which are developed for the purspose of the Elpidoforos Arapantonis MSc thesis in Information Security programe in Luleå University of Technology. The developement board which the thesis is based upon is a Rarpberry Pi with a PICAN2 module. 

log_data.py : will run on the background upon start up and wait for input from a CAN Bus network. When a good amount of data are gathered then some packets will be alternated and refeed back to the bus in order to confuse/fuzz the receiving node.

A log in the logfile.txt shall look like the snipset below:
Timestamp: 1525196535.167178        ID: 0123    S          DLC: 8    ff ff ff ff ff ff ff ff

*Timestamp : When the frame has been caught
*ID: The frame ID of the packet
*DLC: The size of the data frame
*The last field ff ff ff ff...  are the data of the frame.
