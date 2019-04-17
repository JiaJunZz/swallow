<template>
  <div class="group">
    <div class="header-class">
      <el-row :gutter="20">
        <el-col :span="6"><div class="grid-content bg-purple">
          <el-button type="primary" size="mini" @click="dialogVisibleCreate = true">创建用户组</el-button>
        </div>
        </el-col>
        <el-col :span="8"><div class="grid-content bg-purple"></div></el-col>
        <el-col :span="6">
          <div class="grid-content bg-purple">
            <el-input v-model="params.name" placeholder="请输入内容" class="input-with-select" @keyup.enter.native="handleFilter">
              <el-button slot="append" icon="el-icon-search" @click="handleFilter"></el-button>
            </el-input>
          </div>
        </el-col>
        <el-col :span="4"><div class="grid-content bg-purple"></div></el-col>
      </el-row>
      <group-list :values="group" :loading="loading" @edit="handleUpdate" @editPerm="handleEditPerm" @delete="handleDelete" @list="handlelistMember"></group-list>
      <el-dialog
        :visible.sync="dialogVisibleCreate"
        title="创建用户"
        width="50%">
        <group-form ref="gform" :value="createString" @submit="handleSubmitCreate" @cancel="handleCreateCancel"></group-form>
      </el-dialog>
      <el-dialog
        :visible.sync="dialogVisibleUpdate"
        title="修改用户信息"
        width="50%">
        <group-form :form="detailForm" :value="updateString" @submit="handleSubmitUpdate" @cancel="handleUpdateCancel"></group-form>
      </el-dialog>
      <div class="pagination">
        <el-pagination
          :current-page="currentPage1"
          :total="totalNum"
          layout="total, prev, pager, next"
          @current-change="handleCurrentChange">
        </el-pagination>
      </div>
      <el-dialog
        :visible.sync="dialogVisibleUser"
        :title="groupname"
        width="50%">
        <group-member :values="member" @delete="handleDeleteGroupMember"></group-member>
      </el-dialog>
      <el-dialog
        :visible.sync="dialogVisiblePerm"
        :title="perDialogTitle"
        width="60%">
        <group-perm ref="permform" :form="groupForms" :values="groupPerms" :list="permsList" @submit="handleSubmitGroupPerm" @cancel="handlePermCancel"></group-perm>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { getGroupList, createGroup, updateGroup, deleteGroup, deleteGroupMember, getPermission, updateGroupPerm } from '@/api/groups'
import GroupList from './group-list'
import GroupForm from './group-form'
import GroupMember from './group-member'
import GroupPerm from './group-perm'

export default {
  name: 'Group',
  components: { GroupList, GroupForm, GroupMember, GroupPerm },
  data() {
    return {
      groupForms: [],
      group: [],
      member: [],
      permsList: [],
      groupname: '',
      perDialogTitle: '',
      groupid: '',
      groupPerms: [],
      dialogVisibleCreate: false,
      dialogVisibleUpdate: false,
      dialogVisibleUser: false,
      dialogVisiblePerm: false,
      loading: true,
      detailForm: {},
      createString: '立即创建',
      updateString: '立即更新',
      totalNum: 0,
      currentPage1: 1,
      params: {
        page: 1,
        name: '',
        page_size: 10
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      getGroupList(this.params).then(
        // 获取所有用户组
        res => {
          this.group = res.results
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
      // 创建用户组
      createGroup(value).then(
        () => {
          this.fetchData()
          this.$refs.gform.$refs.form.resetFields()
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
      // 编辑更新用户组
      updateGroup(value).then(
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
    handleEditPerm(value) {
      // 更新用户组的权限
      this.groupForms = value
      this.dialogVisiblePerm = true
      getPermission().then(
        res => {
          this.permsList = res
        },
        err => {
          this.$message({
            type: 'error',
            message: err.response.data.detail
          })
        }
      )
      this.perDialogTitle = value.name + '组权限修改'
      this.groupPerms = value.perm.map(item => item.id)
    },
    handleUpdate(value) {
      // 弹出用户组更新对话框
      this.dialogVisibleUpdate = true
      this.detailForm = value
    },
    handleDelete(id) {
      // 删除用户组
      deleteGroup(id).then(
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
    handleSubmitGroupPerm(id, value) {
      // 更新用户组权限
      updateGroupPerm(id, value).then(
        () => {
          this.dialogVisiblePerm = false
          this.fetchData()
          this.$message({
            type: 'success',
            message: '更新成功'
          })
        })
      this.$refs.permform.$refs.trans.clearQuery('left')
      this.$refs.permform.$refs.trans.clearQuery('right')
    },
    handlelistMember(value) {
      // 获取用户组成员列表
      this.groupname = value.name + '组成员列表'
      this.dialogVisibleUser = true
      this.member = value.users
      this.groupid = value.id
    },
    handleDeleteGroupMember(value) {
      // 删除用户组成员
      console.log(this.groupid)
      deleteGroupMember(this.groupid, value).then(
        () => {
          this.dialogVisibleUser = false
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
      // 分页跳转
      this.params.page = val
      this.fetchData()
    },
    handleFilter() {
      // 用户组搜索功能
      this.params.page = 1
      this.fetchData()
    },
    handleCreateCancel() {
      // 对话框取消实现
      this.dialogVisibleCreate = false
      this.fetchData()
    },
    handleUpdateCancel() {
      // 对话框取消实现
      this.dialogVisibleUpdate = false
      this.fetchData()
    },
    handlePermCancel() {
      // 对话框取消实现
      this.dialogVisiblePerm = false
      this.$refs.permform.$refs.trans.clearQuery('left')
      this.$refs.permform.$refs.trans.clearQuery('right')
      this.fetchData()
    }
  }
}

</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.group {
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
