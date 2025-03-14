# Apple-Music-Playlist-Auto-Adder
自动登录网页版 Apple Music 并根据歌曲名称目录自动搜索歌曲并添加到自定义播放列表中。

## 使用方法
先安装 Selenium :
```bash
pip install selenium
```
下载 [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH)，选择和当前 Edge 版本相同的驱动版本，解压至 Python 的环境目录下<br>

在 Run.py 中输入账号密码与待添加的播放列表名称:
```bash
ACCOUNT = ""    # 输入手机号/邮箱
PASSWORD = ""   # 输入密码
PLAYLIST = ""   # 添加的播放列表名称
```

在 songlist 目录下的 songlist.txt 文件中存放想要添加的歌曲的名称（最好带上作者名称），如：
```bash
LOVE 2000-Anna Yanami
恋ひ恋ふ縁
富士山下
...
```

运行代码:
```bash
python Run.py
```

## 注意事项
* 运行后会自动输入账号密码并确认，若开启了 Apple 的二次验证则会要求输入验证码，手动输入验证码后点击 *信任* 即可，cookie会自动保存，下次启动无需登录
* 若登录时显示 *注册 Apple 账户* ，那么可能是官网服务器抽风了，请关闭浏览器重新运行程序

