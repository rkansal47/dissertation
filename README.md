# Dissertation

[![Codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/rkansal47/dissertation/main.svg)](https://results.pre-commit.ci/latest/github/rkansal47/dissertation/main)

<p align="center">
  <img width="600" src="https://raw.githubusercontent.com/rkansal47/dissertation/refs/heads/main/assets/logo.png" />
</p>

Code for my doctoral dissertation.
Many thanks to Stephen Checkoway for the LaTeX [template](https://github.com/stevecheckoway/ucsddissertation) and Michal Hoftich et. al. for the tex4ht and [make4ht](https://github.com/michal-h21/make4ht) LaTeX to HTML conversion tools.


- [Dissertation](#dissertation)
  - [Compiling the PDF](#compiling-the-pdf)
  - [LaTeX to HTML conversion](#latex-to-html-conversion)


## Compiling the PDF

Some notes for future me:

 - Bibliography entries are first processed using `process_bib.py` to manually fix things like changing the author entry for CMS publications to "CMS Collaboration", removing unnecessary fields, etc.
   - This is added to the VSCode `latex-workshop` build recipe in `.vscode/settings.json`

## LaTeX to HTML conversion

Most of the details and changes needed are described in my standard model notes [README](https://github.com/rkansal47/standard-model?tab=readme-ov-file#notes-for-latex-to-html-conversion).
Some additional changes:

 - Bunch of changes to the `postprocess.py` script, `config.cfg` and `style.css` stylesheet to get the table of contents, main page, organization and some minor visuals right.
 - `pic-tabular` make4ht option for SVG tables; needed because of very complex tables which did not convert well to native HTML.
   - Needed a [fix](https://github.com/rkansal47/dissertation/pull/2) to resolve this minor cosmetic [issue](https://github.com/michal-h21/make4ht/issues/160).
   - Ideally would also like to be able to change the font used in the table SVGs some day.
 - Unfortunately the tex4ht conversion is not able to handle image clippings well :(
