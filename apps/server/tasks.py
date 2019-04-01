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

@celery_app.task
class AutoServer(Task):
    name = 'auto_server'
    def run(self, *args, **kwargs):
        current_process()._config = {'semprefix': '/mp'}
        host_list = list(Host.objects.values_list('ip_managemant', flat=True))
        for ip in host_list:
            ansible = Ansible_Play('/etc/ansible/hosts')
            ansible.run_Adhoc(ip, 'setup')
            info = ansible.get_result()
            # QuerySet 获取对应IP的对象
            host = Host.objects.get(ip_managemant=ip)
            if info.get('success'):
                ipv4_all = info['success'][ip]['ansible_facts']['ansible_all_ipv4_addresses']
                ipv4_all.remove(ip)
                if len(ipv4_all) >= 1:
                    # update ip_other1
                    ip_other1 = ipv4_all[0]
                    host.ip_other1 = ip_other1
                if len(ipv4_all) >= 2:
                    # update ip_other2
                    ip_other2 = ipv4_all[1]
                    host.ip_other2 = ip_other2
                # update os_type
                os_type = info['success'][ip]['ansible_facts']['ansible_distribution']
                host.os_type = os_type
                # update os_type
                os_release = info['success'][ip]['ansible_facts']['ansible_distribution_version']
                host.os_release = os_release
                # update cpu_physics_count
                cpu_physics_count = info['success'][ip]['ansible_facts']['ansible_processor_count']
                host.cpu_physics_count = cpu_physics_count
                # update cpu_core_count
                cpu_core_count = info['success'][ip]['ansible_facts']['ansible_processor_cores']
                host.cpu_core_count = cpu_core_count
                # update cpu_logic_count
                cpu_logic_count = info['success'][ip]['ansible_facts']['ansible_processor_vcpus']
                host.cpu_logic_count = cpu_logic_count
                # update mem_capacity
                mem_capacity = float(info['success'][ip]['ansible_facts']['ansible_memtotal_mb']) / 1024
                host.mem_capacity = mem_capacity
                # update mac_address
                mac_address = info['success'][ip]['ansible_facts']['ansible_default_ipv4']['macaddress']
                host.mac_address = mac_address
                # update sn
                sn = info['success'][ip]['ansible_facts']['ansible_product_serial']
                host.sn = sn
                # update model
                model = info['success'][ip]['ansible_facts']['ansible_product_name']
                host.model = model
                host.save()
            return info
