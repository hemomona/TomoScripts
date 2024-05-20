import os
import sys
import re


def extract_number(filename):
    pattern = r'(\d+)_ts_(\d+)'
    match = re.search(pattern, filename)

    if match:
        # must convert to int
        return int(match.group(1)), int(match.group(2))
    else:
        # ensure the file not matched to be sorted at first
        return -1, -1


def rename_mdoc(filedir, prefix, suffix, logfile):
    # get all suffix file in filedir
    files = []
    for file in os.listdir(filedir):
        if file.endswith(suffix):
            files.append(file)

    files.sort(key=extract_number)

    for i, file in enumerate(files, 1):
        new_name = f"{prefix}{i:04}.mdoc"
        os.rename(file, new_name)
        print(f"将文件 {file} 重命名为 {new_name}")
        with open(logfile, "a+") as fp:
            fp.write(file + '\t' + new_name + '\n')


if __name__ == "__main__":
    input_filedir = sys.argv[1]
    input_prefix = sys.argv[2]
    mdoc_suffix = ".mdoc"
    log = "./mdoc_rename_log.txt"

    print(f"Renaming {mdoc_suffix} in {input_filedir}")
    rename_mdoc(input_filedir, input_prefix, mdoc_suffix, log)
    print("done.")
