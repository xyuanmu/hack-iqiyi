# Hack-iqiyi
一款 Windows 下获取爱奇艺flash并输出 enc_key 的python小工具，自带精简版 python 2.7.8，无需另外安装。

## 软件说明：
* 支持平台：Windows
* 所需软件：chrome 内核浏览器
* 下载地址：[点击下载](https://github.com/xyuanmu/hack-iqiyi/archive/master.zip)

![hack-iqiyi](https://cloud.githubusercontent.com/assets/12442896/12503954/1223df2e-c114-11e5-8a4c-4e8205cb97d9.png)

## 使用方法：
* 首先安装 chrome 内核浏览器如 [七星浏览器](http://www.qixing123.com/)（以下简称浏览器），只要能安装第三方扩展即可。
* 运行浏览器，在地址栏输入：chrome://extensions，回车，将 Hack-iQiYi.crx 拖入窗口安装并启用。
* 运行 hack-iqiyi.bat，会自动下载flash文件并打补丁。
* 当CMD窗口出现：`Serving HTTP on 127.0.0.1 port 8036`，用浏览器播放爱奇艺视频，enc_key 会自动出来。
* 最后一步，到浏览器禁用 Hack-iQiYi，不然就无法正常播放了:smile:！

## 相关内容：
* Linux平台获取爱奇艺key：[yan12125/iqiyi-hack](https://github.com/yan12125/iqiyi-hack)
* PHP环境解析爱奇艺视频：[parseiqiyi](https://github.com/xyuanmu/parseiqiyi)
* python解析网站音乐和视频：[soimort/you-get](https://github.com/soimort/you-get)
