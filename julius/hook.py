import socket

def hook(output:str):
    # Juliusに接続する準備
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 10500))

    res = ''
    while True:
        # 音声認識の区切りである「改行+.」がくるまで待つ
        while (res.find('\n.') == -1):
            # Juliusから取得した値を格納していく
            res += sock.recv(1024).decode()
        word = ''
        for line in res.split('/>'):
            # Juliusから取得した値から認識文字列の行を探す
            index = line.find('WORD=')
            if index != -1:
                # 認識文字列部分だけを抜き取る
                recog = line[index + 6 : line.find('"', index + 6)]
                # 文字列の開始記号以外を格納していく
                if recog != "を":
                    word += recog
            if word != '':
                print(word)
                print(res)
                print(recog)
                word = word[3:-4]
                if word == "あぶらかたぶら音楽鳴らして":
                    output = "play_music"
                elif word == "あぶらかたぶら時刻教えて":
                    output = "show_time"
                elif word == "あぶらかたぶら干支教えて":
                    output = "show_zodiac"
                elif word == "あぶらかたぶら月齢教えて":
                    output = "show_moonage"
                else:
                    output = "unknown"
        res = ''
