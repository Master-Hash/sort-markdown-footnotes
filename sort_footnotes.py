#!/usr/bin/python3

import re
import sys

"""
Read a Markdown file via standard input and tidy the containing
Multimarkdown footnotes. The reference links will be numbered in
the order they appear in the text and placed at the bottom
of the file.

Based on "Tidying Markdown reference links" by Dr. Drang available at:

https://leancrew.com/all-this/2012/09/tidying-markdown-reference-links/

Do *not* place footnote reference links at the start of a line, bad things will
happen, your footnotes will be eaten by a grue.
"""

# The regex for finding footnote reference links in the text.
link = re.compile(r"(?<!\n)(\[\^([\d]+)\])")

# The regex for finding the footnote labels with the text.
label = re.compile(r"(?<=\n)\[\^([\d]+)\]:\s?(.*)")


def refrepl(m: re.Match[str]) -> str:
    # Rewrite reference links with the reordered link numbers. Insert the first
    # character from the footnote reference link right before the new link.
    return "[^%d]" % (order.index(m.group(2)) + 1)


# Read in the file and find all the footnote-links and -references.
text = sys.stdin.read()
links = link.findall(text)
labels = dict(label.findall(text))

# Determine the order of the footnote-links in the text. If a link is used
# more than once, its order is its first position.
order: list[str] = []
for i in links:
    if order.count(i[1]) == 0:
        order.append(i[1])

# Make a list of the footnote-references in order of appearance.
newlabels = ["[^%d]: %s" % (i + 1, labels[j]) for (i, j) in enumerate(order)]

# Remove the old footnote-references and put the new ones at the end of the text.
text = label.sub("", text).rstrip() + "\n" * 3 + "\n".join(newlabels) + "\n"

# Rewrite the footnote-links with the new footnote-reference numbers.
text = link.sub(refrepl, text)

print(text)
