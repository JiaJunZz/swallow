import Vue from 'vue'
import Router from 'vue-router'

// in development-env not use lazy-loading, because lazy-loading too many pages will cause webpack hot update too slow. so only in production use lazy-loading;
// detail: https://panjiachen.github.io/vue-element-admin-site/#/lazy-loading

Vue.use(Router)

/* Layout */
import Layout from '../views/layout/Layout'

/**
* hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
* alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
*                                if not set alwaysShow, only more than one route under the children
*                                it will becomes nested mode, otherwise not show the root menu
* redirect: noredirect           if `redirect:noredirect` will no redirect in the breadcrumb
* name:'router-name'             the name is used by <keep-alive> (must set!!!)
* meta : {
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if false, the item will hidden in breadcrumb(default is true)
  }
**/
export const constantRouterMap = [
  { path: '/login', component: () => import('@/views/login/index'), hidden: true },
  { path: '/404', component: () => import('@/views/404'), hidden: true },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    name: 'Dashboard',
    children: [{
      path: 'dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: {
        title: '仪表盘',
        icon: 'dashboard'
      }
    }]
  },
  {
    path: '/asset',
    component: Layout,
    name: 'Asset',
    meta: {
      title: '资产管理',
      icon: 'table'
    },
    children: [
      {
        path: 'server',
        name: 'Server',
        component: () => import('@/views/asset/server/index'),
        meta: { title: '服务器' }
      },
      {
        path: 'idc',
        name: 'Idc',
        component: () => import('@/views/asset/idc/index'),
        meta: { title: 'IDC机房' }
      },
      {
        path: 'cabinet',
        name: 'Cabinet',
        component: () => import('@/views/asset/cabinet/index'),
        meta: { title: '机柜' }
      },
      {
        path: 'supplier',
        name: 'supplier',
        component: () => import('@/views/asset/supplier/index'),
        meta: { title: '供应商' }
      },
      {
        path: 'manufactory',
        name: 'manufactory',
        component: () => import('@/views/asset/manufactory/index'),
        meta: { title: '制造商' }
      }
    ]
  },
  {
    path: '/perm',
    component: Layout,
    meta: {
      title: '权限管理',
      icon: 'people'
    },
    children: [
      {
        path: 'user',
        name: 'Users',
        component: () => import('@/views/perm/users/index'),
        meta: { title: '用户管理' }
      },
      {
        path: 'group',
        name: 'Groups',
        component: () => import('@/views/perm/groups/index'),
        meta: { title: '组管理' }
      }
    ]
  },
  { path: '*', redirect: '/404', hidden: true }
]

export default new Router({
  // mode: 'history', //后端支持可开
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})
