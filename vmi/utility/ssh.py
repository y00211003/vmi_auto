import os
import tempfile
import paramiko

class Connection(object):

    def __init__(self,
                 host,
                 username = None,
                 password = None,
                 private_key = None,
                 port = 22,
                 ):
        self._sftp_live = False
        self._sftp = None
        if not username:
            username = os.environ['LOGNAME']

        templog = tempfile.mkstemp('.txt', 'ssh-')[1]
        paramiko.util.log_to_file(templog)

        self._transport = paramiko.Transport((host, port))
        self._tranport_live = True

        if password:

            self._transport.connect(username = username, password = password)
        else:

            if not private_key:

                if os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
                    private_key = '~/.ssh/id_rsa'
                elif os.path.exists(os.path.expanduser('~/.ssh/id_dsa')):
                    private_key = '~/.ssh/id_dsa'
                else:
                    raise TypeError, "You have not specified a password or key."

            private_key_file = os.path.expanduser(private_key)
            rsa_key = paramiko.RSAKey.from_private_key_file(private_key_file)
            self._transport.connect(username = username, pkey = rsa_key)
    
    def _sftp_connect(self):

        if not self._sftp_live:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
            self._sftp_live = True

    def get(self, remotepath, localpath = None):

        if not localpath:
            localpath = os.path.split(remotepath)[1]
        self._sftp_connect()
        self._sftp.get(remotepath, localpath)

    def put(self, localpath, remotepath = None):
        if not remotepath:
            remotepath = os.path.split(localpath)[1]
        self._sftp_connect()
        self._sftp.put(localpath, remotepath)

    def execute(self, command):
        channel = self._transport.open_session()
        channel.exec_command(command)
        output = channel.makefile('rb', -1).readlines()
        if output:
            return output
        else:
            return channel.makefile_stderr('rb', -1).readlines()

    def close(self):

        if self._sftp_live:
            self._sftp.close()
            self._sftp_live = False

        if self._tranport_live:
            self._transport.close()
            self._tranport_live = False

    def __del__(self):
        self.close()
