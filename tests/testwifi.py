from wifi import Cell, Scheme
import os
import time
import subprocess


# cell = list(Cell.all('wlan0'))
cell = list(Cell.all('wlan0'))

# cellStr = Cell.from_string('Cell(ssid=router)')
# for i in range(len(cell)):
#     if cell[i].ssid == 'smart':
#         # scheme = Scheme.for_cell('wlan0', 'smart', cell[i], 'Loader55')
#         # scheme.save()
#         # scheme.activate()
#         # print("Founded ")
#         # print(cell[i].ssid)
#     print(cell[i])
# print(cell.ssid)
# print(cell)
# scheme = Scheme.for_cell('wlan0', 'smart', cell[4], 'Loader$5')
# scheme.save()
# scheme.activate()
# scheme = Scheme.find('wlan0', 'smart')
# print(scheme)

wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
sudo_mode = "sudo "

def wifi_connect(ssid, psk):
    cmd_result = ""

    # write wifi config to file
    f = open('wifi.conf', 'w')
    f.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
    f.write('update_config=1\n')
    f.write('country=UA\n')
    f.write('\n')
    f.write('network={\n')
    f.write('    ssid="' + ssid + '"\n')
    f.write('    psk="' + psk + '"\n')
    # f.write('    key_mgmt=WPA-PSK\n')
    f.write('}\n')
    f.close()
    time.sleep(1)

    # move to the specific folder and overwrite the old file
    cmd = 'sudo mv wifi.conf ' + wpa_supplicant_conf
    cmd_result = os.system(cmd)
    print(cmd + " - " + str(cmd_result))
    time.sleep(1)

    # reconfigure the wifi service
    cmd = 'wpa_cli -i wlan0 reconfigure'
    cmd_result = os.system(cmd)
    print(cmd + " - " + str(cmd_result))
    time.sleep(10)

    # keep all the information about the network
    p = subprocess.Popen(['ifconfig', 'wlan0'], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    out, err = p.communicate()
    ip_address = "<Not Set>"

    # extract the IP address
    for l in out.split(b'\n'):
        if l.strip().startswith(b'inet '):
            ip_address = l.strip().split(b'inet ')[1].split(b' ')[0]

    return ip_address


# ip = wifi_connect('router', '@Load$5%\Gen%853')
print('@Load$5%Gen$853')
# p = subprocess.Popen(['ifconfig', 'wlan0'], stdout=subprocess.PIPE,
#                          stderr=subprocess.PIPE)

# out, err = p.communicate()
# ip_address = "<Not Set>"

#     # extract the IP address
# for l in out.split(b'\n'):
#     if l.strip().startswith(b'inet '):
#         ip_address = l.strip().split(b'inet ')[1].split(b' ')[0]

    

# if ip == "<Not Set>":
#     print('Fail to connect to Internet')
# else:
#     print('Connection established: IP address: ' + ip.decode("utf-8"))