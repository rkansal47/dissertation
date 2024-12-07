# Understanding the High Energy Higgs Sector with the CMS Experiment and Artificial Intelligence

This is the source code for my doctoral dissertation.
Many thanks to Stephen Checkoway for the LaTeX [template](https://github.com/stevecheckoway/ucsddissertation) and Michal Hoftich for the [make4ht](https://github.com/michal-h21/make4ht) LaTeX to HTML converter.


- [Understanding the High Energy Higgs Sector with the CMS Experiment and Artificial Intelligence](#understanding-the-high-energy-higgs-sector-with-the-cms-experiment-and-artificial-intelligence)
  - [Compiling the PDF](#compiling-the-pdf)
  - [LaTeX to HTML conversion](#latex-to-html-conversion)


## Compiling the PDF

Some notes for future me:

 - Bibliography entries are first processed using `process_bib.py` to manually fix things like changing the author entry for CMS publications to "CMS Collaboration", removing unnecessary fields, etc.
   - This is added to the VSCode `latex-workshop` build recipe in `.vscode/settings.json`


## LaTeX to HTML conversion

Most of the details and changes needed are described in my standard model notes [README](https://github.com/rkansal47/standard-model?tab=readme-ov-file#notes-for-latex-to-html-conversion).
Additional changes:

 - Bunch of changes to the `postprocess.py` script, `config.cfg` and `style.css` stylesheet to get the table of contents, main page, organization and some minor visuals right.
 - `pic-tabular` make4ht option for SVG tables; needed because of very complex tables which did not convert well to native HTML.
 -
