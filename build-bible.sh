echo "Start bible building"

mkdir _build
pdflatex -interaction=nonstopmode -output-directory _build projects/bible_fra_tufte/bible_fra_tufte.tex
pdflatex -interaction=nonstopmode -output-directory _build projects/bible_fra_tufte/bible_fra_tufte_full.tex

echo "Build building is finished."