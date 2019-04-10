import request from '@/utils/request'

export function login(username, password) {
  return request({
    url: '/api-token-auth/',
    method: 'post',
    data: {
      username,
      password
    }
  })
}

export function getInfo(token) {
  return request({
    url: '/users/',
    method: 'get',
    params: { token }
  })
}

