import sys
import subprocess

if __name__ == "__main__":
	start = int(sys.argv[1])
	end = int(sys.argv[2])
	add = int(sys.argv[3])
	prefix = sys.argv[4]

	# 要执行的命令列表
	commands = []
	for i in range(start, end+1, 1):
		cmd1 = "for file in {}{:04d}*.mrc; do mv \"$file\" \"$(echo $file | sed \'s/{:04d}/{:04d}/\')\"; done".format(prefix, i, i, i+add)
		commands.append(cmd1)

	# 迭代执行命令
	for cmd in commands:
		print("Executing command:", cmd)
		# 使用subprocess模块执行命令
		try:
			subprocess.run(cmd, shell=True, check=True)
		except subprocess.CalledProcessError as e:
			print("Error executing command:", cmd)
			print("Error message:", e)

