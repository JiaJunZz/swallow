<template>
  <div class="manufactorylist">
    <el-table
      v-loading="loading"
      :data="values"
      style="width: 100%">
      <el-table-column
        label="制造商名称"
        min-width="200">
        <template slot-scope="scope">
          <span>{{ scope.row.manufactory_name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="制造商电话"
        min-width="200">
        <template slot-scope="scope">
          <span>{{ scope.row.phone }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="备注"
        min-width="200">
        <template slot-scope="scope">
          <span>{{ scope.row.remark }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="200">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="manufactoryEdit(scope.row)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="manufactoryDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

export default {
  name: 'ManufactoryList',
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
    manufactoryEdit(manufactory) {
      this.$emit('edit', manufactory)
    },
    manufactoryDelete(manufactory) {
      this.$confirm(`此操作将删除该${manufactory.manufactory_name}制造商记录, 是否继续?`, '删除制造商', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('delete', manufactory.id)
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

</style>
