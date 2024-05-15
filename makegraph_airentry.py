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

"""ユーザーが変更するパラメータ"""
# 試験回数
num_times = 10
# グラフの軸の調整．PHと加算平均でレンジが違うので変えている
xlim_spec = (0,2001)
ylim_spec_ph = (-100, -20)
ylim_spec_avg = (-140, -30)
xlim_time = (-0.5,16.5)
ylim_time = (-0.8,0.8)
# FFTのデータが入っているディレクトリ名
data_path = os.listdir('03_FFTdata')

# fftのテキストデータからX軸，y軸の値のみ取り出すサブルーチン
def data_trim(file_name):

    if "001" in file_name:
        df_x1 = pd.read_csv('03_FFTdata/%s' %file_name,header=None, skiprows=16, encoding='shift-jis')
    elif "002" in file_name:
        df_x2 = pd.read_csv('03_FFTdata/%s' %file_name,header=None, skiprows=16, encoding='shift-jis')
    elif "003" in file_name:
        df_y2 = pd.read_csv('03_FFTdata/%s' %file_name,header=None, skiprows=16, encoding='shift-jis')
    elif "004" in file_name:
        df_z = pd.read_csv('03_FFTdata/%s' %file_name,header=None, skiprows=16, encoding='shift-jis')

    df_list = [df_x1, df_x2, df_y2, df_z]

    # OVERALLとなっている行を削除（0列目がOVERALLになっていない(!=はノットイコールの意味)行のみを抜き出している）
    for i in range(len(df_list)):
        df_list[i] = df_list[i][df_list[i][0]!='OVERALL'].astype(float)

    x_y_list = []
    # [周波数_x1，Mag_x1，... ，周波数_z，Mag_z]のリストを作成
    for i in range(len(df_list)):
        x_y_list.append(df_list[i][0])
        x_y_list.append(df_list[i][1])

    return x_y_list


# グラフ描画サブルーチン
def make_graph(x_y_list, xlabel, ylabel, xlim, ylim, title):
    # ここからグラフ描画用のプログラム，詳しくはmatplotlibでググってください
    # plt.figureでグラフ記入用の紙を用紙して，add_subplotでグラフエリア，つまり縦軸と横軸の四角を作る感じです
    fig, ax = plt.subplots(2,2,figsize=(6.4,4.8))
    k = 0
    for i in range(2):
        for j in range(2):
            # 散布図をプロット
            ax[i,j].plot(x_y_list[2*k],x_y_list[2*k + 1])
            ax[i,j].set(xlabel = xlabel, ylabel = ylabel)
            ax[i,j].set(xlim = xlim, ylim = ylim)
            k += 1


    # グラフ個別のタイトル
    ax[0,0].set_title("X1")
    ax[0,1].set_title("X2")
    ax[1,0].set_title("Y2")
    ax[1,1].set_title("Z")

    # グラフ全体のタイトル
    fig.suptitle(title)

    plt.savefig("fig/" + title + ".pdf")
    # closeとclfでグラフを閉じてメモリ開放．closeだけではメモリが完全に開放できないらしいからclfもしている．
    plt.close()
    plt.clf()


"""以下からメイン関数"""

# 後の分類を楽にするために，dir_pathリストのすべての要素（文字列）を小文字に変換している
# for s in リストはリストの要素を1個ずつ見ていく感じです
data_path = [s.lower() for s in data_path ]


for i in num_times:

    # dir_pathからtxtファイル名をリストで取得し，その中からn回目のデータを取り出す
    times_file_path = [s for s in data_path if 'n%d' %i in s or "bf" in s or "af" in s]

    for file_name in times_file_path:
        if "in" in file_name:
            # 加速ピークホールドを処理
            if "acc" in file_name:
                if "bf" in file_name:
                    title = "吸気口 試験前 加速ピークホールド"
                elif "af" in file_name:
                    title = "吸気口 試験後 加速ピークホールド"
                else:
                    title = "吸気口 %d回目 加速ピークホールド" %i+1

                # 横軸，縦軸の数値のみ取り出す
                x_y_list = data_trim(file_name)
                # グラフ作成
                make_graph(x_y_list,"Frequency [Hz]", "Mag [dBV]" ,xlim_spec, ylim_spec_ph, title)

            # 定格スペクトルを処理
            elif "nor" in file_name:
                if "bf" in file_name:
                    title = "吸気口 試験前 定格スペクトル"
                elif "af" in file_name:
                    title = "吸気口 試験後 定格スペクトル"
                else:
                    title = "吸気口 %d回目 定格スペクトル" %i+1

                # 横軸，縦軸の数値のみ取り出す
                x_y_list = data_trim(file_name)

                # グラフ作成
                make_graph(x_y_list,"Frequency [Hz]", "Mag [dBV]" ,xlim_spec, ylim_spec_ph, title)

            # 減速ピークホールドを処理
            elif "nor" in file_name:
                if "bf" in file_name:
                    title = "吸気口 試験前 減速ピークホールド"
                elif "af" in file_name:
                    title = "吸気口 試験後 減速ピークホールド"
                else:
                    title = "吸気口 %d回目 減速ピークホールド" %i+1

                # 横軸，縦軸の数値のみ取り出す
                x_y_list = data_trim(file_name)

                # グラフ作成
                make_graph(x_y_list,"Frequency [Hz]", "Mag [dBV]" ,xlim_spec, ylim_spec_ph, title)

            # 時間波形を処理
            elif "air" in file_name:
                if "bf" in file_name:
                    title = "吸気口 試験前 大気突入 時間波形"
                elif "af" in file_name:
                    title = "吸気口 試験後 大気突入 時間波形"
                else:
                    title = "吸気口 %d回目 大気突入 時間波形" %i+1

                # 横軸，縦軸の数値のみ取り出す
                x_y_list = data_trim(file_name)

                # グラフ作成
                make_graph(x_y_list,"Time [s]", "Mag [V]" ,xlim_spec, ylim_spec_ph, title)

        elif "out" in file_name:
            # 加速ピークホールドを処理
            if "acc" in file_name:
                if "bf" in file_name:
                    title = "排気口 試験前 加速ピークホールド"
                elif "af" in file_name:
                    title = "排気口 試験後 加速ピークホールド"
                else:
                    title = "排気口 %d回目 加速ピークホールド" %i+1

                # 横軸，縦軸の数値のみ取り出す
                x_y_list = data_trim(file_name)
                # グラフ作成
                make_graph(x_y_list,"Frequency [Hz]", "Mag [dBV]" ,xlim_spec, ylim_spec_ph, title)

            # 定格スペクトルを処理
            elif "nor" in file_name:
                if "bf" in file_name:
                    title = "排気口 試験前 定格スペクトル"
                elif "af" in file_name:
                    title = "排気口 試験後 定格スペクトル"
                else:
                    title = "排気口 %d回目 定格スペクトル" %i+1

                # 横軸，縦軸の数値のみ取り出す
                x_y_list = data_trim(file_name)

                # グラフ作成
                make_graph(x_y_list,"Frequency [Hz]", "Mag [dBV]" ,xlim_spec, ylim_spec_ph, title)

            # 減速ピークホールドを処理
            elif "nor" in file_name:
                if "bf" in file_name:
                    title = "排気口 試験前 減速ピークホールド"
                elif "af" in file_name:
                    title = "排気口 試験後 減速ピークホールド"
                else:
                    title = "排気口 %d回目 減速ピークホールド" %i+1

                # 横軸，縦軸の数値のみ取り出す
                x_y_list = data_trim(file_name)

                # グラフ作成
                make_graph(x_y_list,"Frequency [Hz]", "Mag [dBV]" ,xlim_spec, ylim_spec_ph, title)

            # 時間波形を処理
            elif "air" in file_name:
                if "bf" in file_name:
                    title = "排気口 試験前 大気突入 時間波形"
                elif "af" in file_name:
                    title = "排気口 試験後 大気突入 時間波形"
                else:
                    title = "排気口 %d回目 大気突入 時間波形" %i+1

                # 横軸，縦軸の数値のみ取り出す
                x_y_list = data_trim(file_name)

                # グラフ作成
                make_graph(x_y_list,"Time [s]", "Mag [V]" ,xlim_spec, ylim_spec_ph, title)


