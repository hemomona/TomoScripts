#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
# File       : write_stars_forrelion.py
# Time       ：2024/5/20 22:51
# Author     ：Jago
# Email      ：huwl2022@shanghaitech.edu.cn
# version    ：python 3.10.11
# Description：
"""
import os


def generate_tomo_and_coord_star_file(filedir, prefix, suffix, particle_ID, bin_factor, tomo_star, coord_star, order_list):
    files = []
    for file in os.listdir(filedir):
        if file.endswith(suffix):
            files.append(file)

    with open(tomo_star, 'w') as f:
        f.write("\ndata_\nloop_\n_rlnTomoName\n_rlnTomoTiltSeriesName\n_rlnTomoImportCtfFindFile"
                "\n_rlnTomoImportImodDir\n_rlnTomoImportOrderList\n")
        for ts in files:
            ts_name = ts.split(suffix)[0]
            f.write(f"{ts_name}\t{prefix}{ts_name}/{ts_name}.mrc\t{prefix}{ts_name}/diagnostic_output.txt\t{prefix}{ts_name}\t{order_list}\n")
    print(f"written {tomo_star}")

    formatted_particles = []
    for file in files:
        with open(f"{filedir}/{file}", 'r') as f:
            particles = f.readlines()

        for line in particles:
            parts = line.strip().split('\t')
            if len(parts) < 4:
                print(f"Skipping malformed line in {file}: {line}")
                continue

            try:
                # python can not convert from str to int directly!!!
                if int(float(parts[0])) == particle_ID:
                    parts[0] = file.split(suffix)[0]
                    parts[1:4] = [str(float(x) * bin_factor) for x in parts[1:4]]
                    formatted_particles.append('\t'.join(parts))
            except ValueError:
                print(f"value error in {file}: {line}")
                continue

    with open(coord_star, "w") as f:
        f.write("data_particles\nloop_\n_rlnTomoParticleId #1\n_rlnTomoName #2\n_rlnCoordinateX #3\n_rlnCoordinateY "
                "#4\n_rlnCoordinateZ #5\n")
        for i in range(len(formatted_particles)):
            f.write(f"{i+1}\t{formatted_particles[i]}\n")
    print(f"written {coord_star}")


