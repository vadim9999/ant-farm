import subprocess

# subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
# subprocess.call(['sudo', 'bluetooth-agent', '1234'])
# cmd = 'sudo hciconfig hci0 piscan'
# subprocess.check_output(cmd, shell = True )
result = subprocess.run(['sudo', 'sudo bluetooth-agent 1234'], stdout=subprocess.PIPE)
print(result.stdout)
result = subprocess.run(['exit'], stdout=subprocess.PIPE)
print(result.stdout)
