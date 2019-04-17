<template>
  <div class="server">
    <el-row :gutter="20">
      <el-col :span="3" :offset="1">
        <div class="grid-content bg-purple">
          <el-button type="primary" size="small" @click="handleDialogCreate">新增服务器</el-button>
        </div>
      </el-col>
      <el-col :span="3">
        <div class="grid-content bg-purple">
          <el-select v-model="params.os_type" clearable size="small" placeholder="操作系统" @change="handleFilter">
            <el-option v-for="(item,index) in osList" :key="index" :label="item.os_type" :value="item.os_type" />
          </el-select>
        </div>
      </el-col>
      <el-col :span="3">
        <div class="grid-content bg-purple">
          <el-select v-model="params.supplier" clearable size="small" placeholder="供应商" @change="handleFilter">
            <el-option v-for="item in supplierOption" :key="item.id" :label="item.supplier_name" :value="item.id" />
          </el-select>
        </div>
      </el-col>
      <el-col :span="3">
        <div class="grid-content bg-purple">
          <el-select v-model="params.manufactory" clearable size="small" placeholder="制造商" @change="handleFilter">
            <el-option v-for="item in manufactoryOption" :key="item.id" :label="item.manufactory_name" :value="item.id" />
          </el-select>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="grid-content bg-purple">
          <el-input v-model="params.keywords" size="small" clearable placeholder="IP、SN、Hostname" class="input-with-select" @keyup.enter.native="handleFilter">
            <el-button slot="append" icon="el-icon-search" @click="handleFilter"></el-button>
          </el-input>
        </div>
      </el-col>
      <el-col :span="3"><div class="grid-content bg-purple"></div></el-col>
    </el-row>
    <server-list ref="serverListTable" :values="server" @mulselect="handleSelectionChange" @edit="handleDialogUpdate" @delete="handleDeleteServer"></server-list>
    <el-dialog
      :visible.sync="dialogVisibleCreate"
      title="新增服务器"
      width="40%">
      <server-form ref="serverCreateForm" :soption="supplierOption" :ioption="idcList" :bname="createString" @submit="handleSubmitCreate" @cancel="handleCreateCancel"></server-form>
    </el-dialog>
    <el-dialog
      :visible.sync="dialogVisibleUpdate"
      title="修改服务器信息"
      width="40%">
      <server-form ref="serverUpdateForm" :form="detailForm" :uarray="uList" :soption="supplierOption" :iarray="idcArray" :ioption="idcList" :bname="updateString" @submit="handleSubmitUpdate" @cancel="handleUpdateCancel"></server-form>
    </el-dialog>
    <el-row class="bottom-class">
      <el-col :span="1">
        <div class="grid-content bg-purple sel-count">
          {{ multipleSelection.length }} 选择
        </div>
      </el-col>
      <el-col :span="1">
        <div class="grid-content bg-purple">
          <el-button type="danger" size="mini" @click="handleMultiDeleteServer">删除</el-button>
        </div>
      </el-col>
      <el-col :span="8" :offset="6">
        <div class="pagination">
          <el-pagination
            :current-page="currentPage1"
            :page-sizes="[10, 20, 100, 200]"
            :total="totalNum"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange">
          </el-pagination>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getServerList, createServer, deleteServer, updateServer } from '@/api/server'
import { getSupplierList } from '@/api/supplier'
import { getManufactoryList } from '@/api/manufactory'
import { getIdcList } from '@/api/idc'

import ServerList from './list'
import ServerForm from './form'

export default {
  name: 'Server',
  components: { ServerList, ServerForm },
  data() {
    return {
      serverid: '',
      server: [],
      idcList: [],
      idcArray: [],
      uList: [],
      multipleSelection: [],
      manufactoryOption: [],
      supplierOption: [],
      osList: [],
      dialogVisibleCreate: false,
      dialogVisibleUpdate: false,
      detailForm: {},
      createString: '立即创建',
      updateString: '立即更新',
      totalNum: 0,
      currentPage1: 1,
      params2: {
        nopage: 1
      },
      params: {
        page: 1,
        keywords: '',
        page_size: 10,
        supplier: '',
        manufactory: '',
        os_type: ''
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      // 获取供应商列表
      getSupplierList(this.params2).then(
        res => {
          this.supplierOption = res.results
        }
      )
      // 获取制造商列表
      getManufactoryList(this.params2).then(
        res => {
          this.manufactoryOption = res.results
        }

      )
      getServerList(this.params).then(
        // 获取服务器列表
        res => {
          this.server = res.results
          this.totalNum = res.count
          this.osList = res.results.filter(item => item.os_type)
        },
        err => {
          this.$message({
            type: 'error',
            message: err.response.data.detail
          })
        }
      )
      // 获取IDC列表
      getIdcList(this.params2).then(
        res => {
          this.idcList = res.results
        }
      )
    },
    handleSubmitCreate(value) {
      // 创建服务器
      createServer(value).then(
        () => {
          this.fetchData()
          this.dialogVisibleCreate = false
          this.$refs.serverCreateForm.$refs.form.resetFields()
          this.$message({
            type: 'success',
            message: '创建成功'
          })
        },
        error => {
          this.$message({
            type: 'error',
            message: error.response
          })
        }
      )
    },
    handleSubmitUpdate(value) {
      // 更新服务器
      updateServer(value).then(
        () => {
          this.fetchData()
          this.dialogVisibleUpdate = false
          this.$refs.serverUpdateForm.$refs.form.resetFields()
          this.$message({
            type: 'success',
            message: '更新成功'
          })
        },
        err => {
          this.$message({
            type: 'error',
            message: err.response
          })
        })
    },
    handleDialogCreate(value) {
      // 弹出服务器新增弹框
      this.dialogVisibleCreate = true
    },
    handleDialogUpdate(value) {
      // 弹出服务器更新弹框
      this.idcArray = []
      this.dialogVisibleUpdate = true
      this.detailForm = value
      if (value.supplier === null || value.supplier === '') {
        this.detailForm.supplier = value.supplier
      } else {
        this.detailForm.supplier = value.supplier.supplier_id
      }
      if (this.detailForm.idc === null || this.detailForm.idc === '') {
        this.idcArray = []
      } else {
        this.idcArray = [this.detailForm.idc.idc_id, this.detailForm.cabinet.cabinet_id]
      }
      this.uList = this.detailForm.uposition.map(item => item.u_id)
    },
    handleDeleteServer(id) {
      // 删除Server
      deleteServer(id).then(
        () => {
          if (this.totalNum % this.params.page_size === 1) {
            this.params.page = this.params.page - 1
          }
          this.fetchData()
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
        },
        err => {
          this.$message({
            type: 'error',
            message: err.response.data.detail
          })
        }
      )
    },
    handleCurrentChange(val) {
      // 分页
      this.params.page = val
      this.fetchData()
    },
    handleSizeChange(val) {
      // 改变分页大小
      this.params.page_size = val
      this.fetchData()
    },
    handleCreateCancel() {
      // 取消创建
      this.dialogVisibleCreate = false
      this.fetchData()
    },
    handleUpdateCancel() {
      // 取消更新
      this.dialogVisibleUpdate = false
      this.fetchData()
    },
    handleFilter() {
      // 搜索
      this.params.page = 1
      this.fetchData()
    },
    handleSelectionChange(val) {
      // 获取表格多选的值
      this.multipleSelection = val
    },
    handleMultiDeleteServer() {
      // 批量删除
      if ((this.totalNum - this.multipleSelection.length) % this.params.page_size === 0) {
        this.params.page = this.params.page - 1
      }
      this.multipleSelection.forEach(
        (item, index) => {
          deleteServer(item.id).then(
            () => {
              this.fetchData()
              this.$message({
                type: 'success',
                message: '删除成功!'
              })
            })
        },
        err => {
          this.$message({
            type: 'error',
            message: err.response.data.detail
          })
        })
      this.$refs.serverListTable.$refs.listTable.clearSelection()
    }
  }
}

</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.server {
  padding: 10px;
  margin-top: 10px;
}
  .el-col {
    border-radius: 4px;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
.bottom-class {
  margin-top: 10px;
}
  .sel-count {
    font-size: 12px;
    margin-top: 7px;
  }
.pagination {
  .el-pagination {
    text-align: center;

    }
  }
</style>
