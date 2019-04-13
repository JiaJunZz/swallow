<template>
  <div class="server-list">
    <el-table
      ref="listTable"
      :data="values"
      style="width: 100%"
      @selection-change="schange">
      <el-table-column
        type="selection"
        width="35">
      </el-table-column>
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item label="CPU型号">
              <span>{{ props.row.cpu_model }}</span>
            </el-form-item>
            <el-form-item label="逻辑CPU个数">
              <span>{{ props.row.cpu_logic_count }}</span>
            </el-form-item>
            <el-form-item label="网卡">
              <el-popover
                placement="left-start"
                width="550"
                trigger="hover">
                <el-table :data="props.row.nic">
                  <el-table-column width="80" property="nic_name" label="网卡名"></el-table-column>
                  <el-table-column width="140" property="mac_address" label="MAC地址"></el-table-column>
                  <el-table-column width="140" property="ip_addr" label="ip地址"></el-table-column>
                  <el-table-column width="140" property="netmask" label="子网掩码"></el-table-column>
                </el-table>
                <el-button slot="reference" type="text">{{ props.row.nic.length }}</el-button>
              </el-popover>
            </el-form-item>
            <el-form-item label="硬盘">
              <el-popover
                placement="right-start"
                width="200"
                trigger="hover">
                <el-table :data="props.row.driver">
                  <el-table-column width="80" property="driver_name" label="设备名"></el-table-column>
                  <el-table-column width="80" property="capacity" label="硬盘大小"></el-table-column>
                </el-table>
                <el-button slot="reference" type="text">{{ props.row.driver.length }}</el-button>
              </el-popover>
            </el-form-item>
            <el-form-item label="序列号">
              <span>{{ props.row.sn }}</span>
            </el-form-item>
            <el-form-item label="UUID">
              <span>{{ props.row.uuid }}</span>
            </el-form-item>
            <el-form-item label="制造商">
              <span v-if="props.row.manufactory"> {{ props.row.manufactory.manufactory_name }} </span>
              <span v-else> {{ props.row.manufactory }} </span>
            </el-form-item>
            <el-form-item label="设备型号">
              <span v-if="props.row.productmodel"> {{ props.row.productmodel.productmodel_name }} </span>
              <span v-else> {{ props.row.productmodel }} </span>
            </el-form-item>
            <el-form-item label="供应商">
              <span v-if="props.row.supplier"> {{ props.row.supplier.supplier_name }} </span>
              <span v-else> {{ props.row.supplier }} </span>
            </el-form-item>
            <el-form-item label="所属IDC机房">
              <span v-if="props.row.idc"> {{ props.row.idc.idc_name }} </span>
              <span v-else> {{ props.row.idc }} </span>
            </el-form-item>
            <el-form-item label="机柜">
              <span v-if="props.row.cabinet"> {{ props.row.cabinet.cabinet_name }} </span>
              <span v-else> {{ props.row.cabinet }} </span>
            </el-form-item>
            <el-form-item label="U位">
              <div v-for="(item, index) in props.row.uposition" :key="index" style="float:left">
                <span>{{ item.name }},</span>
              </div>
            </el-form-item>
            <el-form-item label="备注">
              <span>{{ props.row.remark }}</span>
            </el-form-item>
            <el-form-item label="进场日期">
              <span>{{ props.row.approach_date }}</span>
            </el-form-item>
            <el-form-item label="过保日期">
              <span>{{ props.row.expire_date }}</span>
            </el-form-item>
            <el-form-item label="创建时间">
              <span>{{ props.row.create_date }}</span>
            </el-form-item>
            <el-form-item label="更新时间">
              <span>{{ props.row.update_date }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        label="管理IP"
        min-width="180">
        <template slot-scope="scope">
          <span>{{ scope.row.ip_managemant }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="主机名"
        min-width="200">
        <template slot-scope="scope">
          <span>{{ scope.row.hostname }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作系统"
        min-width="150">
        <template slot-scope="scope">
          <span>{{ scope.row.os_type }} {{ scope.row.os_release }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="CPU核数*物理个数"
        min-width="180">
        <template slot-scope="scope">
          <span v-if="scope.row.cpu_core_count"> {{ scope.row.cpu_core_count }}*{{ scope.row.cpu_physics_count }} </span>
        </template>
      </el-table-column>
      <el-table-column
        label="内存大小(GB)"
        min-width="180">
        <template slot-scope="scope">
          <span>{{ scope.row.mem_capacity }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="150">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="serverEdit(scope.row)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="serverDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

export default {
  name: 'ServerList',
  props: {
    values: {
      type: Array,
      default: function() {
        return []
      }
    },
    mulselect: {
      type: Array,
      default: function() {
        return []
      }
    }
  },
  methods: {
    schange(val) {
      this.$emit('mulselect', val)
    },
    serverEdit(server) {
      this.$emit('edit', server)
    },
    serverDelete(server) {
      this.$confirm(`此操作将删除该${server.ip_managemant}服务器记录, 是否继续?`, '删除服务器', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('delete', server.id)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    }

  }
}

</script>

<style rel="stylesheet/scss" lang="scss" scoped>

  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>
