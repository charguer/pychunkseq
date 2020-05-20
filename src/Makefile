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

MYPROG=./test.py


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
	$(MYPROG) -length 30 -n 30 -seq debug -chunk_capacity 8
	$(MYPROG) -length 30 -n 30 -seq debug_stdlib -chunk_capacity 8

concat_debug: $(MYPROG)
	$(MYPROG) -test concat -length 1000 -n 1000 -seq debug -chunk_capacity 4


################################################################
# EFFECT OF CHUNK CAPACITY

stack_chunk_capacity: $(MYPROG)
	$(PRUN) -prog $(MYPROG) -seq chunk_stack -n 500000 -length 10,1000,10000,100000,500000 -chunk_capacity 4,8,16,32,64,128
	$(PPLOT) scatter --yzero --xlog -x length -y exectime -series chunk_capacity -legend-pos topleft -output plots_stack_chunk_capacity.pdf



################################################################
# PERFORMANCE

optim: $(MYPROG)
	$(PRUN) $< -n 500000 -length 100,1000,500000 -seq my_chunk_stack,stdlib_back -chunk_capacity 128 -timeout 5
	$(PPLOT) scatter --yzero --xlog -x length -y exectime -series seq -legend-pos topleft -output optim.pdf


stack_perf: $(MYPROG)
	$(PRUN) $< -n 500000 -length 10,1000,10000,500000 -seq chunk_stack,stdlib_back,stdlib_front,container_deque -chunk_capacity 128 -timeout 5
	$(PPLOT) scatter --yzero --xlog -x length -y exectime -series seq -legend-pos topleft -output plots_stack_perf.pdf

list_perf: $(MYPROG)
	$(PRUN) $< -n 500000,5000000 -length 500000 -seq stdlib_list -timeout 5
	$(PPLOT) scatter --yzero --xlog -x n -y exectime -series seq -legend-pos topleft -output plots_stack_perf.pdf

concat_perf: $(MYPROG)
	$(PRUN) $< -test concat -n 500000 -length 10000,50000,100000,500000 -seq chunk_stack,stdlib -timeout 10
	$(PPLOT) scatter --yzero --xlog -x length -y exectime -series seq -legend-pos topleft -output plots_concat_perf.pdf

flatten_perf: $(MYPROG)
	$(PRUN) $< -test flatten -n 500000 -length 1000,10000,500000 -seq chunk_stack,stdlib -timeout 10
	$(PPLOT) scatter --yzero --xlog -x length -y exectime -series seq -legend-pos topleft -output plots_flatten_perf.pdf

# Example command line
# main.py -n 500000 -length 10 -seq pstack -chunk_capacity 32 


# TODO 
# 
# t1 = time()
# repeat n/length fois
#    for i= 0 to length
#        push i
#    for i= 0 to length
#        pop i
# echo ("exectime " + (time() - t1))
 