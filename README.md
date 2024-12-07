# Understanding the High Energy Higgs Sector with the CMS Experiment and Artificial Intelligence

This is the source code for my doctoral dissertation.
Many thanks to Stephen Checkoway for the [template](https://github.com/stevecheckoway/ucsddissertation).


## Abstract

This dissertation is a guide to understanding the Higgs boson at the highest energies possible, using the CMS experiment at the Large Hadron Collider and the latest advances in artificial intelligence and machine learning.
It presents a search for new particles in the Higgs sector and a measurement of the properties of the standard-model Higgs boson of the quartic Higgs-to-vector-boson-couping via a search for double-Higgs production in the all-hadronic bbVV channel, in particular a novel and sensitive strategy to corner the two-Higgs-to-two-vector-boson coupling
Complementarily, it discusses a search for possible new siblings of the Higgs boson in the same channel.
It presents as well significant developments using geometric deep learning and transformers in classifying Higgs bosons, particularly in the boosted WW decay mode, to enable these searches, and in fast simulations of the CMS detector to expand our future physics reach.
Finally, it discusses novel approaches to search for new physics in a model-independent manner using equivariant ML, notably in a way that for first time respects the Lorentz-group symmetry.

## Building

Some notes for future me:

 - Bibliography entries are first processed using `process_bib.py` to manually fix things like changing the author entry for CMS publications to "CMS Collaboration", removing unnecessary fields, etc.
   - This is added to the VSCode `latex-workshop` build recipe in `.vscode/settings.json`