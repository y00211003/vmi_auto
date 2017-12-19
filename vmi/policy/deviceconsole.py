import telnetlib

class DeviceConsole(object):

    '''
    Telnet Commucation with Device Console
    '''


    def __init__(self, device_address="127.0.0.1", device_port=5555, device_shell_name = '$'):
        '''
        Constructor
        '''
        self.device_address = device_address
        self.device_port = device_port
        self.device_name = device_address+':'+ str(device_port)
        self.console_shell_name = device_shell_name
    
    def sendSMS(self, recv_num, text):
        tn = telnetlib.Telnet(host=self.device_address, port=self.device_port, timeout=60)
        tn.write("sms send %s %s \n" %(recv_num, text))
        try:
            tn.read_until("OK", 60)
            tn.close()
            return True
        except Exception, e:
            msg = "Failed to send SMS: [%s]" %str(e)
            self.m_logger.error(msg)
            return False
        
    def makePhoneCall(self, phone_num):
        tn = telnetlib.Telnet(host=self.device_address, port=self.device_port, timeout=60)
        tn.write("gsm call %s\n" %(phone_num))
        try:
            tn.read_until("OK", 60)
            tn.close()
            return True
        except Exception, e:
            msg = "Failed to make a phone call: [%s]" %str(e)
            self.m_logger.error(msg)
            return False
        
    def cancelPhoneCall(self, phone_num):
        tn = telnetlib.Telnet(host=self.device_address, port=self.device_port, timeout=60)
        tn.write("gsm cancel %s\n" %(phone_num))
        try:
            tn.read_until("OK", 60)
            tn.close()
            return True
        except Exception, e:
            msg = "Failed to cancel a phone call: [%s]" %str(e)
            self.m_logger.error(msg)
            return False
        
if __name__=="__main__":
    pass
