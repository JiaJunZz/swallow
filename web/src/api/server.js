import request from '@/utils/request'

// 获取server列表
export function getServerList(params) {
  return request({
    url: '/server/',
    method: 'get',
    params
  })
}

// 创建server
export function createServer(params) {
  return request({
    url: '/server/',
    method: 'post',
    data: params
  })
}

// 删除服务器
export function deleteServer(id) {
  return request({
    url: '/server/' + id + '/',
    method: 'delete'
  })
}

// 更新服务器
export function updateServer(params) {
  return request({
    url: '/server/' + params.id + '/',
    method: 'patch',
    data: params
  })
}
