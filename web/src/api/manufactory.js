import request from '@/utils/request'

// 获取制造商列表
export function getManufactoryList(params) {
  return request({
    url: '/manufactory/',
    method: 'get',
    params
  })
}

// 创建制造商
export function createManufactory(params) {
  return request({
    url: '/manufactory/',
    method: 'post',
    data: params
  })
}

// 删除制造商
export function deleteManufactory(id) {
  return request({
    url: '/manufactory/' + id + '/',
    method: 'delete'
  })
}

// 更新制造商
export function updateManufactory(params) {
  return request({
    url: '/manufactory/' + params.id + '/',
    method: 'patch',
    data: params
  })
}
