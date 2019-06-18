#

# Example usage:
#    make stack_perf && make show


################################################################
# OPTIONS

# Access to pbench requires, e.g.
# export PATH=~/pbench:$PATH

# Copy-pasting commands requires
# export PATH=$PATH:.

# Interrupt with ctrl+x in terminal  :  stty intr ^X


################################################################

PRUN=prun
PPLOT=pplot

MYPROG=./test.sh


################################################################
# DEFAULT TARGET

all:
	@echo "Usage, e.g.: make stack_perf"


################################################################
# clean (probably not needed for Python)

# clean:
#	rm -f *.dbg *.out *.opt *.dbg *.cmx *.cmxa *.cmi *.cmo *.cma *.o


################################################################
# SHOW

# `make show` displays the most recent plots*.pdf program
# usage, e.g.: "make stack_perf && make show"

show:
	evince `ls -t plots*.pdf | head -n 1`


################################################################
# DEBUGGING

# Debugging: usage, e.g.
# make SEQ=StackListOfChunks stack_debug

stack_debug: $(MYPROG)
	$(MYPROG) -debug 1 -nb_repeat 1 -n 30 -seq chunk_stack -chunk_capacity 8



################################################################
# EFFECT OF CHUNK CAPACITY

stack_chunk_capacity: $(MYPROG)
	$(PRUN) -prog $(MYPROG) -seq chunk_stack -n 5000000 -length 10,1000,10000,1000000,2000000,5000000 -chunk_capacity 32,64,128,256,512,1024,4096
	$(PPLOT) scatter --yzero --xlog -x length -y exectime -series chunk_capacity -legend-pos topleft -output plots_stack_chunk_capacity.pdf



################################################################
# PERFORMANCE

stack_perf: $(MYPROG)
	$(PRUN) $< -test stack_repeat_pushn_popn -n 5000000 -length 10,1000,10000,100000,500000 -seq chunk_stack,stdlib_list,container_deque -chunk_capacity 256 -timeout 10
	$(PPLOT) scatter --yzero --xlog -x length -y exectime -series seq -legend-pos topleft -output plots_stack_perf.pdf

