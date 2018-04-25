Random-Attack Resilience of Random and Geometric Graphs
=======================================================

(C) 2018 Jan Kumor, Patryk Kocielnik, Warsaw University of Technology

## Usage

The class with experimental methods is `src/resiliences.py`.

The main notebook for the experiment is `src/report.ipynb`.

To run the notebook you need Jupyter Notebook (formerly iPython Notebook). Install with `pip install jupyter`.

The report (the deliverable) is in the main directory of the project in the PDF file named `report.pdf`.

To generate the report from files located in directory `in` where the report draft is located, issue the `make` command while in the project root directory.

## Project structure

Directory tree:

- `workshop` - Data needed to generate the deliverables (the project engine),
  - `contract` - Requirements for the project,
  - `in` - Source text of the report,
  - `out` - Destination for the generated report,
  - `src` - Source code of the experiment (a Python class + sauce & spinach).

## Report

The report is generated from Markdown.

This approach saves a lot of lots in terms of generation time. To withess this miracle, say `cd workshop` and then `make`.
