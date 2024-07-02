import os
import shutil
import time
from datetime import datetime
import subprocess
import threading


def check_for_end_marker(directory, stop_event):
    while not stop_event.is_set():
        time.sleep(10)
        for filename in os.listdir(directory):
            if filename.endswith('titles.txt'):
                with open(os.path.join(directory, filename), 'r') as file:
                    content = file.read()
                    if '--END--' in content:
                        stop_event.set()
                        print("--END-- marker found. Stopping dump generator.")
                        return


def monitor_output(process, stop_event):
    for line in process.stdout:
        print(line.decode(), end='')
        if "Titles saved at" in line.decode():
            stop_event.set()
            print("Stopping dump generator due to 'Titles saved at' message.")
            process.terminate()
            return


def rename_titles_file(directory):
    for filename in os.listdir(directory):
        if filename.endswith('titles.txt'):
            src = os.path.join(directory, filename)
            dst = os.path.join(directory, 'titles.txt')
            os.rename(src, dst)
            print(f"Renamed {filename} to titles.txt")
            return dst


def main():
    wiki_title = "https://creepypasta.fandom.com"
    namespaces = [0]

    date_str = datetime.now().strftime("%Y%m%d")
    folder_name = f"creepypasta.fandom.com-{date_str}-wikidump"

    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
        print(f"Deleted existing directory: {folder_name}")

    args = [
        "wikiteam3dumpgenerator",
        wiki_title,
        "--xml",
        f"--namespaces={','.join(map(str, namespaces))}"
    ]

    stop_event = threading.Event()
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    monitor_thread = threading.Thread(target=monitor_output, args=(process, stop_event))
    monitor_thread.start()
    check_thread = threading.Thread(target=check_for_end_marker, args=(folder_name, stop_event))
    check_thread.start()
    stop_event.wait()

    if process.poll() is None:
        process.terminate()

    renamed_file_path = rename_titles_file(folder_name)

    if renamed_file_path:
        parent_directory = os.path.dirname(os.path.abspath(__file__))
        new_path = os.path.join(parent_directory, 'titles.txt')
        shutil.move(renamed_file_path, new_path)
        print(f"Moved titles.txt to {parent_directory}")

    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)

    print("Dump generation completed or stopped due to conditions met.")

    monitor_thread.join()
    check_thread.join()


if __name__ == "__main__":
    main()
