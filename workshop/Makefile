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
out=raport.pdf
#out="gis-p.kocielnik.pdf"

all: $(in)
	pandoc $(in) -o $(out)
	xdg-open $(out)

ed:
	vim $(in) -c "set syntax=markdown" -c ":Voom markdown"

spellcheck:
	aspell -c $(in) -d pl

pub:
	pandoc $(in) -H quote-setup.tex -o $(out)

show:
	xdg-open $(out)
