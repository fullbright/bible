echo "Start bible building"

mkdir _build

echo "Cleaning the _build folder in case it existed"
rm -rf _build/**

cd projects/

pdflatex -interaction=nonstopmode -output-directory ../_build bible_fra_tufte/bible_fra_tufte.tex
pdflatex -interaction=nonstopmode -output-directory ../_build bible_fra_tufte/bible_fra_tufte_full.tex
#pdflatex -interaction=nonstopmode -output-directory ../_build bible/bible.tex
#pdflatex -interaction=nonstopmode -output-directory ../_build bible_fra/bible_fra.tex
#pdflatex -interaction=nonstopmode -output-directory ../_build bible_fra_short/bible_fra_short.tex
#pdflatex -interaction=nonstopmode -output-directory ../_build kjv/bible_fra_short.tex

cd ..

echo "Build building is finished."