<template>
  <div>
    <el-form ref="form" :model="form" :rules="rules" label-width="100px" class="idc-form">
      <el-form-item label="用户组名" prop="name">
        <el-input v-model="form.name" placeholder="请输入组名"></el-input>
      </el-form-item>
      <el-form-item class="button-right">
        <el-button size="small" @click="cancelForm">取消</el-button>
        <el-button size="small" type="primary" @click="submitForm">{{ value }}</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>

export default {
  name: 'GroupForm',
  props: {
    form: {
      type: Object,
      default: function() {
        return {
          name: ''
        }
      }
    },
    value: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      rules: {
        name: [
          { required: true, message: '请输入机房名称', trigger: 'blur' },
          { max: 80, message: '长度不能超过80个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.$emit('submit', this.form)
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
.idc-form {
  position: relative;
  display: block
  }
    .button-right {
      text-align: right;
  }
</style>
