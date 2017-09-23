TARGET = distorted_SASSI_element

build: $(TARGET).tex
	@pdflatex   --shell-escape   $(TARGET)
	@bibtex $(TARGET)
	@pdflatex   --shell-escape   $(TARGET)
	@bibtex $(TARGET)
	@pdflatex   --shell-escape   $(TARGET)
	@pdflatex   --shell-escape   $(TARGET)
	@rm -rf ./*.out ./*.log ./*.aux ./*.bbl ./*.blg ./*.fls ./*latexmk
	@evince ./*.pdf
	@tar -czvf $(TARGET).tar.gz $(TARGET).tex $(TARGET).pdf refmech.bib images


clean: 
	@rm -rf ./*.pdf ./*.out ./*.log ./*.aux ./*.bbl ./*.blg ./*.fls ./*latexmk ./*.tar.gz

close: 
	pkill -9 evince

rebuild: clean build