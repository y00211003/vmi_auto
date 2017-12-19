#!/usr/bin/env python2

from lxml import etree
import smtplib
import os,sys,commands
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
sys.path.insert(0, os.path.dirname(__file__) )
from gatherresults import *

me='performance_superlab@vmi_qa.com'
#you = ['xiang_wang@trendmicro.com.cn', 'xinxin_fang@trendmicro.com.cn']
#you=['AllofCNVMIQATeam@dl.trendmicro.com', 'AllofCNVMIQAInternTeam@dl.trendmicro.com','neil_cheng@trendmicro.com.cn','george_zhang@trendmicro.com.cn']

#you=['AllofCNVMIQATeam@dl.trendmicro.com', 'AllofCNVMIQAInternTeam@dl.trendmicro.com']
#you=['AllofCNVMITeam@dl.trendmicro.com', 'AllofCNVMIQAInternTeam@dl.trendmicro.com']
#you=['AllofCNVMITeam@dl.trendmicro.com']
you=['richard_yuan@trendmicro.com.cn']

#others=['richard_yuan@trendmicro.com.cn', 'AllofCNVMIQAInternTeam@dl.trendmicro.com', 'harvey_hu@trendmicro.com.cn', 'sarah_ye@trendmicro.com.cn', 'xiafei_lu@trendmicro.com.cn']
others=['richard_yuan@trendmicro.com.cn']

success_template='''<html>
<body>
<p><br>Dears,</br></p>
<p>
we have passed the automation test in build %s.


%s cases passed, and %s failed.
</p>
</body>
</html>
'''
#body = open('template.htm').read()
def get_result_from_xml(output):
    passed = None
    failed = None
    result = {}
    '''
    xml=open(output).read()
    root = etree.XML(xml)
    elem = root.find("statistics").find("total")

    for child in elem:
        if child.text == 'All Tests':
            for key, value in sorted( child.items()):
                passed = child.get('pass')
                failed = child.get('fail')
    suite = root.find('suite')
    for test in suite:
        if test.tag == 'test':
            name = test.get('name')
            s = test.find('status')
            result[name]= s.get('status')
    '''
    result = gather_test_results(output)
    passed = len(filter(lambda x : result[x] == 'PASS' , result) )
    failed = len(result) - passed
    return passed , failed, result

def generate_case_result(name, status):
    s='<tr><td width=8%">'+ name + '</td><td width=6%">'+ status +'</td></tr>'
    return s

if __name__ == '__main__':
    passed, failed, result =  get_result_from_xml(sys.argv[2])
    print passed, failed, result
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'TMVMI 5.5 build %s performance superlab automation test %s passed %s failed' % ( sys.argv[1], passed, failed)
    msg['From'] = me
    msg['To'] = ",".join(you)
    msg['Cc'] = ",".join(others)

    cmd_Server_CPU_Title = 'head -n 3 /root/vmi/sarCpuData.txt | tail -n 1'
    output_Server_CPU_Title = commands.getoutput(cmd_Server_CPU_Title)

    cmd_Server_CPU_Data = 'tail -n 1 /root/vmi/sarCpuData.txt'
    output_Server_CPU_Data = commands.getoutput(cmd_Server_CPU_Data)

    cmd_Server_Mem_Title = 'head -n 3 /root/vmi/sarMemData.txt | tail -n 1'
    output_Server_Mem_Title = commands.getoutput(cmd_Server_Mem_Title)

    cmd_Server_Mem_Data = 'tail -n 1 /root/vmi/sarMemData.txt'
    output_Server_Mem_Data = commands.getoutput(cmd_Server_Mem_Data)

#    cmd_User001Time = 'tail -n 1 /root/vmi/10001001001.txt'
#    output_User001Time = commands.getoutput(cmd_User001Time)

#    cmd_User002Time = 'tail -n 1 /root/vmi/10001001002.txt'
#    output_User002Time = commands.getoutput(cmd_User002Time)

#    cmd_User003Time = 'tail -n 1 /root/vmi/10001001003.txt'
#    output_User003Time = commands.getoutput(cmd_User003Time)

#    cmd_User004Time = 'tail -n 1 /root/vmi/10001001004.txt'
#    output_User004Time = commands.getoutput(cmd_User004Time)

#    cmd_RealDeviceTime = 'tail -n 1 /root/vmi/droidLoginTime.txt'
#    output_RealDeviceTime = commands.getoutput(cmd_RealDeviceTime)

    org = open('template.htm').read().split('TESTRESULT')
    body1 = org[0].replace('BUILD',str(sys.argv[1]))
    body2 = body1.replace('Server_CPU_Title',str(output_Server_CPU_Title))
    body3 = body2.replace('Server_CPU_Data',str(output_Server_CPU_Data))
    body4 = body3.replace('Server_Mem_Title',str(output_Server_Mem_Title))
    body = body4.replace('Server_Mem_Data',str(output_Server_Mem_Data))
#    body5 = body4.replace('Server_Mem_Data',str(output_Server_Mem_Data))
#    body6 = body5.replace('User001Time',str(output_User001Time))
#    body7 = body6.replace('User002Time',str(output_User002Time))
#    body8 = body7.replace('User003Time',str(output_User003Time))
#    body = body8.replace('RealDeviceTime',str(output_RealDeviceTime))
    #body = body7.replace('User003Time',str(output_User003Time))

    for c in sorted(result):
    #for c in result:
        r = '<font color=\"green\">%s</font>' % result[c]
        if result[c] == 'FAIL':
            r = '<font color=\"red\">%s</font>' % result[c]
        s=generate_case_result(c, r)
        body += s

    body += org[1]

    jpgpart1 = MIMEApplication(open('/root/vmi/realDeviceLoginTime.png', 'rb').read())
    jpgpart1.add_header('Content-Disposition', 'attachment', filename='realDeviceLoginTime.png')

    jpgpart2 = MIMEApplication(open('/root/vmi/uniaLoginTime.png', 'rb').read())
    jpgpart2.add_header('Content-Disposition', 'attachment', filename='uniaBootTimeInParallel.png')

    part1 = MIMEText(body,'html')
    msg.attach(part1)
    msg.attach(jpgpart1)
    msg.attach(jpgpart2)
    s = smtplib.SMTP('10.204.16.7')
    s.sendmail(me,[you,others],msg.as_string())
    s.quit()
