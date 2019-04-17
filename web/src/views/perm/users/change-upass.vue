<template>
  <div>
    <el-form ref="form" :model="form" label-width="100px" class="change-pass">
      <el-form-item v-if="is_superuser == false" label="旧密码" prop="old_password">
        <el-input v-model="form.old_password"></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="new_password">
        <el-input v-model="form.new_password"></el-input>
      </el-form-item>
      <el-form-item class="button-right">
        <el-button size="small" @click="cancelForm">取消</el-button>
        <el-button size="small" type="primary" @click="submitForm">更新</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'ChangePass',
  props: {
    form: {
      type: Object,
      default: function() {
        return {
          old_password: '',
          new_password: ''
        }
      }
    }
  },
  data() {
    return {
    }
  },
  computed: {
    ...mapGetters([
      'is_superuser'
    ])
  },
  methods: {
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.$emit('submit', this.form.id, this.form)
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
.update-ugroup {
  position: relative;
  display: block
  }
    .button-right {
      text-align: right;
  }
</style>
