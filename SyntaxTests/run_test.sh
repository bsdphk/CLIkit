#!/bin/sh


python ../CLIkit.py --code
for i in good*.ck
do
	b=`basename $i .ck`
	rm -f $b.[ch] _.$b
	if python ../CLIkit.py --tree $i > _.$b 2>&1; then
		true
	else
		echo "###" Failure $b
		cat _.$b
		rm -f $b.[ch] _.$b
		continue
	fi
	if cc -c -Wall -I. ${b}.c > _.$b 2>&1 ; then
		echo "===" Success $b
	else
		echo "### Compile failure $b"
		cat _.$b
	fi
	rm -f $b.[cho] _.$b
done

for i in bad*.ck
do
	b=`basename $i .ck`
	rm -f $b.[ch] _.$b
	if python ../CLIkit.py --tree $i > _.$b 2>&1 ; then
		echo "###" Failure $b
		cat _.$b
	else
		echo "===" Success $b
	fi
	rm -f $b.[ch] _.$b
done

rm -f clikit.[ch]
