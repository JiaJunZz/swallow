import request from '@/utils/request'

// 获取供应商列表
export function getSupplierList(params) {
  return request({
    url: '/supplier/',
    method: 'get',
    params
  })
}

// 创建供应商
export function createSupplier(params) {
  return request({
    url: '/supplier/',
    method: 'post',
    data: params
  })
}

// 删除供应商
export function deleteSupplier(id) {
  return request({
    url: '/supplier/' + id + '/',
    method: 'delete'
  })
}

// 更新供应商
export function updateSupplier(params) {
  return request({
    url: '/supplier/' + params.id + '/',
    method: 'patch',
    data: params
  })
}
