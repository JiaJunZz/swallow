<template>
  <div class="user">
    <div class="header-class">
      <el-row :gutter="20">
        <el-col :span="6"><div class="grid-content bg-purple">
          <el-button type="primary" size="mini" @click="dialogVisibleCreate = true">创建用户</el-button>
        </div>
        </el-col>
        <el-col :span="8"><div class="grid-content bg-purple"></div></el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">
            <el-input v-model="params.keywords" placeholder="请输入内容" class="input-with-select" @keyup.enter.native="handleFilter">
              <el-button slot="append" icon="el-icon-search" @click="handleFilter"></el-button>
            </el-input>
          </div>
        </el-col>
        <el-col :span="4"><div class="grid-content bg-purple"></div></el-col>
      </el-row>
      <user-list :values="user" :loading="loading" @edit="handleUpdate" @editGroup="handleUpdateGroup" @editPass="handelChangePass" @delete="handleDelete"></user-list>
      <el-dialog
        :visible.sync="dialogVisibleCreate"
        title="创建用户"
        width="50%">
        <user-form ref="userCreateForm" :value="createString" @submit="handleSubmitCreate" @cancel="handleCreateCancel"></user-form>
      </el-dialog>
      <el-dialog
        :visible.sync="dialogVisibleUpdate"
        title="修改用户信息"
        width="50%">
        <user-form :form="detailForm" :value="updateString" @submit="handleSubmitUpdate" @cancel="handleUpdateCancel"></user-form>
      </el-dialog>
      <el-dialog
        :visible.sync="dialogVisibleGroup"
        title="更改用户组"
        width="50%">
        <update-ugroup :form="detailForm" :glist.sync="groupList" :goption="groupOption" @submit="handleSubmitUpdateUserGroup" @cancel="handleGroupCancel"></update-ugroup>
      </el-dialog>
      <el-dialog
        :visible.sync="dialogVisiblePass"
        title="修改密码"
        width="50%">
        <change-pass :form="passForm" @submit="handleChangeUserPass" @cancel="handleChangePassCancel"></change-pass>
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
</div></template>

<script>
import { getUserList, createUser, updateUser, deleteUser, updateUserGroup, changeUserPass } from '@/api/users'
import { getGroupList } from '@/api/groups'
import UserList from './user-list'
import UserForm from './user-form'
import UpdateUgroup from './update-ugroup'
import ChangePass from './change-upass'

export default {
  name: 'User',
  components: { UserList, UserForm, UpdateUgroup, ChangePass },
  data() {
    return {
      groupList: [],
      groupOption: [],
      user: [],
      dialogVisibleCreate: false,
      dialogVisibleUpdate: false,
      dialogVisibleGroup: false,
      dialogVisiblePass: false,
      loading: true,
      passForm: {},
      detailForm: {},
      createString: '立即创建',
      updateString: '立即更新',
      totalNum: 0,
      currentPage1: 1,
      params: {
        page: 1,
        keywords: '',
        page_size: 10
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      getUserList(this.params).then(
        // 获取user列表信息
        res => {
          this.user = res.results
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
      // 创建用户
      createUser(value).then(
        () => {
          this.fetchData()
          this.$refs.userCreateForm.$refs.form.resetFields()
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
      // 更新用户信息
      updateUser(value).then(
        () => {
          this.dialogVisibleUpdate = false
          this.fetchData()
          this.$message({
            type: 'success',
            message: '更新成功'
          })
        },
        error => {
          this.$message({
            type: 'error',
            message: error.response.data.detail
          })
        })
    },
    handleSubmitUpdateUserGroup(id, value) {
      // 更新用户属组事件
      updateUserGroup(id, value).then(
        () => {
          this.dialogVisibleGroup = false
          this.fetchData()
          this.$message({
            type: 'success',
            message: '更新成功'
          })
        },
        error => {
          this.$message({
            type: 'error',
            message: error.response.data.detail
          })
        }
      )
    },
    handleUpdate(value) {
      // 更新用户弹框显示
      this.dialogVisibleUpdate = true
      this.detailForm = value
    },
    handleUpdateGroup(value) {
      // 更新用户属组
      this.groupList = []
      this.detailForm = value
      this.dialogVisibleGroup = true
      getGroupList().then(
        // 获取所有用户组列表
        res => {
          this.groupOption = res.results
        }
      )
      this.groupList = value.groups.map(item => item.id)
    },
    handleDelete(id) {
      deleteUser(id).then(
        // 删除用户
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
    handleChangeUserPass(id, value) {
      // 修改用户密码
      changeUserPass(id, value).then(
        () => {
          this.dialogVisiblePass = false
          this.fetchData()
          this.$message({
            type: 'success',
            message: '修改成功'
          })
        },
        error => {
          this.$message({
            type: 'error',
            message: error.response.data
          })
        }
      )
    },
    handelChangePass(value) {
      // 修改密码弹窗
      this.dialogVisiblePass = true
      this.passForm = value
    },
    handleChangePassCancel() {
      this.dialogVisiblePass = false
      this.fetchData()
    },
    handleCreateCancel() {
      // 创建用户取消按钮
      this.dialogVisibleCreate = false
      this.fetchData()
    },
    handleUpdateCancel() {
      // 更新用户取消按钮
      this.dialogVisibleUpdate = false
      this.fetchData()
    },
    handleGroupCancel() {
      // 更细属组取消按钮
      this.dialogVisibleGroup = false
      this.fetchData()
    },
    handleCurrentChange(val) {
      // 分页
      this.params.page = val
      this.fetchData()
    },
    handleFilter() {
      // 搜索
      this.params.page = 1
      this.fetchData()
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.user {
  padding: 10px;
}
  .header-class {
    margin-top: 10px;
  }
    .el-col {
      border-radius: 4px;
    }
    .grid-content {
      border-radius: 4px;
      min-height: 36px;
    }
  .pagination {
    .el-pagination {
      text-align: center;
      margin-top: 10px;
    }
  }
</style>
