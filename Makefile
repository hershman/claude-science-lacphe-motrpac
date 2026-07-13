# Reproducibility Makefile — raw data (deposited) -> figures -> compiled PDF
PY=python3
TEX=pdflatex -interaction=nonstopmode
PAPER=paper/cndp2_lacphe_substrate_not_switch

.PHONY: all stats figures pdf clean
all: stats figures pdf

stats:
	$(PY) code/01_compute_statistics.py
	$(PY) code/02_response_stats.py

figures:
	$(PY) code/03_make_figures.py
	$(PY) code/06_boltz_cofold_figure.py
	$(PY) code/04_transparent_backgrounds.py paper/figures

pdf:
	cd paper && $(TEX) $(notdir $(PAPER)).tex && bibtex $(notdir $(PAPER)) || true && $(TEX) $(notdir $(PAPER)).tex && $(TEX) $(notdir $(PAPER)).tex

citations:
	$(PY) code/05_verify_citations.py

clean:
	cd paper && rm -f *.aux *.log *.out *.bbl *.blg
