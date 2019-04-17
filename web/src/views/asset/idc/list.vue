<template>
  <div class="idclist">
    <el-table
      v-loading="loading"
      :data="values"
      style="width: 100%">
      <el-table-column
        label="机房名称"
        min-width="200">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="机房地址"
        min-width="200">
        <template slot-scope="scope">
          <span>{{ scope.row.address }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="机房电话"
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
            @click="idcEdit(scope.row)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="idcDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

export default {
  name: 'IdcList',
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
    idcEdit(idc) {
      this.$emit('edit', idc)
    },
    idcDelete(idc) {
      this.$confirm(`此操作将删除该${idc.name}IDC记录, 是否继续?`, '删除机房', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('delete', idc.id)
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
