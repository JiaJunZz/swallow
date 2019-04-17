<template>
  <div class="groupperm">
    <el-form ref="form" :model="form" label-width="100px" class="group-perm">
      <el-form-item label="组名" prop="name">
        <el-input v-model="form.name" :readonly="true" ></el-input>
      </el-form-item>
      <el-form-item label="用户组" prop="perm">
        <el-transfer
          ref="trans"
          v-model="permList"
          :data="list"
          :titles="['可选权限', '已选权限']"
          :props="{
            key: 'id',
            label: 'name'
          }"
          filterable
          filter-placeholder="请输入内容">
        </el-transfer>
      </el-form-item>
      <el-form-item class="button-right">
        <el-button size="small" @click="cancelForm">取消</el-button>
        <el-button size="small" type="primary" @click="submitForm">更新</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'GroupPerm',
  props: {
    form: {
      type: Object,
      default: function() {
        return {
          username: '',
          name: '',
          email: '',
          phone: ''
        }
      }
    },
    list: {
      type: Array,
      default: () => []
    },
    values: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      permList: this.values
    }
  },
  watch: {
    values() {
      this.permList = this.values
    }
  },
  methods: {
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.$emit('submit', this.form.id, this.permList)
        } else {
          return
        }
      })
    },
    cancelForm() {
      this.$emit('cancel')
    }
  }
}

</script>

<style lang="scss" scoped>
.group-perm {
  position: relative;
  display: block
  }
    .button-right {
      text-align: right;
  }
</style>
