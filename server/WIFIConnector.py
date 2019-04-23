from wifi import Cell, Scheme
import os
import time
import subprocess


# cell = list(Cell.all('wlan0'))

class WIFIConnector():
    wpa_supplicant_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
    sudo_mode = "sudo "

    def getWIFINetworks(self):


        cell = list(Cell.all('wlan0'))
        arrStr = "["
        for i in range(len(cell)):
            arrStr = arrStr + "\"" + cell[i].ssid + "\""

            if i < (len(cell) -1):
               arrStr = arrStr + ","

        arrStr = arrStr + "]"

        # scheme = Scheme.for_cell('wlan0', 'smart', cell[i], 'Loader55')
        # scheme.save()
        # scheme.activate()
        # print("Founded ")
        # print(cell[i].ssid)
    # print(cell[i])
        return arrStr

    def wifi_connect(self,ssid, psk):
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
        cmd = 'sudo mv wifi.conf ' + self.wpa_supplicant_conf
        cmd_result = os.system(cmd)
        print(cmd + " - " + str(cmd_result))
        time.sleep(1)

        # reconfigure the wifi service
        cmd = 'wpa_cli -i wlan0 reconfigure'
        cmd_result_wifi = os.system(cmd)
        
        print(cmd + " - " + str(cmd_result_wifi))
        time.sleep(20)
        if cmd_result_wifi == 0:
            p = subprocess.Popen(['ifconfig', 'wlan0'], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

            out, err = p.communicate()
            ip_address = "<Not Set>"

    # extract the IP address
            for l in out.split(b'\n'):
                if l.strip().startswith(b'inet '):
                    ip_address = l.strip().split(b'inet ')[1].split(b' ')[0]

            ip_address = str(ip_address.decode("utf-8"))
            print(ip_address)
            return ip_address
        else:

            return "FAIL"

    def getIP(self):
        p = subprocess.Popen(['ifconfig', 'wlan0'], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

        out, err = p.communicate()
        ip_address = "NoIP"

    # extract the IP address
        for l in out.split(b'\n'):
            if l.strip().startswith(b'inet '):
                ip_address = l.strip().split(b'inet ')[1].split(b' ')[0]

        if ip_address != "NoIP":
            ip_address = str(ip_address.decode("utf-8"))
            print(ip_address)
            return ip_address
        else:
            return "NoIP"
            
        
        
    # keep all the information about the network
        








# ip = wifi_connect('router', '@Load$5%\Gen%853')
