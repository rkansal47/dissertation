from bs4 import BeautifulSoup
from pathlib import Path
import re


maketitle = """
UNIVERSITY OF CALIFORNIA SAN DIEGO
<strong><h2 class="titleHead">Understanding the High Energy Higgs Sector with the CMS
Experiment and Artificial Intelligence</h2></strong>
<br>
A dissertation submitted in partial satisfaction of the
requirements for the degree
Doctor of Philosophy
<br>
<br>
in
<br>
<br>
Physics
<br>
<br>
by
<br>
<br>
<div class="author">Raghav Kansal</div>
<br>
<br>
<br>
Committee in charge:
<br>
Javier Duarte, Chair
<br>
Maurizio Pierini
<br>
Hao Su
<br>
Zhuowen Tu
<br>
Frank Wuerthwein
<br>
<br>
<br>
2024
"""


def edit_file(file_path: Path, edit_function: callable):
    with file_path.open("r") as file:
        soup = BeautifulSoup(file, "html.parser")
        edit_function(soup)

    with file_path.open("w") as file:
        file.write(str(soup))


def edit_main(soup: BeautifulSoup):
    # move the title and abstract inside the main content
    main_content_main = soup.find("main", {"class": "main-content"})

    # remove indent paragraph
    first_paragraph = soup.body.find("p")
    if first_paragraph:
        first_paragraph.decompose()

    maketitle_div = soup.find("div", {"class": "maketitle"})
    maketitle_div.clear()
    maketitle_div.append(BeautifulSoup(maketitle, "html.parser"))
    main_content_main.insert(0, maketitle_div)

    # abstract_section = soup.find("section", {"class": "abstract"})
    # main_content_main.insert(1, abstract_section)

    # Remove the weird default "Next" link
    last_paragraph = main_content_main.find_all("p")[-1]
    last_paragraph.decompose()

    # Add the same type of "Next" as in all the other pages:
    next_nav = soup.new_tag("nav")
    next_nav["class"] = "crosslinks-bottom"
    next_nav.append(soup.new_tag("a", href="Frontmatter.html"))
    next_nav.a.string = "⭢"
    main_content_main.insert(2, next_nav)


def edit_header(soup: BeautifulSoup):
    main_content_main = soup.find("main", {"class": "main-content"})
    if not main_content_main:
        return

    header_link = soup.new_tag(
        "a",
        href="https://github.com/rkansal47/dissertation",
        **{
            "class": "header-link",
            "target": "_blank",
            "rel": "noopener noreferrer",
            "style": "top: 10px; right: 12px;",
        },
    )
    header_img = soup.new_tag(
        "img",
        src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
        alt="GitHub Repository",
        **{"class": "header-icon", "style": "width: 32px; height: 32px;"},
    )
    header_link.append(header_img)
    main_content_main.insert(0, header_link)

    pdf_link = soup.new_tag(
        "a",
        href="https://github.com/rkansal47/dissertation/blob/gh-pages/dissertation.pdf?raw=true",
        **{
            "class": "header-link",
            "target": "_blank",
            "rel": "noopener noreferrer",
            "style": "top: 12px; right: 54px;",
        },
    )
    pdf_img = soup.new_tag(
        "img",
        src="assets/download.png",
        alt="Download PDF",
        **{"class": "header-icon", "style": "width: 25px; height: 25px;"},
    )
    pdf_link.append(pdf_img)
    main_content_main.insert(1, pdf_link)


def edit_footnotes(soup: BeautifulSoup):
    """Move footnotes inside the maincontent div and add a copyright footer"""
    main_content_main = soup.find("main", {"class": "main-content"})
    if not main_content_main:
        return

    footnotes_div = soup.find("div", {"class": "footnotes"})
    if footnotes_div:
        if footnotes_div.contents:
            main_content_main.append(footnotes_div)
        else:
            footnotes_div.decompose()

    footer_div = soup.new_tag("div", **{"class": "footer"})
    footer_p = soup.new_tag("p")
    footer_p.string = "Copyright © 2024 Raghav Kansal. All rights reserved."
    footer_div.append(footer_p)
    main_content_main.append(footer_div)


def edit_toc(soup: BeautifulSoup):
    """Add logo to the Table of Contents"""
    toc_nav = soup.find("nav", {"class": "TOC"})
    if toc_nav:
        main_toc_span = soup.new_tag("span", **{"class": "mainToc"})
        main_toc_link = soup.new_tag("a", href="index.html")
        main_toc_img = soup.new_tag(
            "img",
            src="assets/logo.png",
            alt="Symmetries, QFT, & The Standard Model",
            width="100%",
            **{"class": "mainTocLogo"},
        )
        main_toc_link.append(main_toc_img)
        main_toc_span.append(main_toc_link)
        toc_nav.insert(0, main_toc_span)


def edit_frontmatter(soup: BeautifulSoup):
    # move the title and abstract inside the main content
    main_content_main = soup.find("main", {"class": "main-content"})
    main_content_main.h2["style"] = "text-align: center;"
    main_content_main.div["style"] = "margin-top: 20rem; margin-bottom: 20rem;"


def regex_fixes(file: Path):
    """Workaround for bug with MathML code for subscripts / superscripts with \cancel{}"""
    with file.open("r") as f:
        content = f.read()

    # Apply regex to move <msub|...> tag outside of <menclose> tag
    content = re.sub(
        r'<menclose notation="updiagonalstrike"><(msub|msup|msubsup)>',
        r'<\1><menclose notation="updiagonalstrike">',
        content,
    )

    # Apply regex to move <msub|...> tag outside of <menclose> tag
    content = re.sub(r"main.html", r"index.html", content)

    with file.open("w") as f:
        f.write(content)


if __name__ == "__main__":
    html_files = list(Path(".").glob("*.html"))
    main_file = Path("main.html")

    # This has to be done first, otherwise the html parsing will be messed up
    for html_file in html_files:
        regex_fixes(html_file)

    # Edit the main content
    edit_file(main_file, edit_main)
    edit_file(Path("Dedication.html"), edit_frontmatter)
    edit_file(Path("Epigraph.html"), edit_frontmatter)

    # Edit footnotes for all HTML files in the directory
    for html_file in html_files:
        edit_file(html_file, edit_header)
        edit_file(html_file, edit_footnotes)
        edit_file(html_file, edit_toc)

    # Rename main.html to index.html
    main_file.rename("index.html")

    # Copy main.pdf to standard-model.pdf
    main_pdf = Path("main.pdf")
    notes_pdf = Path("dissertation.pdf")
    notes_pdf.write_bytes(main_pdf.read_bytes())
