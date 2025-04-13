# Wordsearch

Which of course, generates word searches (rather then searching for words).

# Why?

I needed a way to quickly generate a word search for any given list of words with varying levels of difficulty.

## Aren't there free online tools?

Probably (almost definitely); however, in observing some of the students I was teaching use a published word-search book, they would find words that weren't in the search list. While these "bonus" words were fine (and they thought themselves smart for having found them), I wanted a tool that could guarantee me no "bonus" words (and, especially not any that happened to be foul language or not age-appropriate).

## How does `wordsearch` help with this?

After generating a mapping, if `offensive_words.txt` is present or, `all_english_words.txt` is present in the `wordsearch` folder (next to `_english_words.py`), the program loads in all words found in either of these files and makes sure that none of them are present (in any orientation) in the filler text (if it finds one, it will randomly select a different filler letter).

> I don't see either of those word files in the repo??

`all_english_words.txt` can be downloaded (and renamed) from [dwyl/english-words](https://github.com/dwyl/english-words/blob/master/words.txt) (I am choosing to not redistribute this 4.64MB file both for the sake of the size of this repo, but also to maintain attribution to user dwyl and other maintainers who have been maintaining this list)


`offensive_words.txt` -> It felt *really* weird to make a text file of cuss words, private body parts, and other non-age appropriate words. On top of that, my intention was not to build a library of foul language. As such, I am also choosing to not distribute this file in the repo. I got mine started by prompting Chat GPT:

> I'm working on having a bot generate word searches for children. Can you help me come up with words it should avoid accidentally listing to keep it kid friendly?

(followed up by)

> admittedly, since I try to not use swear words, I don't know very many, but are there others I should be including?

and then

> could we do a plain text format?
>
> Use a pound sign to signal each category and then list each word to avoid on its own line?

From there, I asked it to add a few more things to the list (that reading through it made me think of).

I did also wind up removing some words from the list Chat GPT offered. Notably, it gave me the categories:
- "Adult or Sensitive Topics"
- "Violence, Weapons, or Gore"

(and a few others) that were generally good; however, since I was teaching a Bible class, I chose to not block-list words that are actually likely to be topics of discussion in the context of the Bible (e.g., what happens at the end of life, where we go after that).

**NOTE**: `offensive_words.txt` does not need to be an exhaustive list, because:
1. Any word listed in that file will also match any longer word that starts the same (e.g., `sock` would block `socks` and `socker` as well)
2. If `all_english_words.txt` is used, in theory, there will be NO "bonus" words (foul or otherwise).

## How do I use it?

In future, there may be a website, but for now, this is just a command line tool, so you will need a computer with Python installed on it (version 3.8 or higher, at the time of writing).

1. Download the repo

    <details><summary>Option 1: Using Git (requires having [Git](https://git-scm.com/) installed already)</summary>
    `git clone https://github.com/mshafer1/wordsearch.git`
    </details>
    
    <details open><summary>Option 2: Download a zipfile of the source</summary>
    - Use the "Source" menu at the [top of the repo](https://github.com/mshafer1/wordsearch.git) and select "Download Zip"
    - Extract the zip file
    </details>

1. CD into the repo
   
    `cd wordsearch`

2. Install deps and run the script

    <details><summary>Option 1: Using poetry (requires having [poetry](https://python-poetry.org/) installed)</summary>
    <pre>poetry install</pre>
    <br/>
    <pre>poetry run wordsearch --help</pre>
    </details>
    
    <details open><summary>Option 2: Using a venv</summary>
    <ul>
    <li>Make a virtual environment: <pre>python -m venv .venv</pre></li>
    <li>Install the current project into it: <pre>.venv\Scripts\python.exe -m pip install .</pre></li>
    <li>Run the script <pre>.venv\Scripts\wordsearch --help</li>
    </details>

3. Generating output.

This step is largely individual, but here is an example:

`poetry run wordsearch --hardness-level hard --wordlist-file books_of_nt.txt --width 30 --height 30 --output word_search_file.txt`

(use the output of `--help` to see all options available)

