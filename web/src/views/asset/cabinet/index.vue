<template>
  <div class="cabinet">
    <el-row>
      <el-col :span="8">
        <div class="block">
          <el-form :model="cabinetForm" label-width="100px" class="update-ugroup">
            <el-form-item label="IDC机房" prop="idc" >
              <el-select v-model="cabinetForm.idc" placeholder="请选择机房">
                <el-option
                  v-for="item in idcCabinet"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                  style="width: 190px"
                >
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="机柜号" prop="name" >
              <el-input
                v-model="cabinetForm.name"
                placeholder="请输入内容"
                clearable
                style="width: 200px"
              >
              </el-input>
            </el-form-item>
            <el-form-item class="button-right">
              <el-button size="small" type="primary" @click="handleCreateCabinet">增加</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-col>
      <el-col :span="8"><div class="grid-content bg-purple-light">
        <el-tree
          :data="idcCabinet"
          :props="defaultProps"
          accordion
        >
          <span slot-scope="{ node, data }" class="custom-tree-node">
            <span>{{ node.label }}</span>
            <span>

              <el-button
                type="text"
                size="mini"
                @click="() => remove(node, data)">
                删除
              </el-button>
            </span>
          </span>
        </el-tree>
      </div>
      </el-col>
    </el-row>

  </div>
</template>

<script>
import { getIdcCabinet, getCreateCabinet, deleteCabinet } from '@/api/cabinet'

export default {
  name: 'Cabinet',
  data() {
    return {
      params: {
        nopage: 1
      },
      idcCabinet: [],
      cabinetForm: {
        name: '',
        idc: ''
      },
      defaultProps: {
        children: 'idc_cab',
        label: 'name'
      },
      id: '',
      cname: ''
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      getIdcCabinet(this.params).then(
        // 获取IDC列表
        res => {
          this.idcCabinet = res.results
        },
        err => {
          this.$message({
            type: 'error',
            message: err.response.data.detail
          })
        }
      )
    },
    remove(node, data) {
      // 删除机柜
      if (node.isLeaf) {
        deleteCabinet(data.id).then(
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
      }
    },
    handleCreateCabinet() {
      // 创建机柜
      getCreateCabinet(this.cabinetForm).then(
        () => {
          this.fetchData()
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
    }
  }
}

</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.cabinet {
  padding: 10px;
  margin-top: 10px;
}
  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
  }

</style>
