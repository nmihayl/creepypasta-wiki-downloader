# Creepypasta Wiki Downloader

This set of Python scripts allows for scraping the Creepypasta Fandom Wiki to download the individual stories and save them as plaintext files.

## How does this work?

You need the `wikiteam3` Python library in order to scrape the available page titles in the wiki. The resulting `...-titles.txt` file will then be used as a reference for a different scraper script to extract the page contents directly from the Fandom edit view and save them as individual text files. A supplementary script moves all the files into alphabetical folders and that should do it for the scraping process.

## How can I use this data?

You can just fire up your text editor of choice, pick a text file of your choosing and start reading! Keep in mind that the text formatting uses the Fandom syntax (there is an additional script which translates the source syntax to Markdown for later processing).

My use case of scraping the data is to make my own Markdown and PDF files which I can later convert to an eBook compilation of the PDFs using Pandoc.

## Can I just grab the data from somewhere?

Yes, the downloaded and organized text files are available on the Internet Archive, courtesy of me:

[Internet Archive](https://archive.org/details/creepypasta-fandom-wiki.tar)

Do keep in mind the data is a snapshot from July 2nd 2024, and newer pages may not be in this archive.

## Okay, what do I need?

You will need:

- Python 3.8

- The `wikiteam3` Python package

- Pandoc (optional, only if you want to make PDFs and eBooks)

git clone this repository and cd into it:

`git clone https://github.com/nmihayl/creepypasta-wiki-downloader`

`cd creepypasta-wiki-downloader`

Install the `wikiteam3` package using pip:

`pip install wikiteam3`

Execute the first script to source the titles:

`python 01-title-scraper.py`

Let the process finish. You should end up with a `...titles.txt` file in the directory.

Now execute the second script to scrape the text contents from the titles:

`python 02-text-scraper.py`

This script will also move all the created files containing a redirect link on the wiki to a separate "redirect" folder.

The last script `03-fandom-md.py` converts the Fandom wiki syntax to Markdown and change the file extensions to `.md`. It is recommended to use the `--copy` flag to save the modified files to a separate directory instead of overwriting them, but the choice is yours. Here is the command:

`python 03-fandom-md.py --copy out`

That should do it for the scraper, you can now manually review the files you want to convert to other document formats using Pandoc!
