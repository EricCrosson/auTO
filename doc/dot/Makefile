# build an executable named myprog from myprog.c
all: pipeline.gv
		dot -Gsplines=none pipeline.gv | neato -n -Gsplines=ortho -Tpng -opipeline.png

clean: 
		$(RM) popeline.png
