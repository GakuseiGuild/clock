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
    cm = ''
    for line in res.split('\n'):
        # Juliusから取得した値から認識文字列の行を探す
        index = line.find('WORD=')
        cmdex = line.find('CM=')
        if index != -1:
            # 認識文字列部分だけを抜き取る
            line_wd = line[index + 6 : line.find('"', index + 6)]
            line_cm = line[cmdex + 4 : line.find('"', cmdex + 6)]
            # 文字列の開始記号以外を格納していく
            if line_wd != '[s]':
                word = word + line_wd
                cm = cm + line_cm
                break
    if word != '':
        # ここで単語が出てくるので，ifなりなんなりで分岐させて処理を行う
        print(word)
        print(cm)
        if(cm == "1.000"):
            print('成功！')
    res = ''
