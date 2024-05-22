"""
大気突入試験レポートに使用するグラフを作成するプログラム
もうちょっと汎用性を高めたいなあ
GA87-1529-36で使用

"""

import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
import pandas as pd
import os
from tqdm import tqdm

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
folder_path = '04_FFTdata'


# fftのテキストデータからX軸，y軸の値のみ取り出すサブルーチン
def data_trim(fft_folderpath, file_list):
    for file_name in file_list:
        if "001" in file_name:
            df_x1 = pd.read_csv('%s/%s' %(fft_folderpath, file_name),header=None, skiprows=16, encoding='shift-jis')
        elif "002" in file_name:
            df_x2 = pd.read_csv('%s/%s' %(fft_folderpath, file_name),header=None, skiprows=16, encoding='shift-jis')
        elif "003" in file_name:
            df_y2 = pd.read_csv('%s/%s' %(fft_folderpath, file_name),header=None, skiprows=16, encoding='shift-jis')
        elif "004" in file_name:
            df_z = pd.read_csv('%s/%s' %(fft_folderpath, file_name),header=None, skiprows=16, encoding='shift-jis')


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
    fig.tight_layout()

    plt.savefig("05_レポート/01_fig/" + title + ".pdf")
    # closeとclfでグラフを閉じてメモリ開放．closeだけではメモリが完全に開放できないらしいからclfもしている．
    plt.close()
    plt.clf()


"""以下からメイン関数"""

# folder_pathの中身のパスをリストとして取得
# 後の分類を楽にするために，dir_pathリストのすべての要素（文字列）を小文字に変換している
# for s in リストはリストの要素を1個ずつ見ていく感じです
data_path = [s.lower() for s in os.listdir(folder_path) ]

for i in tqdm(range(num_times)):
    title_dict = {"in" : "吸気口", "out" : "排気口", "bf" : "試験前", "af" : "試験後", "n%s" %str(i+1).zfill(2) : "%s回目" %str(i+1).zfill(2), "acc" : "加速ピークホールド",
                "nor" : "定格スペクトル", "air" : "大気突入時間波形", "brk" : "減速ピークホールド"}

    # dir_pathからtxtファイル名をリストで取得し，その中からn回目のデータを取り出す
    times_file_path = [s for s in data_path if 'n%s' %str(i+1).zfill(2) in s or "bf" in s or "af" in s]


    for direction in ["in", "out"]:
        for when in ["bf", "n%s" %str(i+1).zfill(2), "af"]:
            for mode in ["acc", "nor" , "brk", "air"]:
                    if ((when == "bf" and mode == "air") or (when == "af" and mode == "air") or (when == "n%s" %str(i+1).zfill(2) and mode == "brk")):
                        continue
                    title = title_dict[direction] + "_" + title_dict[when] + "_" + title_dict[mode]
                    file_list = [s for s in times_file_path if direction in s and when in s and mode in s]
                    if mode == "air":
                        xlabel = "Time [s]"
                        ylabel = "Mag [V]"
                        xlim = xlim_time
                        ylim = ylim_time
                    elif mode == "nor":
                        xlabel = "Frequency [Hz]"
                        ylabel = "Mag [dBV]"
                        xlim = xlim_spec
                        ylim = ylim_spec_avg
                    else:
                        xlabel = "Frequency [Hz]"
                        ylabel = "Mag [dBV]"
                        xlim = xlim_spec
                        ylim = ylim_spec_ph
                    # 横軸，縦軸の数値のみ取り出す
                    x_y_list = data_trim(folder_path,file_list)
                    # グラフ作成
                    make_graph(x_y_list,xlabel, ylabel ,xlim, ylim, title)





