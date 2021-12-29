# julius

[このサイト](https://zenn.dev/minako_ph/articles/45503855f1f626)を参考にしてシステムをインストールしています．

1.  USB マイクとヘッドホンを Raspberry Pi に指す
    参考) ヘッドホンは，正しく音声が録音できているかを確認するために聴くときに使う．
    スピーカーでも OK．イヤホンジャックに指す．

1.  USB マイクが認識されているか確認する

    ```
    $ lsusb
    Bus 001 Device 005: ID 0d8c:8100 C-Media Electronics, Inc. USB PnP Sound Device
    Bus 001 Device 004: ID 0424:7800 Microchip Technology, Inc. (formerly SMSC)
    Bus 001 Device 003: ID 0424:2514 Microchip Technology, Inc. (formerly SMSC) USB 2.0 Hub
    Bus 001 Device 002: ID 0424:2514 Microchip Technology, Inc. (formerly SMSC) USB 2.0 Hub
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
    ```

    USB PnP Sound Device が追加されていれば認識されているっぽいです．

1.  USB マイクで録音できるか確認する

    1.  ハードウェアのカード番号とデバイス番号を確認する

        参考) `arecord`は録音するコマンド，`aplay`は再生するコマンド．
        Linux では録音を Capture，再生を Playback と言うらしい．

        ```
        $ arecord -l
        **** ハードウェアデバイス CAPTURE のリスト ****
        カード 1: Device [USB PnP Sound Device], デバイス 0: USB Audio [USB Audio]
          サブデバイス: 1/1
          サブデバイス #0: subdevice #0
        ```

        マイクは，カード番号が 1，デバイス番号が 0 であることを確認できる．（もしかしたら異なるかもしれないので，その場合はその値を覚えておく．）

        ```
        $ aplay -l
        **** ハードウェアデバイス PLAYBACK のリスト ****
        カード 0: Headphones [bcm2835 Headphones], デバイス 0: bcm2835 Headphones [bcm2835 Headphones]
          サブデバイス: 8/8
          サブデバイス #0: subdevice #0
          サブデバイス #1: subdevice #1
          サブデバイス #2: subdevice #2
          サブデバイス #3: subdevice #3
          サブデバイス #4: subdevice #4
          サブデバイス #5: subdevice #5
          サブデバイス #6: subdevice #6
          サブデバイス #7: subdevice #7
        カード 1: Device [USB PnP Sound Device], デバイス 0: USB Audio [USB Audio]
          サブデバイス: 1/1
          サブデバイス #0: subdevice #0
        カード 2: vc4hdmi [vc4-hdmi], デバイス 0: MAI PCM i2s-hifi-0 [MAI PCM i2s-hifi-0]
          サブデバイス: 1/1
          サブデバイス #0: subdevice #0
        ```

        ヘッドホンはカード番号が 0，デバイス番号が 0 であることを確認できる．（もしかしたら異なるかもしれないので，その場合はその値を覚えておく．）

    1.  ヘッドホン音量とマイク音量を 100%にする．

        ```
        $ alsamixer
        ```

        GUI っぽい画面が出るので，F3 と F4 で切り替えて，↑↓ キーでヘッドホン音量とマイク音量を最大にしておく．Esc で戻る．

    1.  マイクで音を録音する

        ```
        # plughw:[マイクのカード番号],[マイクのデバイス番号]にする
        $ arecord -D plughw:1,0 -f cd test.wav
        ```

        かっこよくマイクに向かって魔法を詠唱したら Ctrl+c で停止する．

    1.  音が録音できているか再生して確認する

        ```
        # hw:[ヘッドホンのカード番号],[ヘッドホンのデバイス番号]にする
        $ aplay -D hw:0,0 test.wav
        ```

        魔法の詠唱が聞こえたら OK．
        何も聞こえなかったら録音が失敗しているか，再生が失敗しているので，デバイスの確認などをしてください

1.  julius で入力するデバイスを環境変数に登録する

    ```
    $ sudo vim /etc/profile

    # 最後の行に次を追記する
    # plughw:[マイクのカード番号],[マイクのデバイス番号]にする
    export ALSADEV="plughw:1,0"
    ```

1.  julius システムをインストールする．
    以降はこの README.md が存在するディレクトリで実行することを想定する．

    ```
    # ソースコードのダウンロード
    $ wget https://github.com/julius-speech/julius/archive/v4.4.2.1.tar.gz
    $ tar xvzf v4.4.2.1.tar.gz
    $ cd julius-4.4.2.1

    # アップデート
    $ sudo apt-get update
    $ sudo apt-get upgrade

    # 必要なライブラリのインストール
    $ sudo apt-get install libasound2-dev libesd0-dev libsndfile1-dev

    # システムのコンパイルとインストール
    $ ./configure --with-mictype=alsa
    $ make
    $ sudo make install

    # インストールされているか確認する
    $julius --version
    JuliusLib rev.4.4.2.1 (fast)
    ...
    ```

1.  julius ディクテーションキットをインストールして動作確認を行う．
    以降はこの README.md が存在するディレクトリで実行することを想定する．

    ```
    # ソースコードのダウンロード
    $ wget https://osdn.net/dl/julius/dictation-kit-v4.4.zip
    $ unzip dictation-kit-v4.4.zip
    $ cd dictation-kit-v4.4

    # 音声認識デモを起動
    $ julius -C main.jconf -C am-gmm.jconf -demo
    ...
    <<< please speak >>>
    ```

    please speak と表示されたら成功なので，魔法の詠唱を行いましょう．
    大変精度が悪いですが，何かしら認識されます．
    Ctrl+c で停止．

1.  julius 用独自辞書データを作る．
    以降はこの README.md が存在するディレクトリで実行することを想定する．
    参考）`julius-4.4.2.1`フォルダが`generate_voca.py`と同じ階層に存在することを確認する

    1. `generate_voca.py`の`WORD_LIST`を変更することで認識する単語を編集できる．

       ```
       WORD_LIST = [
           ('MAHO1', 'ちちんぷいぷい'),
           ('MAHO2', 'あぶらかたぶら')
       ]
       ```

    1. julius 用の辞書データを次のプログラムで生成する．
       ```
       $ python3 generate_voca.py
       ```

1.  独自辞書データで認識を行う

    ```
    $ julius -C ./dictation-kit-v4.4/am-gmm.jconf -nostrip -gram ./custom/custom -input mic
    ```

    うまいこと認識出来たら OK

1.  julius を音声認識サーバーにする
    1. julius をサーバーとして建てる
       ```
       julius -C ./dictation-kit-v4.4/am-gmm.jconf -nostrip -gram ./custom/custom -input mic -module
       ```
    1. 別のターミナルを開いて，`hook.py`を実行する
       ` python hook.py `
       出力がきちんと表示されれば OK！
       julius をバックグラウンドプロセスとして実行するなり，サービスとして登録するなりすれば，音声認識が正しくできるようになるよ！
