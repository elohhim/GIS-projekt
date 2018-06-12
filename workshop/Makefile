# High-Focus Writing Environment
#
# Dependencies:
# - Vim,
# - Pandoc, and
# - Pdflatex.
#
# Optional dependencies:
# - aspell

in=in/raport.md
out="GIS_Kocielnik_Kumor_Sprawozdanie_3.pdf"

all: $(in)
	pandoc $(in) -H setup.tex -o $(out)
#    xdg-open $(out)

ed:
	vim $(in) -c "set syntax=markdown" -c ":Voom markdown"

spellcheck:
	aspell -c $(in) -d pl

pub:
	pandoc $(in) -H setup.tex -o $(out)

show:
	xdg-open $(out)
