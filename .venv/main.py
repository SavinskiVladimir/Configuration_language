import yaml
import sys
import re

def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        # загрузка данных из yaml файла, содержащего код конфигурационного языка
        return yaml.safe_load(file)

def convert_to_custom_language(data):
    output = []
    for key, value in data.items():
        if isinstance(value, list):
            output.append(f"{key}: [{'; '.join(map(str, value))}]")
        elif isinstance(value, dict):
            output.append(f"{key}: {{ {convert_to_custom_language(value)} }}")
        else:
            output.append(f"{key}: {value}")
    return "\n".join(output)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_yaml_file>")
        return

    file_path = sys.argv[1]

    try:
        data = parse_yaml(file_path)
        output = convert_to_custom_language(data)
        print(output)
    except yaml.YAMLError as e:
        print(f"YAML Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()