import re
import os
import shutil
import argparse

def convert_fandom_to_markdown(text):
    text = re.sub(r'^=+\s*(.*?)\s*=+', r'# \1', text, flags=re.MULTILINE)
    text = re.sub(r"'''(.*?)'''", r'**\1**', text)
    text = re.sub(r"''(.*?)''", r'*\1*', text)
    text = re.sub(r'\n\*\s*(.*?)\n', r'\n* \1\n', text)
    text = re.sub(r'\n#\s*(.*?)\n', r'\n1. \1\n', text)
    text = re.sub(r'\[\[(.*?)\]\]', r'[\1](\1)', text)
    text = re.sub(r'\[\[File:(.*?)\]\]', r'![Image](\1)', text)
    text = re.sub(r'----', r'---', text)
    text = re.sub(r'\{\|(.*?)\|\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\|\|(.*?)\|\|', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'\|-(.*?)\|-', '', text, flags=re.DOTALL)
    text = re.sub(r'\|\+(.*?)\+\|', r'\1', text, flags=re.DOTALL)
    text = re.sub(r'\|\|(.*?)\|\|', r'\1', text, flags=re.DOTALL)

    return text

def convert_file(source_file, destination_dir):
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            fandom_text = f.read()

        markdown_text = convert_fandom_to_markdown(fandom_text)

        rel_path = os.path.relpath(source_file, os.path.join(os.getcwd(), "out"))
        dest_file = os.path.join(destination_dir, rel_path)

        os.makedirs(os.path.dirname(dest_file), exist_ok=True)

        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(markdown_text)

        print(f"Conversion complete. '{source_file}' has been formatted and copied to '{dest_file}'.")

    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found.")

def convert_files_in_directory(source_dir, destination_dir):
    for root, _, files in os.walk(source_dir):
        for file_name in files:
            if file_name.endswith(".txt"):
                file_path = os.path.join(root, file_name)
                convert_file(file_path, destination_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Fandom format files to Markdown.')
    parser.add_argument('source', metavar='source_directory', type=str,
                        help='the source directory containing Fandom format files')
    parser.add_argument('--copy', action='store_true', help='copy formatted files to "out-formatted" directory')

    args = parser.parse_args()

    source_directory = args.source
    copy_files = args.copy

    destination_directory = os.path.join(os.getcwd(), "out-formatted")

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    convert_files_in_directory(source_directory, destination_directory)
