import os
import sys

if __name__ == "__main__":
	txt = sys.argv[1]

	with open(txt, 'r') as file:
		lines = file.readlines()
		for line in lines:
			parts = line.strip().split('\t')
			old_file_name = parts[1]
			new_file_name = parts[0]
			if not os.path.exists(old_file_name):
				print(f"File {old_file_name} does not exist, skipping.")
				continue

			if os.path.exists(new_file_name):
				print(f"File {new_file_name} already exists, skipping.")
			else:
				os.rename(old_file_name, new_file_name)
				print(f"Renamed {old_file_name} to {new_file_name}")
