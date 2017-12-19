#!/usr/bin/env python2

from lxml import etree
import smtplib
import os,sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
sys.path.insert(0, os.path.dirname(__file__) )
from gatherresults import *
me='tmvmi_qa_bot@vmi.com'
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
    msg['Subject'] = 'TMVMI 5.5 build %s client automation test %s passed %s failed' % ( sys.argv[1], passed, failed)
    msg['From'] = me
    msg['To'] = ",".join(you)
    msg['Cc'] = ",".join(others)

    org = open('template.htm').read().split('TESTRESULT')
    body = org[0].replace('BUILD',str(sys.argv[1]))

    for c in sorted(result):
    #for c in result:
        r = '<font color=\"green\">%s</font>' % result[c]
        if result[c] == 'FAIL':
            r = '<font color=\"red\">%s</font>' % result[c]
        s=generate_case_result(c, r)
        body += s

    body += org[1]

    part1 = MIMEText(body,'html')
    msg.attach(part1)
    s = smtplib.SMTP('10.204.16.7')
    s.sendmail(me,[you,others],msg.as_string())
    s.quit()
