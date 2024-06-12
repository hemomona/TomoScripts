import sys
import os


def write_mrc_paths(directory, output_file):
    # 获取指定目录下所有以 .mrc 结尾的文件的绝对路径
    mrc_files = [os.path.abspath(os.path.join(directory, f)) for f in os.listdir(directory) if f.endswith('.mrc')]

    # 将这些路径写入指定的输出文件
    with open(output_file, 'w') as file:
        for path in mrc_files:
            file.write(path + '\n')


if __name__ == "__main__":
    direc = sys.argv[1]
    vll = sys.argv[2]

    write_mrc_paths(direc, vll)
    print("done")
