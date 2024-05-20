if __name__ == "__main__":
    star_file = "tomograms.star"
    tsname_file = "tsname.txt"
    tsdefocus_file = "tsdefocus.txt"
    prefix = "/storage_data/Huwanlong/20240501_tomo/RR-LB-36-10/"
    suffix = "_rec.mrc"
    pixelsize = 6.720000
    subtomonum = 2

    with open(tsname_file, 'r') as file:
        tsname = file.readlines()
    format_tsname = [line.strip() for line in tsname]

    with open(tsdefocus_file, 'r') as file:
        tsdefocus = file.readlines()
    format_tsdefocus = []
    for num in tsdefocus:
        try:
            format_tsdefocus.append(round(float(num), 6))
        except ValueError:
            print(f"无法转换为浮点数: {num}")

    if not len(format_tsname) == len(format_tsdefocus):
        print("Sizes of 2 input files are not equal, do nothing!")
    else:
        with open(star_file, 'w') as file:
            for i in range(0, len(format_tsname), 1):
                file.write(
                    f"{i + 1}\t{prefix}{format_tsname[i]}/{format_tsname[i]}{suffix}\t{pixelsize}\t{format_tsdefocus[i]}\t{subtomonum}\t1\t1\tNone\tNone\t50\t50\tNone\tNone\n")
        print("done")
