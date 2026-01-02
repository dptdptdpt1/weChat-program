export default defineAppConfig({
  pages: [
    'pages/index/index',
    'pages/proposal/index',
    'pages/profile/index',
    'pages/event-detail/index'
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#fff',
    navigationBarTitleText: '宝利足球赛事通',
    navigationBarTextStyle: 'black'
  },
  tabBar: {
    color: '#999',
    selectedColor: '#1890ff',
    backgroundColor: '#fff',
    borderStyle: 'black',
    list: [
      {
        pagePath: 'pages/index/index',
        text: '首页'
      },
      {
        pagePath: 'pages/proposal/index',
        text: '今日方案'
      },
      {
        pagePath: 'pages/profile/index',
        text: '我的'
      }
    ]
  },
  // 启用按需注入
  lazyCodeLoading: 'requiredComponents'
})
