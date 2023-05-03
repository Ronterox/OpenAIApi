from tokenizer import count_tokens
import os

DIR_PATH = "/home/rontero/Downloads/Touhou: Flandre Scarlet is in my house"
FILE_EXT = ".txt"

def lines_to_str(lines): return '\n'.join(lines)

def get_tokens(prompt: list[str]): return count_tokens("text-davinci-003", lines_to_str(prompt))

def get_path_name(filepath): return filepath.split("/")[-1]

def create_prompt_files(filepath):
    with open(filepath, "r") as f:
        lines = f.read().split("\n")
        total_lines = len(lines)
        divisions = 1

        tokens = get_tokens(lines)
        while tokens > 4096:
            divisions += 1
            tokens = get_tokens(lines[:total_lines // divisions])

        folderpath = f"data/{get_path_name(DIR_PATH)}"
        filename = get_path_name(filepath).replace(FILE_EXT, "")
        prompt_filepath = f"{folderpath}/{filename}"

        lines_per_file = total_lines // divisions
        print(f"Files: {divisions}\nLines per file: {lines_per_file}")

        for i in range(divisions):
            text = lines_to_str(lines[i * lines_per_file:(i + 1) * lines_per_file])
            os.makedirs(prompt_filepath, exist_ok=True)
            open(f"{prompt_filepath}/{i}.{filename}{FILE_EXT}", "w").write(text)

if __name__ == "__main__":
    for file in os.listdir(DIR_PATH):
        if file.endswith(FILE_EXT):
            create_prompt_files(f"{DIR_PATH}/{file}")