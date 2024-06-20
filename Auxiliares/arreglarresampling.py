def truncate(number, decimals=3):
    multiplier = 10 ** decimals
    truncated_number = int(number * multiplier) / multiplier
    return int(truncated_number) if truncated_number == 0.0 else truncated_number

input_file_path = "/home/carla/Documentos/Tesis/Py/Datasets/Nuevo/6horas_50hz.txt"

output_lines = []

with open(input_file_path, "r") as input_file:
    for line in input_file:
        values = line.strip().split(";")
        first_value = values[0]
        truncated_values = [str(truncate(float(val))) if i > 0 else val for i, val in enumerate(values)]
        output_line = ";".join(truncated_values)
        output_lines.append(output_line)

with open(input_file_path, "w") as output_file:
    output_file.write("\n".join(output_lines))
