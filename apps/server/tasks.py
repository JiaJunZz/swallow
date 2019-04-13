#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/1 14:18
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from multiprocessing import current_process
from swallow import celery_app
from .models import Server
from celery.task import Task
from django.conf import settings
from core.ansible_api import AnsiblePlay
import json
import requests

headers = {"Content-Type": "application/json"}


@celery_app.task
class AutoServer(Task):
    name = 'auto_server'

    def __init__(self):

        self.data_server = {
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
        self.interfaces = {
            "nic_name": "",
            "mac_address": "",
            "ip_addr": "",
            "netmask": ""
        }

        self.device_dict = {
            "driver_name": "",
            "capacity": ""
        }

    @staticmethod
    def get_token():
        payload = {
            "username": settings.REQUEST_USERNAME,
            "password": settings.REQUEST_PASSWORD
        }
        r = requests.post(settings.REQUEST_TOKEN_URL, data=json.dumps(payload), headers=headers)
        result = json.loads(r.text)['token']
        return result

    def run(self, *args, **kwargs):
        current_process()._config = {'semprefix': '/mp'}
        host_dict = dict(list(Server.objects.values_list('ip_managemant', 'id')))
        ansible = AnsiblePlay(settings.ANSIBLE_HOSTS_FILE)
        ansible.run_adhoc(settings.ANSIBLE_GROUP, 'setup')
        info = ansible.get_result().get('success')
        authtoken = self.get_token()
        headers_server = {'content-type': "application/json", 'Authorization': 'Token ' + authtoken}
        for ip in info:
            self.data_server["ip_managemant"] = ip
            self.data_server["hostname"] = info[ip]["ansible_facts"]["ansible_hostname"]
            self.data_server["os_type"] = info[ip]["ansible_facts"]["ansible_distribution"]
            self.data_server["os_release"] = info[ip]["ansible_facts"]["ansible_distribution_version"]
            self.data_server["cpu_model"] = info[ip]["ansible_facts"]["ansible_processor"][2]
            self.data_server["cpu_physics_count"] = info[ip]["ansible_facts"]["ansible_processor_count"]
            self.data_server["cpu_core_count"] = info[ip]["ansible_facts"]["ansible_processor_cores"]
            self.data_server["cpu_logic_count"] = info[ip]["ansible_facts"]["ansible_processor_vcpus"]
            self.data_server["mem_capacity"] = float(
                "%.2f" % (int(info[ip]["ansible_facts"]["ansible_memtotal_mb"]) / 1024))
            self.data_server["sn"] = info[ip]["ansible_facts"]["ansible_product_serial"]
            self.data_server["uuid"] = info[ip]["ansible_facts"]["ansible_product_uuid"]
            self.data_server["productmodel"] = info[ip]["ansible_facts"]["ansible_product_name"]
            self.data_server["manufactory"] = info[ip]["ansible_facts"]["ansible_system_vendor"]
            all_nic = info[ip]["ansible_facts"]["ansible_interfaces"]
            all_nic.remove("lo")
            nic_list = []
            for nic_name in all_nic:
                name = "ansible_" + nic_name.replace("-", "_")
                self.interfaces["nic_name"] = nic_name
                try:
                    self.interfaces["ip_addr"] = info[ip]["ansible_facts"][name]["ipv4"]["address"]
                    self.interfaces["netmask"] = info[ip]["ansible_facts"][name]["ipv4"]["network"]
                    self.interfaces["mac_address"] = info[ip]["ansible_facts"][name]["macaddress"]
                except KeyError:
                    self.interfaces = {}
            nic_list.append(self.interfaces)
            self.data_server["nic"] = nic_list
            all_devices = info[ip]["ansible_facts"]["ansible_devices"]
            devices = [x for x in all_devices if x.startswith("sd") or x.startswith("hd")]
            device_list = []
            for d in devices:
                self.device_dict["driver_name"] = d
                self.device_dict["capacity"] = info[ip]["ansible_facts"]["ansible_devices"][d]["size"]
                device_list.append(self.device_dict)
            self.data_server["driver"] = device_list
            if ip in host_dict:
                # PUT更新服务
                datas = json.dumps(self.data_server)
                url = settings.REQUEST_AUTOSERVER_URL + str(host_dict[ip]) + '/'
                requests.put(url, data=datas, headers=headers_server)
            else:
                # POST新增服务器
                datas = json.dumps(self.data_server)
                requests.post(settings.REQUEST_AUTOSERVER_URL, data=datas, headers=headers_server)
