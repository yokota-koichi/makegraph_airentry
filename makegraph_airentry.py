"""
大気突入試験レポートに使用するグラフを作成するプログラム
もうちょっと汎用性を高めたいなあ
GA87-1529-36で使用

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import re

# グラフ描画サブルーチン
def make_graph(file_path, x, y, xlabel, ylabel, xlim, ylim):
    # ここからグラフ描画用のプログラム，詳しくはmatplotlibでググってください
    # plt.figureでグラフ記入用の紙を用紙して，add_subplotでグラフエリア，つまり縦軸と横軸の四角を作る感じです
    fig = plt.figure(figsize=(6.4,4.8), tight_layout=True)
    # 111というのは縦に1分割，横に1分割したときの1つ目の（この時は1つしかないが）のグラフをaxに返しています
    ax = fig.add_subplot(111, xlabel=xlabel, ylabel=ylabel, xlim = xlim, ylim = ylim)
    ax.plot(x,y)
    plt.savefig(file_path)
    # closeとclfでグラフを閉じてメモリ開放．closeだけではメモリが完全に開放できないらしいからclfもしている．
    plt.close()
    plt.clf()



"""以下からメイン関数"""

# FFTフォルダ配下のディレクトリを取得
# top_path = ['X1', 'Y2Z']
top_path = os.listdir('FFT')

# X1内のファイルを処理してからY2Z内のファイルを処理
for i in top_path:
    # txtファイルのファイル名をリストで取得
    dir_path = os.listdir('FFT/%s' %i)

    # 後の分類を楽にするために，dir_pathリストのすべての要素（文字列）を小文字に変換している
    # for s in リストはリストの要素を1個ずつ見ていく感じです
    dir_path = [s.lower() for s in dir_path ]

    # X1のデータから不必要なデータを削除
    for s in dir_path:
        if 'x1' in s:
            # ファイル名をまず「_」で分割．そして最後のかたまり（例：acc001.txt）から数値のみを抽出
            # 正規表現好きじゃないからなにかいい方法を見つけたい
            num = re.findall(r'[0-9]{3}', s.split('_')[-1])
            # 文字列型のままなのでint型に変換
            num = int(num[0])
            # 末尾の数字が偶数のものをリストから削除
            if num % 2 == 0:
                dir_path.remove(s)




    # 周波数応答に使うデータのファイル名リスト
    # dir_pathからtxtファイル名をリストで取得し，その中からbf，4th，afが含まれるもののみ抜き出す
    freq_file_path = [s for s in dir_path if 'bf' in s or 'aft' in s or '4th' in s]

    # 時間波形に使うデータのファイル名リスト
    # airという文字がファイル名の先頭にもついているため，ファイル名を「_」で区切った時の最後の文字列のかたまりからairを探している
    time_file_path = [s for s in dir_path if 'air' in s.split('_')[-1]]


    # 周波数応答曲線作成
    for j in freq_file_path:
        # グラフの保存先のパス
        file_name = j.split('.')[0]
        save_path = 'fig/frequency_response/%s.jpg' %file_name

        # txtファイルの中身をデータフレームとして読み込み．最初の16行は飛ばしている
        df = pd.read_csv('FFT/%s/%s' %(i,j),header=None, skiprows=16, encoding='shift-jis')
        # OVERALLとなっている行を削除（0列目がOVERALLになっていない(!=はノットイコールの意味)行のみを抜き出している）
        df = df[df[0]!='OVERALL'].astype(float)
        # 1列目をx，2列目をyとする
        x = df[0]
        y = df[1]
        # グラフのメモリや軸の設定
        xlabel = 'Frequency [Hz]'
        ylabel = 'Mag [dBV]'
        xlim = (0,2001)
        # ピークホールドとスペクトルで縦軸の幅を変えている
        if 'nor' in j:
            ylim = (-140,-30)
        else :
            ylim = (-100,-20)

        # グラフ作成のサブルーチンを呼び出す
        make_graph(save_path, x, y, xlabel, ylabel, xlim, ylim)



    # 時間波形グラフ作成
    for j in time_file_path:
        # グラフの保存先のパス
        file_name = j.split('.')[0]
        save_path = 'fig/time_wave/%s.jpg' %file_name

        df = pd.read_csv('FFT/%s/%s' %(i,j),header=None, skiprows=16, encoding='shift-jis')
        # OVERALLとなっている行を削除（0列目がOVERALLになっていない行のみを抜き出している）
        df = df[df[0]!='OVERALL'].astype(float)
        x = df[0]
        y = df[1]
        # グラフのメモリや軸の設定
        xlabel = 'Frequency [Hz]'
        ylabel = 'Mag [dBV]'
        xlim = (-0.5,16.5)
        ylim=(-0.8,0.8)
        xlabel='Time [s]'
        ylabel='Mag[V]'
        # グラフ作成のサブルーチンを呼び出す
        make_graph(save_path, x, y, xlabel, ylabel, xlim, ylim)
