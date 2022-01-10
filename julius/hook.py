# coding: UTF-8
import socket

# Juliusに接続する準備
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 10500))

res = ''
while True:
    # 音声認識の区切りである「改行+.」がくるまで待つ
    while (res.find('\n.') == -1):
        # Juliusから取得した値を格納していく
        res += sock.recv(1024).decode('utf-8')
    word = ''
    for line in res.split('/>'):
        # Juliusから取得した値から認識文字列の行を探す
        index = line.find('WORD=')
        if index != -1:
            # 認識文字列部分だけを抜き取る
            recog = line[index + 6 : line.find('"', index + 6)]
            # 文字列の開始記号以外を格納していく
            if recog != "を".decode('utf-8'):
                word += recog
        if word != '':
            word = word[3:-4]
            # ここで単語が出てくるので，ifなりなんなりで分岐させて処理を行う
            print("word"+word)
            if word == "あぶらかたぶら音楽鳴らして".decode('utf-8'):
                print("音楽を流す")
            if word == "あぶらかたぶら時刻教えて".decode('utf-8'):
                print("時刻を表示する")
            if word == "あぶらかたぶら干支教えて".decode('utf-8'):
                print("干支を表示する")
            if word == "あぶらかたぶら月齢教えて".decode('utf-8'):
                print("月齢を表示する")
    res = ''