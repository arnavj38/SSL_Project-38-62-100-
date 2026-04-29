all: report/report.pdf

report/report.pdf: report/report.tex report/gamehub.jpeg report/arcade_bg.jpeg report/leaderboard.jpeg report/tictactoe.jpeg report/othello.jpeg report/connect4.jpeg
	pdflatex report/report.tex
	pdflatex report/report.tex

.PHONY: clean

clean:
	rm *.out *.toc *.aux *.log report.pdf