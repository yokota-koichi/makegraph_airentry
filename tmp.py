import os
import glob

# ファイルが保存されているディレクトリを指定します
directory_path = "test"

for i in range(10):
    # すべての.txtファイルを取得します
    for file_name in glob.glob(os.path.join(directory_path, '???_???_n%d_???.txt' %(i+1))):
        # 元のファイル名から新しいファイル名を作成します
        new_file_name = file_name.replace('_n%d_' %(i+1), '_n%s_' %str(i+1).zfill(2))
        # ファイル名を変更します
        os.rename(file_name, new_file_name)