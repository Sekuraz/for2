# Executables
latexmk = latexmk -outdir=build

pandoc = pandoc

# Main file name
MASTER_TEX = project.tex

project.pdf: $(MASTER_TEX) chapters/introduction.tex chapters/instrumentation.tex chapters/prelim.tex chapters/results.tex chapters/issues.tex chapters/conclusion.tex bibliography.bib
	$(latexmk) $(MASTER_TEX)


.PHONY: clean
clean:
	$(latexmk) -C

chapters/%.tex: chapters/%.md
	$(pandoc) --listings -t latex -o $@ $<

