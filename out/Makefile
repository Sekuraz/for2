# Executables
latexmk = latexmk -outdir=build

pandoc = pandoc

# Main file name
MASTER_TEX = project.tex

project.pdf: $(MASTER_TEX) chapters/introduction.tex chapters/this_work.tex chapters/game.tex chapters/learning.tex chapters/results.tex chapters/conclusion.tex chapters/appendix.tex bibliography.bib
	$(latexmk) $(MASTER_TEX)


.PHONY: clean
clean:
	$(latexmk) -C

chapters/%.tex: chapters/%.md
	$(pandoc) --listings -t latex -o $@ $<
