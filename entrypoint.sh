#!/bin/sh
# MODE controls which filler(s) to run:
#   cpu (default) - run cpu_filler.py only
#   mem           - run mem_filler.py only
#   all           - run both cpu_filler.py and mem_filler.py concurrently

MODE="${MODE:-cpu}"

if [ "$MODE" = "mem" ]; then
    exec python /mem_filler.py
elif [ "$MODE" = "all" ]; then
    python /cpu_filler.py &
    exec python /mem_filler.py
else
    exec python /cpu_filler.py
fi
