<template>
  <div class="idc">
    <el-button type="primary" size="mini" @click="dialogVisibleCreate = true">创建机房</el-button>
    <idc-list :values="idc" :loading="loading" @edit="handleUpdate" @delete="handleDelete"></idc-list>
    <el-dialog
      :visible.sync="dialogVisibleCreate"
      title="创建机房"
      width="50%">
      <idc-form ref="idcCreateForm" :value="createString" @submit="handleSubmitCreate" @cancel="handleCreateCancel"></idc-form>
    </el-dialog>
    <el-dialog
      :visible.sync="dialogVisibleUpdate"
      title="修改机房信息"
      width="50%">
      <idc-form :form="detailForm" :value="updateString" @submit="handleSubmitUpdate" @cancel="handleUpdateCancel"></idc-form>
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
import { getIdcList, createIdc, updateIdc, deleteIdc } from '@/api/idc'
import IdcList from './list'
import IdcForm from './form'

export default {
  name: 'Idc',
  components: { IdcList, IdcForm },
  data() {
    return {
      idc: [],
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
      getIdcList(this.params).then(
        // 获取IDC列表
        res => {
          this.idc = res.results
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
      // 创建IDC
      createIdc(value).then(
        () => {
          this.fetchData()
          this.dialogVisibleCreate = false
          this.$refs.idcCreateForm.$refs.form.resetFields()
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
      // 更新Idc
      updateIdc(value).then(
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
      // 弹出IDC更新弹框
      this.dialogVisibleUpdate = true
      this.detailForm = value
    },
    handleDelete(id) {
      // 删除IDC列表
      deleteIdc(id).then(
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
      // 取消创建
      this.dialogVisibleCreate = false
      this.fetchData()
    },
    handleUpdateCancel() {
      // 取消更新
      this.dialogVisibleUpdate = false
      this.fetchData()
    }
  }
}

</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.idc {
  padding: 10px;
}
  .pagination {
    .el-pagination {
      text-align: center;
      margin-top: 10px;
    }
  }
</style>
