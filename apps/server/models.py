from django.db import models
from manufactory.models import Manufactory, ProductModel
from supplier.models import Supplier
from idc.models import Idc,Cabinet


# Create your models here.
class Server(models.Model):
    """
    服务器模型
    """
    ip_managemant = models.GenericIPAddressField("管理IP", db_index=True, unique=True, max_length=15, help_text="管理IP")
    hostname = models.CharField("主机名", max_length=24, db_index=True, help_text="主机名")
    os_type = models.CharField("系统类型", max_length=16, help_text="系统类型")
    os_release = models.CharField("操作系统版本", max_length=16, help_text="操作系统版本")
    cpu_model = models.CharField("CPU型号", max_length=128, blank=True, null=True,help_text="CPU型号")
    cpu_physics_count = models.SmallIntegerField("物理CPU个数", help_text="物理CPU个数")
    cpu_core_count = models.SmallIntegerField("CPU核数", help_text="CPU核数")
    cpu_logic_count = models.SmallIntegerField("逻辑CPU个数", help_text="逻辑CPU个数")
    mem_capacity = models.DecimalField("内存大小(GB)", max_digits=10, decimal_places=2, help_text="内存大小(GB)")
    disk_capacity = models.DecimalField("磁盘容量(GB)", max_digits=10, decimal_places=2, help_text="磁盘容量(GB)")
    sn = models.CharField("序列号", max_length=128, unique=True, db_index=True, help_text="序列号")
    uuid = models.CharField("UUID", max_length=128, unique=True, db_index=True, blank=True, null=True,help_text="UUID")
    productmodel = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING, verbose_name="设备型号", null=True,
                                     max_length=32, help_text="设备型号")
    manufactory = models.ForeignKey(Manufactory, on_delete=models.DO_NOTHING, verbose_name="制造商", null=True,
                                    max_length=64, help_text="制造商")
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, verbose_name="供应商", null=True, max_length=12,
                                 help_text="供应商")
    idc = models.ForeignKey(Idc, on_delete=models.DO_NOTHING, verbose_name="所属IDC机房", max_length=16, null=True,
                            help_text="所属IDC机房")
    cabinet = models.ForeignKey(Cabinet, on_delete=models.DO_NOTHING, verbose_name="所属机柜", max_length=16, null=True,
                            help_text="所属机柜")
    remark = models.TextField("备注", null=True, max_length=255, help_text="备注")
    trade_date = models.DateField("购买日期", null=True, max_length=32, help_text="购买日期")
    expire_date = models.DateField("过保日期", null=True, max_length=32, help_text="过保日期")
    create_date = models.DateTimeField("创建时间", blank=True, null=True, auto_now_add=True, max_length=32,
                                       help_text="创建时间")
    update_date = models.DateTimeField("更新时间", blank=True, null=True, auto_now=True, max_length=32, help_text="更新时间")

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.ip_managemant


class Nic(models.Model):
    """
    网卡模型
    """
    nic_name = models.CharField("网卡名", max_length=16, help_text="网卡名")
    mac_address = models.CharField("MAC地址", max_length=64, help_text="MAC地址")
    server = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name="所属服务器", help_text="所属服务器")
    remark = models.TextField("备注", null=True, max_length=255, help_text="备注")

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.nic_name


class ServerIp(models.Model):
    """
    IP地址模型
    """
    ip_addr = models.GenericIPAddressField("ip地址", max_length=15, db_index=True, unique=True, help_text="ip地址")
    netmask = models.CharField("子网掩码", max_length=15, help_text="子网掩码")
    nic = models.ForeignKey(Nic, on_delete=models.CASCADE, verbose_name="所属网卡", help_text="所属网卡")
    remark = models.TextField("备注", null=True, max_length=255, help_text="备注")

    class Meta:
        verbose_name = 'IP地址'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.ip_addr
