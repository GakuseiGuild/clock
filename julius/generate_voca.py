import os
import subprocess

# 音声認識したい単語とそのIDを組にして登録する．
WORD_LIST = [
    ('MAHO1', 'ちちんぷいぷい'),
    ('MAHO2', 'あぶらかたぶら'),
    ('GOMI1', 'あいうえお'),
    ('GOMI2', 'かきくけこ'),
    ('GOMI3', 'さしすせそ'),
    ('GOMI4', 'なにぬねの'),
    ('GOMI3', 'たちつてと'),
]

#### これ以降は変えなくて良い ####

# 認識単語辞書のファイル名
FILE_NAME = 'custom'


# FILE_NAMEフォルダを作成する
os.makedirs("./" + FILE_NAME, exist_ok=True)

BASIC_PATH = os.path.abspath(os.path.join(FILE_NAME, FILE_NAME))
YOMI_PATH = BASIC_PATH + ".yomi"
PHONE_PATH = BASIC_PATH + ".phone"
GRAMMAR_PATH = BASIC_PATH + ".grammar"
VOCA_PATH = BASIC_PATH + ".voca"

# 読みファイルを作成する
with open(YOMI_PATH, "w") as fp:
    for word in WORD_LIST:
        fp.write("{} {}\n".format(word[1], word[1]))

# コマンドで音素ファイルを生成する
subprocess.run("iconv -f utf8 -t eucjp {} | ./julius-4.4.2.1/gramtools/yomi2voca/yomi2voca.pl | iconv -f eucjp -t utf8 > {}".format(YOMI_PATH, PHONE_PATH), shell=True, text=True)

# 文法ファイルを作成する
with open(GRAMMAR_PATH, "w") as fp:
    fp.write("S : NS_B CMD NS_E\n")
    for word in WORD_LIST:
        fp.write("CMD : {}\n".format(word[0]))

# 音素ファイルから語彙ファイルを作成する
with open(PHONE_PATH, "r") as fp1:
    with open(VOCA_PATH, "w") as fp2:
        for word in WORD_LIST:
            fp2.write("% {}\n".format(word[0]))
            fp2.write(fp1.readline())
        fp2.write("% NS_B\n")
        fp2.write("[s] silB\n")
        fp2.write("% NS_E\n")
        fp2.write("[/s] silE\n")

# コマンドでdfaファイルを生成する
subprocess.run("cd ./julius-4.4.2.1/gramtools/mkdfa && mkdfa.pl {}".format(BASIC_PATH), shell=True, text=True)
