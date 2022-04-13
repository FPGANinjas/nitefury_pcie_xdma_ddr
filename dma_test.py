#!/usr/bin/env python3
import os
import time

##############################################    
def main():

    # Generate some data
    TRANSFER_SIZE = 4096
    tx_data = bytearray(os.urandom(TRANSFER_SIZE))

    # Open files
    fd_h2c = os.open("/dev/xdma0_h2c_0", os.O_WRONLY)
    fd_c2h = os.open("/dev/xdma0_c2h_0", os.O_RDONLY)

    # Send data to FPGA 
    start = time.time()
    os.pwrite(fd_h2c, tx_data, 0);
    end = time.time()
    duration = end-start;

    # Print time
    BPS = TRANSFER_SIZE / (duration);
    print("Sent in " + str((duration)*1000.0) + " milliseconds (" + str(BPS/1000000) + " MBPS)")

    # Receive data from FPGA 
    start = time.time()
    rx_data = os.pread(fd_c2h, TRANSFER_SIZE, 0);
    end = time.time()
    duration = end-start;

    # Print time
    BPS = TRANSFER_SIZE / (duration);
    print("Received in " + str((duration)*1000.0) + " milliseconds (" + str(BPS/1000000) + " MBPS)")

    # Make sure data matches
    if tx_data != rx_data:
        print ("Whoops")
    else:
        print ("OK")

    # done
    os.close(fd_h2c)
    os.close(fd_c2h)


##############################################    

if __name__ == '__main__':
    main()


