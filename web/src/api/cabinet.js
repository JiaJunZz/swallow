import request from '@/utils/request'

// 获取IDC列表
export function getIdcCabinet(params) {
  return request({
    url: '/idc/',
    method: 'get',
    params
  })
}

// 新增Cabinet
export function getCreateCabinet(params) {
  return request({
    url: '/cabinet/',
    method: 'post',
    data: params
  })
}

// 删除Cabinet
export function deleteCabinet(id) {
  return request({
    url: '/cabinet/' + id + '/',
    method: 'delete'
  })
}

