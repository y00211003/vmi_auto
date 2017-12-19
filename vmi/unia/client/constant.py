import threading


MUTEX = threading.Lock() 

VNC_MODE = 0
CSR_MODE = 1
X_MODE = 2

MODE_USED = -1

VNC_HEADER  = 'RFB 003.009\n'
CSR_HEADER  = 'CSR 003.009\n'
X_HEADER    = 'RFB 003.009\n'

DEVICE_WIDTH    = 480
DEVICE_HEIGHT   = 800
