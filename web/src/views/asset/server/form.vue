<template>
  <div>
    <el-form ref="form" :model="form" :rules="rules" label-width="100px" class="server-form">
      <el-form-item label="管理IP" prop="ip_managemant">
        <el-input v-model="form.ip_managemant" placeholder="请输入管理IP"></el-input>
      </el-form-item>
      <el-form-item label="备注" prop="remark">
        <el-input v-model="form.remark" placeholder="请输入备注"></el-input>
      </el-form-item>
      <el-form-item label="供应商" prop="supplier">
        <el-select
          v-model="form.supplier"
          placeholder="请选择供应商"
          filterable
          allow-create
          style="width: 100%">
          <el-option
            v-for="item in soption"
            :key="item.id"
            :label="item.supplier_name"
            :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="机房区域">
        <div class="block">
          <el-row>
            <el-col :span="11">
              <el-form-item prop="areaArr">
                <el-cascader
                  :options="ioption"
                  :props="prop1"
                  v-model="areaArr"
                  expand-trigger="hover"
                  placeholder="请选择机柜"
                  style="width: 100%"
                ></el-cascader>
              </el-form-item>
            </el-col>
            <el-col :span="12" :offset="1">
              <el-form-item prop="uposition">
                <el-select
                  v-model="areaArr2"
                  style="width: 100%"
                  filterable
                  multiple
                  placeholder="请选择U位"
                >
                  <el-option
                    v-for="(item,index) in uoption"
                    :key="index"
                    :label="item.name"
                    :value="item.u_id"
                  ></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </div>
      </el-form-item>
      <el-form-item label="进场/过保日期">
        <el-row>
          <el-col :span="11">
            <el-form-item prop="approach_date">
              <el-date-picker
                v-model="form.approach_date"
                type="date"
                placeholder="选择进场日期"
                style="width: 100%"
                value-format="yyyy-MM-dd">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12" :offset="1">
            <el-form-item prop="expire_date">
              <el-date-picker
                v-model="form.expire_date"
                type="date"
                style="width: 100%;"
                placeholder="选择过保日期"
                value-format="yyyy-MM-dd">
              </el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form-item>
      <el-form-item class="button-right">
        <el-button size="small" @click="cancelForm">取消</el-button>
        <el-button size="small" type="primary" @click="submitForm">{{ bname }}</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>

export default {
  name: 'ServerForm',
  props: {
    form: {
      type: Object,
      default: function() {
        return {
          ip_managemant: '',
          remark: '',
          supplier: '',
          idc: '',
          cabinet: '',
          uposition: [],
          approach_date: '',
          expire_date: ''
        }
      }
    },
    bname: {
      type: String,
      required: true
    },
    soption: {
      type: Array,
      default: () => []
    },
    ioption: {
      type: Array,
      default: () => []
    },
    iarray: {
      type: Array,
      default: () => []
    },
    uarray: {
      type: Array,
      default: () => []
    }
  },
  data() {
    const getUoption = _ => {
      const data = []
      for (let i = 1; i <= 42; i++) {
        data.push({
          u_id: i,
          name: i
        })
      }
      return data
    }
    return {
      uoption: getUoption(),
      areaArr: this.iarray,
      areaArr2: this.uarray,
      prop1: {
        label: 'name',
        value: 'id',
        children: 'idc_cab'
      },
      rules: {
        ip_managemant: [
          { required: true, message: '请输入ip地址', trigger: 'blur' }],
        remark: [
          { max: 255, message: '长度不能超过255个字符', trigger: 'blur' }

        ]
      }
    }
  },
  watch: {
    iarray() {
      this.areaArr = this.iarray
    },
    uarray() {
      this.areaArr2 = this.uarray
    }
  },
  methods: {
    submitForm() {
      this.form.uposition = this.areaArr2
      this.form.idc = this.areaArr[0]
      this.form.cabinet = this.areaArr[1]
      if (this.form.approach_date === '' || this.form.approach_date === null) {
        delete this.form.approach_date
      }

      if (this.form.expire_date === '' || this.form.expire_date === null) {
        delete this.form.expire_date
      }
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
.server-form {
  position: relative;
  display: block
  }
  .button-right {
      text-align: right;
  }
</style>
