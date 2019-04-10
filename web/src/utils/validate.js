/**
 * Created by jiachenpan on 16/11/18.
 */

export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

export function validAlphabetsSpecific(str) {
  // 校验存在问题，无法校验汉字以及其他问题,BUG
  const reg = /([A-Za-z@.+-_])/
  return reg.test(str)
}
