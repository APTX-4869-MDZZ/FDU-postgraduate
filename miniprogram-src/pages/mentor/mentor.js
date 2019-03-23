// pages/mentor/mentor.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    nav: true,
    is_paper: true,
    papers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  },

  onPageScroll: function (event) {
    let _this = this;
    if (event.scrollTop > 100) {
      _this.setData({
        nav: false
      });
    } else {
      _this.setData({
        nav: true
      });
    }
  },

  handleChange: function ({ detail }) {
    let _this = this;
    if (detail.key === "tab1") {
      console.log('123');
      _this.setData({
        is_paper: true
      });
    } else {
      _this.setData({
        is_paper: false
      });
    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // wx.hideTabBar({});
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