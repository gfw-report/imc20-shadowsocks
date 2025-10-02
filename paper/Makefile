PDFLATEX = pdflatex -halt-on-error -file-line-error -interaction=nonstopmode -synctex=1
BIBTEX = bibtex

FIGURES = figures/*.pdf figures/*.tex

shadowsocks.pdf: shadowsocks.tex shadowsocks.bib $(FIGURES)

source_latex.zip: shadowsocks.tex shadowsocks.bib $(FIGURES) acmart.cls ACM-Reference-Format.bst figures/Makefile Makefile
	zip -r source_latex.zip shadowsocks.tex shadowsocks.bib acmart.cls ACM-Reference-Format.bst Makefile figures -x figures/__pycache__

# Suppress the warnings and errors until the final round of the compilation.
# This is a workaround to ignore the warnings on undefined citations.
%.pdf: %.tex
	rm -f "$*.aux" "$*.bbl"
	$(PDFLATEX) -draftmode "$*" #> /dev/null
	$(BIBTEX) "$*"
	$(PDFLATEX) -draftmode "$*" #> /dev/null
	$(PDFLATEX) "$*"

.PHONY: clean
clean:
	rm -rf $(addprefix shadowsocks,.aux .ent .log .pdf .bbl .blg .out)

.DELETE_ON_ERROR:
