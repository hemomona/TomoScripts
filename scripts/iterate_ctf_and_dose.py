import os
import sys
import subprocess


def read_file(filename, pixelsize):
	with open(filename, 'r') as file:
		blocks = {}
		current_block = None
		total_dose = 0  # 该值为前几张累积dose + 当前dose

		for line in file:
			line = line.strip()
			if not line:
				continue

			if line.startswith('[ZValue') and line.endswith(']'):
				if current_block:  # 如果是第二个到倒数第二个block，再赋给current_block block_name前，它就是"前一个"
					dose_rate = float(blocks[current_block]['DoseRate'])
					exposure_time = float(blocks[current_block]['ExposureTime'])
					curr_dose = dose_rate * exposure_time / pixelsize / pixelsize
					total_dose += curr_dose
					blocks[current_block]['CurrDose'] = curr_dose
					blocks[current_block]['TotalDose'] = total_dose
				# 包括了第一个到倒数第二个block的情况
				block_name = line.split('=')[-1].strip().rstrip(']')
				current_block = block_name
				blocks[current_block] = {}
			elif current_block:
				key, value = line.split('=')
				blocks[current_block][key.strip()] = value.strip()
		# 最后一个block
		dose_rate = float(blocks[current_block]['DoseRate'])
		exposure_time = float(blocks[current_block]['ExposureTime'])
		curr_dose = dose_rate * exposure_time / pixelsize / pixelsize
		total_dose += curr_dose
		blocks[current_block]['CurrDose'] = curr_dose
		blocks[current_block]['TotalDose'] = total_dose
	return blocks


def write_doseperview_file(blocks, dose_file):
	with open(dose_file, 'w') as file:
		sorted_blocks = sorted(blocks.items(), key=lambda x: float(x[1]['TiltAngle']))
		for block_name, block_data in sorted_blocks:
			curr_dose = float(block_data.get('CurrDose', 0))
			prior_dose = float(block_data.get('TotalDose', 0)) - curr_dose
			file.write(f"{prior_dose}\t{curr_dose}\n")


def calculate_average_from_file(filename):
	total = 0
	count = 0

	try:
		with open(filename, 'r') as file:
			for line in file:
				# 忽略以 # 开头的行
				if line.startswith("#"):
					continue

				parts = line.split()
				if len(parts) >= 2:
					try:
						# 提取第二列的数字并累加
						number = float(parts[1])
						total += number
						count += 1
					except ValueError:
						continue
	except FileNotFoundError:
		print(f"Error: The file '{filename}' was not found.")
		return None

	if count == 0:
		return 0

	return total / count


def iterate_ctf_and_dose(start, end, prefix, pixel_size, dose_file, ctf_file, log_file):
	original_dir = os.getcwd()

	for i in range(start, end + 1, 1):
		folder_name = f"{prefix}{i:04}"
		os.chdir(folder_name)

		# compute dose
		blocks = read_file(f"../{folder_name}.mdoc", pixel_size)
		write_doseperview_file(blocks, dose_file)

		print(f"done dose computation and doing ctffind in {folder_name}")

		# run ctffind
		ctf = "ctffind"
		process = subprocess.Popen(ctf, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
								   stderr=subprocess.PIPE, universal_newlines=True)

		process.stdin.write(f'{folder_name}.mrc\n')  # 文件名
		process.stdin.flush()
		process.stdin.write('no\n')  # not movie
		process.stdin.flush()
		process.stdin.write('diagnostic_output.mrc\n')  # diagnostic_output.mrc
		process.stdin.flush()
		process.stdin.write('1.68\n')  # pixel size
		process.stdin.flush()
		process.stdin.write('300\n')  # 300kV
		process.stdin.flush()
		process.stdin.write('2.7\n')  # 2.7
		process.stdin.flush()
		process.stdin.write('0.07\n')  # 0.07
		process.stdin.flush()
		process.stdin.write('512\n')  # 512
		process.stdin.flush()
		process.stdin.write('50\n')  # 50 minres
		process.stdin.flush()
		process.stdin.write('5\n')  # 5 maxres
		process.stdin.flush()
		process.stdin.write('5000\n')  # 5000 mindefocus
		process.stdin.flush()
		process.stdin.write('60000\n')  # 60000 maxdefocus
		process.stdin.flush()
		process.stdin.write('100\n')  # 100
		process.stdin.flush()
		process.stdin.write('no\n')  # no
		process.stdin.flush()
		process.stdin.write('no\n')  # no
		process.stdin.flush()
		process.stdin.write('no\n')  # no
		process.stdin.flush()
		process.stdin.write('no\n')  # no
		process.stdin.flush()
		process.stdin.write('no\n')  # no
		process.stdin.flush()

		output, error = process.communicate()
		print(output)
		print(error)

		os.chdir(original_dir)

		with open(ctffile, 'a+') as f:
			average_defocus = calculate_average_from_file(f"{folder_name}/diagnostic_output.txt")
			f.write(f"{folder_name}\t{average_defocus}\n")
		with open(log_file, "a+") as fp:
			fp.write(error + '\n')


if __name__ == "__main__":
	input_start = int(sys.argv[1])
	input_end = int(sys.argv[2])
	input_prefix = sys.argv[3]
	input_pixelsize = float(sys.argv[4])
	dosefile = "prior_and_curr_dose.txt"
	ctffile = "average_defocus.txt"
	log = "ctf_dose_log.txt"

	iterate_ctf_and_dose(input_start, input_end, input_prefix, input_pixelsize, dosefile, ctffile, log)
