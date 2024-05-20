import argparse

from scripts.iterate_ctf_and_dose import iterate_ctf_and_dose
from scripts.iterate_newstack import iterate_newstack
from scripts.rename_mdoc import rename_mdoc
from scripts.rename_mrc import rename_mrc
from scripts.write_stars_forrelion import generate_tomo_and_coord_star_file


def main():
    parser = argparse.ArgumentParser(description='There are scripts I used in tomo data process in linux.\n'
                                                 'Whenever having problems, type -h or --help.\n\n'
                                                 'Make sure your acquired data is right, or you may need to understand '
                                                 'the rename_fromtxt.py and addnum_formrc.py fully before using them.\n'
                                                 'Example Usages:\n'
                                                 
                                                 'python3 main.py --function rename_mrc '
                                                 '--number_place 2 --degree_place 3 --suffix .mrc '
                                                 '(--file_directory ./ --log mrc_rename_log.txt)\n'
                                                 
                                                 'python3 main.py --function rename_mdoc '
                                                 '--prefix 20240501_RR-PBS-15-10_ --suffix .mdoc '
                                                 '(--file_directory ./ --log mdoc_rename_log.txt)\n'
                                                 
                                                 'python3 main.py --function newstack --start 1 --end 32 '
                                                 '--prefix  20240501_RR-PBS-15-10_ --suffix _0.mrc\n'
                                                 
                                                 'python3 main.py --function ctf_and_dose --start 1 --end 32 '
                                                 '--prefix 20240501_RR-PBS-15-10_ --pixel_size 1.68 '
                                                 '(--dose_file dose_per_view.txt --ctf_file average_defocus.txt '
                                                 '--log ctf_dose_log.txt)\n'
                                                 
                                                 'python3 main.py --function deepetpicker2relion --file_directory '
                                                 '/storage_data/Huwanlong/20240501_tomo/deepetpicker/RR-PBS-15-10/ '
                                                 '--prefix /storage_data/Huwanlong/20240501_tomo/RR-PBS-15-10/ '
                                                 '--suffix _rec.coords --particle_ID 1 --bin_factor 4 (--tomo_star '
                                                 'tomogram_descri.star --coord_star particle_coords.star --order_list '
                                                 'my_order_list.csv)\n',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--function', type=str, help='the invoked function.')
    parser.add_argument('--file_directory', type=str, help='the file directory.')
    parser.add_argument('--number_place', type=str, help='the tiff acquiring number,'
                                                         'the place number started from 0')
    parser.add_argument('--degree_place', type=str, help='the tiff acquiring degree,'
                                                         'the place number started from 0')
    parser.add_argument('--log', type=str, help='log file name')
    parser.add_argument('--prefix', type=str, help='file name prefix')
    parser.add_argument('--suffix', type=str, help='file name suffix')

    parser.add_argument('--start', type=int, help='start number of process')
    parser.add_argument('--end', type=int, help='end number (also to be processed) of process')

    parser.add_argument('--dose_file', type=str, help='log file name', default='dose_per_view.txt')
    parser.add_argument('--ctf_file', type=str, help='log file name', default='average_defocus.txt')
    parser.add_argument('--pixel_size', type=float, help='in Angstrom')

    parser.add_argument('--particle_ID', type=int, help='particle ID in deepetpicker coordinate')
    parser.add_argument('--bin_factor', type=int, help='bin factor to times coordinates in deepetpicker')
    parser.add_argument('--tomo_star', type=str, help='tomograms description star file', default='tomogram_descri.star')
    parser.add_argument('--coord_star', type=str, help='particles coordinate star file', default='particle_coords.star')
    parser.add_argument('--order_list', type=str, help='degree list when acquiring tiff', default='my_order_list.csv')

    args = parser.parse_args()

    if args.function == 'rename_mrc':
        file_directory = args.file_directory if args.file_directory is not None else "./"
        log = args.log if args.log is not None else "mrc_rename_log.txt"
        print(f'Renaming {args.suffix} in {file_directory}')
        rename_mrc(file_directory, args.number_place, args.degree_place, args.suffix, log)
        print("done.")

    elif args.function == 'rename_mdoc':
        file_directory = args.file_directory if args.file_directory is not None else "./"
        log = args.log if args.log is not None else "mdoc_rename_log.txt"
        print(f"Renaming {args.suffix} in {file_directory}")
        rename_mdoc(file_directory, args.prefix, args.suffix, log)
        print("done.")

    elif args.function == 'newstack':
        iterate_newstack(args.start, args.end, args.prefix, args.suffix)
        print("done.")

    elif args.function == 'ctf_and_dose':
        log = args.log if args.log is not None else "ctf_dose_log.txt"
        iterate_ctf_and_dose(args.start, args.end, args.prefix, args.pixel_size, args.dose_file, args.ctf_file, log)
        print("done.")

    elif args.function == 'deepetpicker2relion':
        file_directory = args.file_directory if args.file_directory is not None else "./"
        generate_tomo_and_coord_star_file(file_directory, args.prefix, args.suffix, args.particle_ID, args.bin_factor, args.tomo_star, args.coord_star, args.order_list)
        print("done.")

    else:
        print(f"Unknown function: {args.function}")


if __name__ == "__main__":
    main()
