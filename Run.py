from AddMusic import AddMusic

ACCOUNT = ""    # 输入手机号/邮箱
PASSWORD = ""   # 输入密码
PLAYLIST = ""   # 添加的播放列表名称
SONGLIST_FILE_PATH = './songlist/songlist.txt' # 存放歌曲名称目录

def load_songlist(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        songlist = [line.strip() for line in file if line.strip()]
    return songlist

def main():
    songlist = load_songlist(SONGLIST_FILE_PATH)
    user = AddMusic(account=ACCOUNT, password=PASSWORD, songlist=songlist, playlist=PLAYLIST)
       
    user.Setup_driver()
    user.AM_login()
    user.SearchAdd()

if __name__ == "__main__":
    main()

