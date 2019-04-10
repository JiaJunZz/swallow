<template>
  <div class="supplierlist">
    <el-table
      v-loading="loading"
      :data="values"
      style="width: 100%">
      <el-table-column
        label="供应商名称"
        min-width="200">
        <template slot-scope="scope">
          <span>{{ scope.row.supplier_name }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="供应商电话"
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
            @click="supplierEdit(scope.row)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="supplierDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

export default {
  name: 'SupplierList',
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
    supplierEdit(supplier) {
      this.$emit('edit', supplier)
    },
    supplierDelete(supplier) {
      this.$confirm(`此操作将删除该${supplier.supplier_name}供应商记录, 是否继续?`, '删除供应商', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('delete', supplier.id)
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
