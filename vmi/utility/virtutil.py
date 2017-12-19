import libvirt

def request_credentials(credentials, user_data):
    for credential in credentials:
        if credential[0] == libvirt.VIR_CRED_AUTHNAME:
            credential[4] = user_data[0]

            if len(credential[4]) == 0:
                credential[4] = credential[3]
        elif credential[0] == libvirt.VIR_CRED_PASSPHRASE:
            credential[4] = user_data[1]
        else:
            return -1

    return 0


class Connection(object):
    
    def __init__(self, uri):
        
        self.uri = uri
        self.conn = None
        self._open()
        
    def _open(self):
        
        user_data = ['vmi','none']
        
        auth = [[libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_PASSPHRASE], request_credentials, user_data]
        self.vm_conn = libvirt.openAuth(self.uri, auth, 0)
        print self.uri
        if self.vm_conn == None:
            print 'Failed to open connection to %s' % self.uri
            
    def destroy_all_instances(self):
                
        for v_id in self.vm_conn.listDomainsID():
            dom = self.vm_conn.lookupByID(v_id)
            dom.destroy()
