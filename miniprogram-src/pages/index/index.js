// pages/index/index.js
var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    motto: '开启你的复旦之旅',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    wxBind: false,
    first: true,
    searchValue: '',
    instruction: '选择你感兴趣的专业（可多选）：',
    tags: [
      {
        isChosen: false,
        text: '计算机科学'
      },
      {
        isChosen: false,
        text: '软件工程'
      },
      {
        isChosen: false,
        text: '微电子'
      },
      {
        isChosen: false,
        text: '通信工程'
      },
    ],
    chosenTags: [],
    current: "tuijian"
  },

  bindTagTap: function(event) {
    let text = event._relatedInfo.anchorTargetText
    let newTags = []
    for(let i=0; i<this.data.tags.length; i++){
      let tag = this.data.tags[i]
      if(tag.text === text){
        tag.isChosen = !tag.isChosen
        newTags.push(tag)
      }
      else{
        newTags.push(tag)
      }
    }
    this.setData({
      tags: newTags
    })
  },

  handleChange: function({detail}){
    this.setData({
      current: detail.key
    })
  },

  bindInput: function(e){
    this.setData({
      searchValue: e.detail.value
    })
  },

  bindSearch: function(){
    console.log(this.data.searchValue)
    app.globalData.searchValue = this.data.searchValue
    wx.navigateTo({
      url: '../search/search',
    })
  },

  bindConfirmTap: function(){
    let tagArray = []
    for (let i = 0; i < this.data.tags.length; i++) {
      let tag = this.data.tags[i]
      if(tag.isChosen){
        tagArray.push(tag.text)
      }
    }
    console.log(tagArray)
    this.setData({
      first: false
    })
    wx.showTabBar({})
  },

  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      wx.hideTabBar({})
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.hideTabBar({})
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true,
      wxBind: true
    })

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    this.setData({
      searchValue: ''
    })
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})