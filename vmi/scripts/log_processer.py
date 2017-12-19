# -*- coding: UTF-8 -*-

import os
from datetime import datetime

portal_log_files = ['portal.log', 'portal.log.1', 'portal.log.2', 'portal.log.3', 'portal.log.4', 'portal.log.5']
unia_callback_files = ['unia_callback.log', 'unia_callback.log.1', 'unia_callback.log.2', 'unia_callback.log.3', 'unia_callback.log.4', 'unia_callback.log.5']

portal_get_config_lines = []
portal_useful_lines = []
for portal_log_file in portal_log_files:
	file_lines = []
	if os.path.exists(portal_log_file):
		try:
			fobj = open(portal_log_file, 'r')
			file_lines = fobj.readlines()
		finally:
			fobj.close()
		for line in file_lines:
			if 'get config' in line:
				portal_get_config_lines.append(' '.join(line.strip().split()[2:]))
			if ('get config' in line) or ('start unia command to unia process' in line) or ('unia instance is' in line) or ('check unia request by' in line):
				portal_useful_lines.append(' '.join(line.strip().split()[2:]))
			

unia_callback_lines = []
unia_callback_useful_lines = []
for unia_callback_file in unia_callback_files:
	file_lines = []
	if os.path.exists(unia_callback_file):
		try:
			fobj = open(unia_callback_file, 'r')
			file_lines = fobj.readlines()
		finally:
			fobj.close()
		for line in file_lines:
			if 'status to active' in line:
				unia_callback_lines.append(' '.join(line.strip().split()[2:]))
			if ('status to active' in line) or ('status to idle' in line):
				unia_callback_useful_lines.append(' '.join(line.strip().split()[2:]))
			
portal_get_config_lines.extend(unia_callback_lines) 
portal_get_config_lines.sort()

portal_useful_lines.extend(unia_callback_useful_lines)
portal_useful_lines.sort()

#for line in portal_get_config_lines:
#	print line
	
#filter the pair of two lines of get config and UNIA active
previous_type = 'get_config'
previous_line = ''
logs = []
for line in portal_get_config_lines:
	#if 'test' not in line:
	if previous_line == '':
		previous_line = line
		if 'get config' in line:
			previous_type = 'get_config'
		else:
			previous_type = 'unia_active'
	else:
		if 'active' in line:
			if previous_type == 'get_config':
				#print previous_line
				previous_line_user = previous_line.split()[3]
				current_line_user = line.split()[5]
				if previous_line_user == current_line_user:
					logs.append(previous_line)
					logs.append(line)
					previous_type = 'unia_active'
					previous_line = line
		else:
			previous_type = 'get_config'
			previous_line = line		
#for line in logs:
#	print line

#calculate the login time
get_config_time = ''
login_complete_time = ''
fobj = open('vmi_login_time.csv', 'w')
login_time_result = []
slow_login_records = {}
t_0_5 = 0
t_6_10 = 0
t_11_15 = 0
t_16_20 = 0
t_20_more = 0
login_count = 0
login_time_result.append('Login Timestamp,User Name,Time Cost,,,Login Time Range,Login Time Distribution,Percentage')
for line in logs:
	if 'get config' in line:		
		get_config_time = line.split()[0] + ' ' + line.split()[1]
		get_config_time1 = line.split()[0] + ' ' + line.split()[1].split(',')[0]
	else:
		login_complete_time = line.split()[0] + ' ' + line.split()[1]
		login_count += 1
		current_line_user = line.split()[5]
		time_delta = (datetime.strptime(str(login_complete_time),"%Y-%m-%d %H:%M:%S,%f") - datetime.strptime(str(get_config_time),"%Y-%m-%d %H:%M:%S,%f")).seconds + 1
		if time_delta <= 5:
			t_0_5 += 1
		elif time_delta <=10:
			t_6_10 += 1
		elif time_delta <= 15:
			t_11_15 += 1
		elif time_delta <= 20:
			t_16_20 += 1
			slow_login_records[get_config_time] = current_line_user
		else:
			t_20_more += 1
			slow_login_records[get_config_time] = current_line_user
		result = get_config_time1 + ','+ current_line_user + ','+ str(time_delta)
		login_time_result.append(result)
login_time_result[1] = login_time_result[1] + ',,,[1 ~ 5],' + str(t_0_5) + ",%.1f%%" % (float(t_0_5)/float(login_count)*100)
login_time_result[2] = login_time_result[2] + ',,,[6 ~ 10],' + str(t_6_10) + ",%.1f%%" % (float(t_6_10)/float(login_count)*100)
login_time_result[3] = login_time_result[3] + ',,,[11 ~ 15],' + str(t_11_15) + ",%.1f%%" % (float(t_11_15)/float(login_count)*100)
login_time_result[4] = login_time_result[4] + ',,,[16 ~ 20],' + str(t_16_20) + ",%.1f%%" % (float(t_16_20)/float(login_count)*100)
login_time_result[5] = login_time_result[5] + ',,,[>20],' + str(t_20_more) + ",%.1f%%" % (float(t_20_more)/float(login_count)*100)

for line in login_time_result:
	fobj.write(line + '\n')
fobj.close()

print 'The summary of login time has been saved in login_time.csv. Please open it in Excel.\n'

slow_login_logs = []
log_length = len(portal_useful_lines)
if len(slow_login_records) > 0:
	for get_config_time in slow_login_records.keys():
		for i in range(log_length):
			if portal_useful_lines[i].startswith(get_config_time):
				slow_login_logs.append('User Name: %s' % slow_login_records[get_config_time])				
				slow_login_logs.append(portal_useful_lines[i])
				for count in range(50):
					line = portal_useful_lines[i+count]
					slow_login_logs.append(line)
					if 'set user %s status to idle'%slow_login_records[get_config_time] in line:
						unia_boot_complete_time =  line.split()[0] + ' ' + line.split()[1]
					elif 'unia instance is ready for user' in line:
						unia_check_unia_complete_time =  line.split()[0] + ' ' + line.split()[1]
					elif 'set user %s status to active'%slow_login_records[get_config_time] in line:
						unia_active_time =  line.split()[0] + ' ' + line.split()[1]
						break
				delta1 = (datetime.strptime(str(unia_boot_complete_time),"%Y-%m-%d %H:%M:%S,%f") - datetime.strptime(str(get_config_time),"%Y-%m-%d %H:%M:%S,%f")).seconds
				delta2 = (datetime.strptime(str(unia_check_unia_complete_time),"%Y-%m-%d %H:%M:%S,%f") - datetime.strptime(str(unia_boot_complete_time),"%Y-%m-%d %H:%M:%S,%f")).seconds
				delta3 = (datetime.strptime(str(unia_active_time),"%Y-%m-%d %H:%M:%S,%f") - datetime.strptime(str(unia_check_unia_complete_time),"%Y-%m-%d %H:%M:%S,%f")).seconds
				slow_login_logs.append('Time distribution: Get config to UNIA boot complete: %d' % delta1)
				slow_login_logs.append('Time distribution: UNIA boot complete to Check UNIA complete: %d' % delta2)
				slow_login_logs.append('Time distribution: Check UNIA complete to RMX connection established: %d' % delta3)
				slow_login_logs.append('##%s,%d,%d,%d'% (slow_login_records[get_config_time], delta1, delta2, delta3))
				slow_login_logs.append('----------------------------------------------------------------------------------------------------------------------')
				break
	fobj = open('vmi_slow_login.log', 'w')
	for line in slow_login_logs:
		fobj.write(line + '\n')
	fobj.close()
	print 'There are %d user login records whose login time is longer than 15 seconds. Please check the log file vmi_slow_login.log' % (t_16_20 + t_20_more) 


