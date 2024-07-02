import os
import requests
from bs4 import BeautifulSoup
import re
import shutil

def sanitize_filename(title):
    sanitized_title = re.sub(r'[\\/:*?"<>|]', '_', title)
    return sanitized_title.strip()

def fetch_edit_page_content(base_url, page_title):
    edit_url = f"{base_url}/wiki/{page_title}?action=edit"
    response = requests.get(edit_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        textarea = soup.find('textarea', id='wpTextbox1')

        if textarea:
            return textarea.text
        else:
            redirect_match = re.match(r'#REDIRECT \[\[([^\]]+)\]\]', response.text)
            if redirect_match:
                redirect_title = redirect_match.group(1)
                print(f"Redirect found: {page_title} -> {redirect_title}")
                return fetch_edit_page_content(base_url, redirect_title)
            else:
                print(f"Textarea not found for page '{page_title}'")
                return None
    else:
        print(f"Failed to fetch edit page for '{page_title}', Status code: {response.status_code}")
        return None

def save_to_file(content, directory, filename, page_title):
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"{page_title}\n\n")
        f.write(content)
    print(f"Content saved to '{filepath}'")

    lines = content.splitlines()
    lines_lower = [line.lower() for line in lines]

    if len(lines) < 10 and any("#redirect[[" in line or "#redirect [[" in line for line in lines_lower):
        target_dir = os.path.join(directory, "redirects")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        redirect_filepath = os.path.join(target_dir, filename)
        shutil.move(filepath, redirect_filepath)
        print(f"File '{filename}' contains a redirect and has been moved to '{target_dir}'.")

def main():
    base_url = "https://creepypasta.fandom.com"
    output_directory = "./out"

    try:
        titles_file = [file for file in os.listdir() if file.lower().endswith('titles.txt')]
        if not titles_file:
            raise FileNotFoundError

        with open(titles_file[0], 'r', encoding='utf-8') as file:
            page_titles = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: No file ending with 'titles.txt' found in the current directory.")
        return

    try:
        for page_title in page_titles:
            print(f"Processing page: {page_title}")

            edit_content = fetch_edit_page_content(base_url, page_title)

            if edit_content:
                sanitized_title = sanitize_filename(page_title)
                filename = f"{sanitized_title}.txt"

                first_letter = filename[0].upper()
                letter_directory = os.path.join(output_directory, first_letter)
                save_to_file(edit_content, letter_directory, filename, page_title)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
