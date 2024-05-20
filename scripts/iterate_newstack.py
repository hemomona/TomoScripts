import sys
import subprocess


def generate_stack_file(filename, prefix, suffix):
    with open(filename, "w") as file:
        file.write("41\n")
        for i in range(-60, 61, 3):
            if i == 0:
                file.write(f"{prefix}-{i}{suffix}\n0\n")
                continue
            file.write(f"{prefix}{i}{suffix}\n0\n")


def iterate_newstack(start, end, prefix, suffix):
    commands = []
    for i in range(start, end + 1, 1):
        stack_name = f"stack{i}.txt"
        generate_stack_file(stack_name, prefix, suffix)

        commands.append(f"mkdir {prefix}{i:04d}")
        commands.append(f"newstack -filei stack{i}.txt -ou {prefix}{i:04d}/{prefix}{i:04d}.mrc")
        commands.append(f"chmod 777 {prefix}{i:04d}")

    for cmd in commands:
        print("Executing command:", cmd)
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print("Error executing command:", cmd)
            print("Error message:", e)


if __name__ == "__main__":
    input_start = int(sys.argv[1])
    input_end = int(sys.argv[2])
    input_prefix = sys.argv[3]
    mrc_suffix = "_0.mrc"

    iterate_newstack(input_start, input_end, input_prefix, mrc_suffix)
