import os
import itertools
import sys


def rename_mrc(filedir, number, degree, suffix, logfile):
    # get all suffix file in filedir
    files = []
    for file in os.listdir(filedir):
        if file.endswith(suffix):
            files.append(file)

    sorted_data = sorted(files, key=lambda x: (
        float(x[0:x.rfind(suffix)].split('_')[degree]), float(x[0:x.rfind(suffix)].split('_')[number])))

    grouped_data = [list(group) for key, group in
                    itertools.groupby(sorted_data, key=lambda x: float(x[0:x.rfind(suffix)].split('_')[degree]))]

    for group in grouped_data:
        gr = sorted(files, key=lambda x: (
            float(x[0:x.rfind(suffix)].split('_')[degree]), float(x[0:x.rfind(suffix)].split('_')[degree])))
        for i in range(0, len(group)):
            old_file_name = group[i]
            new_file_name = old_file_name.replace(
                '_' + old_file_name[0:old_file_name.rfind(suffix)].split('_')[number] + '_',
                '_' + "{:04d}".format(int(i + 1)) + '_')
            print(f"mv {old_file_name} to {new_file_name}")
            os.system("mv '%s' '%s'" % (os.path.join(filedir, old_file_name), os.path.join(filedir, new_file_name)))
            with open(logfile, "a+") as fp:
                fp.write(old_file_name + '\t' + new_file_name + '\n')


if __name__ == "__main__":
    input_filedir = sys.argv[1]
    input_number = sys.argv[2]
    input_degree = sys.argv[3]
    mrc_suffix = ".mrc"
    log = "./mrc_rename_log.txt"

    print(f"Renaming {mrc_suffix} in {input_filedir}")
    rename_mrc(input_filedir, input_number, input_degree, mrc_suffix, log)
    print("done.")
