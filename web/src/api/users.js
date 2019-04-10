import request from '@/utils/request'

// 获取用户列表
export function getUserList(params) {
  return request({
    url: '/users/',
    method: 'get',
    params
  })
}

// 创建用户
export function createUser(params) {
  return request({
    url: '/users/',
    method: 'post',
    data: params
  })
}

// 更新用户
export function updateUser(params) {
  return request({
    url: '/users/' + params.id + '/',
    method: 'patch',
    data: params
  })
}

// 删除用户
export function deleteUser(id) {
  return request({
    url: '/users/' + id + '/',
    method: 'delete'
  })
}

// 更新用户的属组
export function updateUserGroup(id, data) {
  return request({
    url: '/usergroup/' + id + '/',
    method: 'patch',
    data
  })
}
