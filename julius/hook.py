import socket

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
    for line in res.split('\n'):
        # Juliusから取得した値から認識文字列の行を探す
        index = line.find('WORD=')
        if index != -1:
            # 認識文字列部分だけを抜き取る
            line = line[index + 6 : line.find('"', index + 6)]
            # 文字列の開始記号以外を格納していく
            if line != '[s]':
                word = word + line
                break
    if word != '':
        # ここで単語が出てくるので，ifなりなんなりで分岐させて処理を行う
        print(word)
    res = ''
