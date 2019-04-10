import request from '@/utils/request'

// 获取IDC列表
export function getIdcList(params) {
  return request({
    url: '/idc/',
    method: 'get',
    params
  })
}

// 创建IDC
export function createIdc(params) {
  return request({
    url: '/idc/',
    method: 'post',
    data: params
  })
}

// 删除IDC
export function deleteIdc(id) {
  return request({
    url: '/idc/' + id + '/',
    method: 'delete'
  })
}

// 更新IDC
export function updateIdc(params) {
  return request({
    url: '/idc/' + params.id + '/',
    method: 'patch',
    data: params
  })
}
