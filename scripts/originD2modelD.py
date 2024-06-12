#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
# File       : originD2modelD.py
# Time       ：2024/6/3 14:19
# Author     ：Jago
# Email      ：huwl2022@shanghaitech.edu.cn
# version    ：python 3.10.11
# Description：
"""
import pandas as pd
import numpy as np


def rotation_matrix(rot, tilt, psi):
    # 将角度转换为弧度
    rot = np.radians(rot)
    tilt = np.radians(tilt)
    psi = np.radians(psi)

    # 绕Z轴旋转的旋转矩阵
    R_z1 = np.array([[np.cos(rot), -np.sin(rot), 0],
                     [np.sin(rot), np.cos(rot), 0],
                     [0, 0, 1]])

    # 绕新的Y轴旋转的旋转矩阵
    R_y = np.array([[np.cos(tilt), 0, np.sin(tilt)],
                    [0, 1, 0],
                    [-np.sin(tilt), 0, np.cos(tilt)]])

    # 绕新的Z轴旋转的旋转矩阵
    R_z2 = np.array([[np.cos(psi), -np.sin(psi), 0],
                     [np.sin(psi), np.cos(psi), 0],
                     [0, 0, 1]])

    # 最终旋转矩阵是这三个旋转矩阵的乘积
    return R_z2 @ R_y @ R_z1


def calculate_model_length(point_out, point_in, shift, euler):
    # # 获取旋转矩阵
    # R = rotation_matrix(euler[0], euler[1], euler[2])
    #
    # point_out = np.append(point_out, 1)
    # point_in = np.append(point_in, 1)

    # # 以下为方法1：计算逆矩阵，用于将图像坐标转换回模型坐标
    # R_inv = np.linalg.inv(R)
    #
    # # 将初始坐标逆推回observation坐标
    # point_out_obs = point_out - shift
    # point_in_obs = point_in - shift
    #
    # # 将observation坐标转换到模型坐标系
    # point_out_model = R_inv @ point_out_obs
    # point_in_model = R_inv @ point_in_obs

    # # 以下为方法2：将旋转矩阵与平移向量水平结合为3×4矩阵
    # R = np.hstack((R, shift.reshape(-1, 1)))
    #
    # # 计算伪逆矩阵，4×3
    # R_pinv = np.linalg.pinv(R)
    #
    # point_out_model = R_pinv @ point_out
    # point_in_model = R_pinv @ point_in

    # 使用深度信息z进行缩放
    # point_out_model = point_out_model * z / point_out_model[2]
    # point_in_model = point_in_model * z / point_in_model[2]

    # 计算初始坐标系中两点的距离
    length_ori = np.linalg.norm(point_out - point_in)
    # # 计算模型坐标系中两点的距离
    # length_model = np.linalg.norm(point_out_model[:3] - point_in_model[:3])

    return length_ori


def calculate_file(input, sheet, output):
    df = pd.read_excel(input, sheet_name=sheet)

    # 提取_rlnOriginXAngst..(bin1，单位A), _rlnAngleRot..(Z, newY, newZ), bin4 coordinates
    cols = ['_rlnOriginXAngst', '_rlnOriginYAngst', '_rlnOriginZAngst', '_rlnAngleRot', '_rlnAngleTilt', '_rlnAnglePsi',
            'bi4_CZ', 'bin4_OutX_virus', 'bin4_OutY_virus', 'bin4_InX_virus', 'bin4_InY_virus',
            'bin4_OutX_ctl', 'bin4_OutY_ctl', 'bin4_InX_ctl', 'bin4_InY_ctl']
    data = df[cols].copy().astype(float)  # 使用 .copy() 明确表示需要一个副本

    # 使用 .loc 进行赋值操作，以明确地选择行和列，避免 SettingWithCopyWarning，从bin4的pixel坐标转为Angstrom坐标
    # data.loc[:, ['bi4_CZ', 'bin4_OutX_virus', 'bin4_OutY_virus', 'bin4_InX_virus', 'bin4_InY_virus',
    #              'bin4_OutX_ctl', 'bin4_OutY_ctl', 'bin4_InX_ctl', 'bin4_InY_ctl']] *= 4 * 1.68

    data[['virus_distance']] = data.apply(
        lambda row: pd.Series(calculate_model_length(
            np.array([row['bin4_OutX_virus'], row['bin4_OutY_virus']]) * 4 * 1.68,
            np.array([row['bin4_InX_virus'], row['bin4_InY_virus']]) * 4 * 1.68,
            np.array([row['_rlnOriginXAngst'], row['_rlnOriginYAngst'], row['_rlnOriginZAngst']]),
            np.array([row['_rlnAngleRot'], row['_rlnAngleTilt'], row['_rlnAnglePsi']])
        )), axis=1
    )

    data[['ctl_distance']] = data.apply(
        lambda row: pd.Series(calculate_model_length(
            np.array([row['bin4_OutX_ctl'], row['bin4_OutY_ctl']]) * 4 * 1.68,
            np.array([row['bin4_InX_ctl'], row['bin4_InY_ctl']]) * 4 * 1.68,
            np.array([row['_rlnOriginXAngst'], row['_rlnOriginYAngst'], row['_rlnOriginZAngst']]),
            np.array([row['_rlnAngleRot'], row['_rlnAngleTilt'], row['_rlnAnglePsi']])
        )), axis=1
    )

    # 将结果保存到新的Excel文件

    data.to_excel(output, index=False)
    print("done")


if __name__ == "__main__":
    file_path = 'D:/CourseStudy/0research_project/cryo_ET/RR-membrane-info.xlsx'
    sheet_name = '0226RR'
    output_file_path = 'RR-membrane-distance.xlsx'
    calculate_file(file_path, sheet_name, output_file_path)

    # testPointOut = np.array([297, 1361]) * 4 * 1.68
    # testPointIn = np.array([336, 1379]) * 4 * 1.68
    # shift = np.array([1.459635, 17.119635, -0.04037])
    # euler = np.array([105.533081, 108.715194, -30.00834])
    # print(calculate_model_length(testPointOut, testPointIn, shift, euler))
