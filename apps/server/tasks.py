#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/1 14:18
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from core.ansible_api import Ansible_Play
from multiprocessing import current_process
from .models import Server
import datetime
from celery.task import Task
from swallow import celery_app

data_server = {
    "ip_managemant": "",
    "hostname": "",
    "os_type": "",
    "os_release": "",
    "cpu_model": "",
    "cpu_physics_count": "",
    "cpu_core_count": "",
    "cpu_logic_count": "",
    "mem_capacity": "",
    "disk_capacity": "",
    "sn": "",
    "uuid": "",
    "productmodel": "",
    "manufactory": "",
    "nic": "",
}

@celery_app.task
class AutoServer(Task):
    name = 'auto_server'
    def run(self, *args, **kwargs):
        current_process()._config = {'semprefix': '/mp'}
        host_dict = dict(list(Server.objects.values_list('ip_managemant', 'id')))
        ansible = Ansible_Play('/etc/ansible/hosts')
        ansible.run_Adhoc('servers', 'setup')
        info = ansible.get_result().get('success')
        hosts = host_dict.keys()
        for ip in info:
            data_server["ip_managemant"] = ip
            data_server["hostname"] = info[ip]['ansible_facts']['ansible_hostname']
            data_server["os_type"] = info[ip]['ansible_facts']['ansible_distribution']
            data_server["os_release"] = info[ip]['ansible_facts']['ansible_distribution_version']
            data_server["cpu_model"] = info[ip]['ansible_facts']['ansible_processor'][2]
            data_server["cpu_physics_count"] = info[ip]['ansible_facts']['ansible_processor_count']
            data_server["cpu_core_count"] = info[ip]['ansible_facts']['ansible_processor_cores']
            data_server["cpu_logic_count"] = info[ip]['ansible_facts']['ansible_processor_vcpus']
            data_server["mem_capacity"] = float('%.2f' % (int(info[ip]['ansible_facts']['ansible_memtotal_mb']) / 1024))
            # data_server["disk_capacity"] =
            data_server["sn"] = info[ip]['ansible_facts']['ansible_product_serial']
            data_server["uuid"] = info[ip]['ansible_facts']['ansible_product_uuid']
            data_server["productmodel"] = info[ip]['ansible_facts']['ansible_product_name']
            data_server["manufactory"] = info[ip]['ansible_facts']['ansible_system_vendor']
            all_nic = info[ip]['ansible_facts']['ansible_interfaces']
            all_nic.remove('lo')
            nic_list = []
            for nic_name in all_nic:
                name = 'ansible_' + nic_name.replace("-", "_")
                interfaces["nic_name"] = nic_name
                interfaces["mac_address"] = info[ip]['ansible_facts'][name]['macaddress']
                interfaces["ip_addr"] = info[ip]['ansible_facts'][name]['ipv4']['address']
                interfaces["netmask"] = info[ip]['ansible_facts'][name]['ipv4']['network']
                nic_list.append(interfaces)
            data_server["nic"] = nic_list
            print(json.dumps(data_server))
            if ip in host_dict:
                pass
                # put server (ip and info)
            else:
                # post server
                pass



