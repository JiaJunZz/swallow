<template>
  <div class="dashboard-container">
    <el-table
      :data="tableData"
      stripe
      style="width: 100%">
      <el-table-column
        prop="username"
        label="用户名"/>
      <el-table-column
        prop="email"
        label="邮箱"/>
    </el-table>
    <div class="pagination">
      <el-pagination
        :current-page="currentPage1"
        :page-sizes="[10, 50, 100, 200]"
        :total="totalNum"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange">
      </el-pagination>
    </div>
  </div>
</template>

<script>
import { getUserList } from '@/api/dashboard'

export default {
  data() {
    return {
      tableData: [],
      totalNum: 0,
      currentPage1: 1,
      params: {
        page: 1,
        page_size: 10
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      getUserList(this.params).then(res => {
        this.tableData = res.results
        this.totalNum = res.count
      })
    },
    handleCurrentChange(val) {
      this.params.page = val
      this.fetchData()
    },
    handleSizeChange(val) {
      this.params.page_size = val
      this.fetchData()
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
.pagination {
  .el-pagination {
    text-align: center;
    margin-top: 10px;
  }
}
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
