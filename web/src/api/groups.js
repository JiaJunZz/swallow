import request from '@/utils/request'

// 获取用户组列表
export function getGroupList(params) {
  return request({
    url: '/groups/',
    method: 'get',
    params
  })
}

// 创建用户组
export function createGroup(params) {
  return request({
    url: '/groups/',
    method: 'post',
    data: params
  })
}

// 更新用户组
export function updateGroup(params) {
  return request({
    url: '/groups/' + params.id + '/',
    method: 'patch',
    data: params
  })
}

// 删除用户组
export function deleteGroup(id) {
  return request({
    url: '/groups/' + id + '/',
    method: 'delete'
  })
}

// 删除用户组的成员
export function deleteGroupMember(id, params) {
  return request({
    url: '/groupmember/' + id + '/',
    method: 'delete',
    data: params
  })
}

// 获取权限
export function getPermission() {
  return request({
    url: '/permission/',
    method: 'get'
  })
}

// 更新用户组权限
export function updateGroupPerm(id, params) {
  return request({
    url: '/groupperm/' + id + '/',
    method: 'patch',
    data: params
  })
}
