<template>
  <div class="supplier">
    <el-button type="primary" size="mini" @click="dialogVisibleCreate = true">创建供应商</el-button>
    <supplier-list :values="supplier" :loading="loading" @edit="handleUpdate" @delete="handleDelete"></supplier-list>
    <el-dialog
      :visible.sync="dialogVisibleCreate"
      title="创建供应商"
      width="50%">
      <supplier-form ref="supplierCreateForm" :value="createString" @submit="handleSubmitCreate" @cancel="handleCreateCancel"></supplier-form>
    </el-dialog>
    <el-dialog
      :visible.sync="dialogVisibleUpdate"
      title="修改供应商信息"
      width="50%">
      <supplier-form :form="detailForm" :value="updateString" @submit="handleSubmitUpdate" @cancel="handleUpdateCancel"></supplier-form>
    </el-dialog>
    <div class="pagination">
      <el-pagination
        :current-page="currentPage1"
        :total="totalNum"
        layout="total, prev, pager, next"
        @current-change="handleCurrentChange">
      </el-pagination>
    </div>
  </div>
</template>

<script>
import { getSupplierList, createSupplier, updateSupplier, deleteSupplier } from '@/api/supplier'
import SupplierList from './list'
import SupplierForm from './form'

export default {
  name: 'Supplier',
  components: { SupplierList, SupplierForm },
  data() {
    return {
      supplier: [],
      dialogVisibleCreate: false,
      dialogVisibleUpdate: false,
      loading: true,
      detailForm: {},
      createString: '立即创建',
      updateString: '立即更新',
      totalNum: 0,
      currentPage1: 1,
      params: {
        page: 1
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      // 获取供应商列表
      getSupplierList(this.params).then(
        res => {
          this.supplier = res.results
          this.totalNum = res.count
          this.loading = false
        },
        err => {
          this.$message({
            type: 'error',
            message: err.response.data.detail
          })
        }
      )
    },
    handleSubmitCreate(value) {
      // 创建供应商
      createSupplier(value).then(
        () => {
          if (this.totalNum % this.params.page_size === 1) {
            this.params.page = this.params.page - 1
          }
          this.fetchData()
          this.dialogVisibleCreate = false
          this.$refs.supplierCreateForm.$refs.form.resetFields()
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
      // 更新供应商
      updateSupplier(value).then(
        () => {
          this.fetchData()
          this.dialogVisibleUpdate = false
          this.$message({
            type: 'success',
            message: '更新成功'
          })
        },
        err => {
          this.$message({
            type: 'error',
            message: err.response.data.detail
          })
        })
    },
    handleUpdate(value) {
      // 更新供应商对话框
      this.dialogVisibleUpdate = true
      this.detailForm = value
    },
    handleDelete(id) {
      // 删除供应商
      deleteSupplier(id).then(
        () => {
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
    handleCreateCancel() {
      // 创建取消按钮
      this.dialogVisibleCreate = false
      this.fetchData()
    },
    handleUpdateCancel() {
      // 更新取消按钮
      this.dialogVisibleUpdate = false
      this.fetchData()
    }
  }
}

</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.supplier {
  padding: 10px;
}
  .pagination {
    .el-pagination {
      text-align: center;
      margin-top: 10px;
    }
  }
</style>
