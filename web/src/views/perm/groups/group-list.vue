<template>
  <div class="grouplist">
    <el-table
      v-loading="loading"
      :data="values"
      style="width: 100%">
      <el-table-column
        label="用户组名"
        min-width="150"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="成员"
      >
        <template slot-scope="scope">
          <el-button type="text" @click="groupMember(scope.row)">{{ scope.row.users.length }}</el-button>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="groupEdit(scope.row)">编辑</el-button>
          <el-button
            size="mini"
            type="primary"
            @click="permEdit(scope.row)">权限</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="groupDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: 'GroupList',
  props: {
    values: {
      type: Array,
      default: function() {
        return []
      }
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    groupEdit(group) {
      this.$emit('edit', group)
    },
    permEdit(group) {
      this.$emit('editPerm', group)
    },
    groupDelete(group) {
      this.$confirm(`此操作将删除该${group.name}用户记录, 是否继续?`, '删除机房', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('delete', group.id)
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    groupMember(group) {
      this.$emit('list', group)
    }

  }
}

</script>

<style rel="stylesheet/scss" lang="scss" scoped>

</style>
