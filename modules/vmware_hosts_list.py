#!/usr/bin/env python
#!/bin/python

import json
import sys
from pyVim.connect import SmartConnect
try:
        from pyVmomi import vim
except Exception as e:
        print(e)
        print("Please install pyVmomi and try again")
        sys.exit(1)
import ssl
#import configparser
from ansible.module_utils.basic import *

def main():
        #module = AnsibleModule(argument_spec={})
	module_args = dict(
            vcenter=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True)
        )
	module = AnsibleModule(
				 argument_spec=module_args,
				 supports_check_mode=True
			 )
	#response = {'HOST': module.params['host']}    
#        vcenter = mainresponse['HOST']
        vcenter = module.params['vcenter']
        username = module.params['username']
        password = module.params['password']
#https://www.programcreek.com/python/example/94933/ansible.module_utils.basic.AnsibleModule
#http://devopstechie.com/create-custom-ansible-module/
        #Get all the Clusters from vCenter invetory and printing its name
        #Below is Python 2.7.x code, which can be easily converted to python 3.x version
        
        #s=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        #s.verify_mode=ssl.CERT_NONE

        s = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        s.verify_mode = ssl.CERT_NONE
        #another non good method #s = ssl._create_unverified_context()
        
        #inifile=configparser.ConfigParser()
        #inifile.read(r'esxi_hosts_list.ini')
        #host = inifile['server']['vcenter']
        #user = inifile['credential']['username']
        #pwd = inifile['credential']['password']
        #print(host)

        #si = SmartConnect(host="192.168.34.20", user="Administrator@vsphere.local", pwd="Computer@1",sslContext=s)
        #si= SmartConnect(host=host, user=user, pwd=pwd, sslContext=s)
        si = SmartConnect(host=vcenter, user=username, pwd=password,sslContext=s)
        content=si.content

        # Method that populates objects of type vimtype
        def get_all_objs(content, vimtype):
                obj = {}
                container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
                for managed_object_ref in container.view:
                        obj.update({managed_object_ref: managed_object_ref.name})
                return obj

        #Calling above method
        esxihosts=get_all_objs(content, [vim.HostSystem])

        #Iterating each cluster object and printing its name
        #for host in esxihosts:
        #        print (host.name)

        #show results in ansible required format
        #esxilist = esxihosts.Name
        formatedlist = []
        for esxihost in esxihosts:
                test = str(esxihost.name)
                formatedlist.append(test)

        #all_hosts={'hosts': formatedlist}
        #all_hosts={'esxi': {'hosts': formatedlist, 'vars' : {'entity': 'EsxiHosts'}}}
        
        #print(json.dumps(all_hosts))  
        #return None
        #module = AnsibleModule(argument_spec={})
        response = {'hosts': formatedlist}
        module.exit_json(changed=True, meta=response)

if __name__== "__main__":
        main()

#ansible -i test.py all --list-hosts