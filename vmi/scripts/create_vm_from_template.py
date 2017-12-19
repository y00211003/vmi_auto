#!/usr/bin/env python
from pysphere import VIServer
from optparse import OptionParser
from getpass import getpass

usage = "usage: %prop [options]"
parser = OptionParser(usage=usage)
parser.add_option("-s", "--server", dest="vcenter",
                  help="set the vCenter server to connect to")
parser.add_option("-u", "--user", dest="username",
                  help="set the user to connect as")
parser.add_option("-p", "--password", dest="password",
                  help="password to use when connecting")
parser.add_option("-f", "--origin", dest="origin",
                  help="Origin template to copy")
parser.add_option("-t", "--target", dest="target",
                  help="Target template.")

(options, args) = parser.parse_args()

try:
    options.vcenter
except NameError:
    options.vcenter = raw_input("Enter the vCenter to connect to: ")

try:
    options.username
except NameError:
    options.username = raw_input("Enter the usename to use: ")

try:
    options.password
except NameError:
    options.password = getpass()

server = VIServer()
server.connect(options.vcenter,options.username,options.password)

try:
    f_vm = server.get_vm_by_name(options.origin)
    template = f_vm.clone('Template',template = True)
    t_vm = template.clone(options.target, resourcepool = None)
    print t_vm.get_status()
except Exception,e:
    print e
finally:
    server.disconnect()
