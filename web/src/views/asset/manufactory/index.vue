<template>
  <div class="manufactory">
    <el-button type="primary" size="mini" @click="dialogVisibleCreate = true">创建制造商</el-button>
    <manufactory-list :values="manufactory" :loading="loading" @edit="handleUpdate" @delete="handleDelete"></manufactory-list>
    <el-dialog
      :visible.sync="dialogVisibleCreate"
      title="创建制造商"
      width="50%">
      <manufactory-form ref="manufactoryCreateForm" :value="createString" @submit="handleSubmitCreate" @cancel="handleCreateCancel"></manufactory-form>
    </el-dialog>
    <el-dialog
      :visible.sync="dialogVisibleUpdate"
      title="修改制造商信息"
      width="50%">
      <manufactory-form :form="detailForm" :value="updateString" @submit="handleSubmitUpdate" @cancel="handleUpdateCancel"></manufactory-form>
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
import { getManufactoryList, createManufactory, updateManufactory, deleteManufactory } from '@/api/manufactory'
import ManufactoryList from './list'
import ManufactoryForm from './form'

export default {
  name: 'Manufactory',
  components: { ManufactoryList, ManufactoryForm },
  data() {
    return {
      manufactory: [],
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
      // 制造商列表
      getManufactoryList(this.params).then(
        res => {
          this.manufactory = res.results
          this.totalNum = res.count
          this.loading = false
        },
        error => {
          this.$message({
            type: 'error',
            message: error.response.data.detail
          })
        }
      )
    },
    handleSubmitCreate(value) {
      // 创建制造商
      createManufactory(value).then(
        () => {
          this.fetchData()
          this.$refs.manufactoryCreateForm.$refs.form.resetFields()
          this.dialogVisibleCreate = false
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
      // 更新制造商
      updateManufactory(value).then(
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
      // 更新制造商对话框
      this.dialogVisibleUpdate = true
      this.detailForm = value
    },
    handleDelete(id) {
      // 删除制造商
      deleteManufactory(id).then(
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
    handleCreateCancel() {
      this.dialogVisibleCreate = false
      this.fetchData()
    },
    handleUpdateCancel() {
      this.dialogVisibleUpdate = false
      this.fetchData()
    }
  }
}

</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.manufactory {
  padding: 10px;
  margin-top: 10px;
}
  .pagination {
    .el-pagination {
      text-align: center;
      margin-top: 10px;
    }
  }
</style>
