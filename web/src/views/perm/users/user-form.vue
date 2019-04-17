<template>
  <div>
    <el-form ref="form" :model="form" :rules="rules" label-width="100px" class="user-form">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item label="姓名" prop="name">
        <el-input v-model="form.name" placeholder="请输入姓名"></el-input>
      </el-form-item>
      <el-form-item label="邮箱地址" prop="email">
        <el-input v-model="form.email" placeholder="请输入email"></el-input>
      </el-form-item>
      <el-form-item label="电话号码" prop="phone">
        <el-input v-model="form.phone" placeholder="请输入电话号码"></el-input>
      </el-form-item>
      <el-form-item class="button-right">
        <el-button size="small" @click="cancelForm">取消</el-button>
        <el-button size="small" type="primary" @click="submitForm">{{ value }}</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { validAlphabetsSpecific } from '@/utils/validate'

export default {
  name: 'UserForm',
  props: {
    form: {
      type: Object,
      default: function() {
        return {
          username: '',
          name: '',
          email: '',
          phone: '',
          password: ''
        }
      }
    },
    value: {
      type: String,
      required: true
    }
  },
  data() {
    var validateInput = (rule, value, callback) => {
      if (!validAlphabetsSpecific(value)) {
        callback(new Error('用户名只允许包括汉字，数字，字母及@.+-_'))
      } else {
        callback()
      }
    }
    return {
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { validator: validateInput, trigger: ['change', 'blur'] },
          { max: 150, message: '长度不能超过150个字符', trigger: 'blur' }
        ],
        name: [
          { max: 150, message: '长度不能超过150个字符', trigger: 'blur' }
        ],
        email: [
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        phone: [
          { max: 16, message: '长度不能超过16个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
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
.user-form {
  position: relative;
  display: block
  }
    .button-right {
      text-align: right;
  }
</style>
