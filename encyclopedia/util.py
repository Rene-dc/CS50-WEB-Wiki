import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def convert_markdown(text):
    text = re.sub(r'\r\n', r'\n', text)
    text = re.sub(r'\r', r'\n', text)
    # Titles
    text = re.sub(r'^#{6} (.*)', r'<h6>\1</h6>', text, flags=re.M)
    text = re.sub(r'^#{5} (.*)', r'<h5>\1</h5>', text, flags=re.M)
    text = re.sub(r'^#{4} (.*)', r'<h4>\1</h4>', text, flags=re.M)
    text = re.sub(r'^#{3} (.*)', r'<h3>\1</h3>', text, flags=re.M)
    text = re.sub(r'^#{2} (.*)', r'<h2>\1</h2>', text, flags=re.M)
    text = re.sub(r'^#{1} (.*)', r'<h1>\1</h1>', text, flags=re.M)

    # Links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)

    # Bold text
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

    # Italic text
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)

    # Unordered lists
    text = re.sub(r'([\*\-\+] (.+\n)*)', r'<ul>\n\1</ul>\n', text, flags=re.M)
    text = re.sub(r'[\*\-\+] (.+)', r'<li>\1</li>', text)

    # Ligne change
    text = re.sub(r'  \r?\n', r'<br />', text)
    
    # Paragraphs
    text = re.sub(r'\r?\n\r?\n([a-zA-Z0-9<].*)', r'<p>\1</p>', text)
    print(text)

    return text
    