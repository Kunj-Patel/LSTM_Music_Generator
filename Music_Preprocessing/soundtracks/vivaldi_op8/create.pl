#!/bin/sh
#
# CREATE
#
# This script is used to generate all possible source variants of the
# Vivaldi Concertos, Opus 8.

# Ensure that the input file is available.

if [ -d turino ]
then
	echo ""
else
	echo "Creating \"turino\" subdirectory ..."
	mkdir turino
fi
exit
if [ -f $2 ]
then
	echo ""
else
	echo "$2: File not found."
	exit
fi
if [ X"$1" = X-A ]
then
	echo "Extracting Amsterdam print for file $2  ..."
fi
if [ X"$1" = X-D ]
then
	echo "Extracting Dresden manuscript for file $2  ..."
fi
if [ X"$1" = X-M ]
then
	echo "Extracting Manchester partbook for file $2  ..."
fi
if [ X"$1" = X-T ]
then
	echo "Extracting Turino autograph for file $2  ..."
fi
if [ X"$1" = X-S ]
then
	echo "Extracting Selfridge-Field edition for file $2  ..."
fi
exit

if [ X$1 = Xop8n01a.krn ]
then
	do
	# Choices for op8n01a:
	strophe -x A op8n01a.krn > amsterdm/op8n01aa.krn	# Amsterdam print.
	strophe -x S op8n01a.krn > critical/op8n01as.krn	# Selfridge-Field edition.
	done
fi
exit

# Choices for op8n01b.krn: No alternatives for op8n01b.krn

# Choices for op8n01c.krn:
strophe -x A op8n01c.krn > amsterdm/op8n01ca.krn	# Amsterdam print.
strophe -x S op8n01c.krn > critical/op8n01cs.krn	# Selfridge-Field edition.

# Choices for op8n02a.krn:
thru -v Selfridge-Field op8n02a.krn | strophe -x S > critical/op8n02as.krn
thru -v Amsterdam op8n02a.krn | strophe -x A > amsterdm/op8n02aa.krn

# Choices for op8n02b.krn:
strophe -x A op8n02b.krn > amsterdm/op8n02ba.krn	# Amsterdam print.
strophe -x S op8n02b.krn > critical/op8n02bs.krn	# Selfridge-Field edition.

# Choices for op8n02c.krn:
thru -v Selfridge-Field op8n02c.krn | strophe -x S > critical/op8n02cs.krn	# Selfridge-Field edition.
thru -v Amsterdam op8n02c.krn | strophe -x A > amsterdm/op8n02ca.krn
thru -v Manchester op8n02c.krn | strophe -x M > manchest/op8n02cm.krn	# Manchester part-books.

# Choices for op8n03a.krn:
thru -v Selfridge-Field op8n03a.krn | strophe -x S > critical/op8n03as.krn	# Selfridge-Field edition.
thru -v Amsterdam op8n03a.krn | strophe -x A > amsterdm/op8n03aa.krn
thru -v Manchester op8n03a.krn | strophe -x M > manchest/op8n03am.krn	# Manchester part-books.

# Choices for op8n03b.krn: No alternatives for op8n03b.krn

# Choices for op8n03c.krn:
thru -v Selfridge-Field op8n03c.krn | strophe -x S > critical/op8n03cs.krn	# Selfridge-Field edition.
thru -v Manchester op8n03c.krn | strophe -x M > manchest/op8n03cm.krn	# Manchester part-books.
thru -v Amsterdam op8n03c.krn | strophe -x A > amsterdm/op8n03ca.krn

# Choices for op8n04a.krn:
thru -v Selfridge-Field op8n04a.krn > critical/op8n04as.krn	# Selfridge-Field edition.
thru -v Manchester op8n04a.krn | sed 's/cemba/organ/' > manchest/op8n04am.krn	# Manchester part-books.
thru -v Amsterdam op8n04a.krn > amsterdm/op8n04aa.krn

# Choices for op8n04b.krn:
strophe -x S op8n04b.krn > critical/op8n04bs.krn
strophe -x M op8n04b.krn > manchest/op8n04bm.krn

# Choices for op8n04c.krn:
thru -v Selfridge-Field op8n04c.krn | strophe -x S > critical/op8n04cs.krn	# Selfridge-Field edition.
thru -v Manchester op8n04c.krn | strophe -x M > manchest/op8n04cm.krn	# Manchester part-books.
thru -v Amsterdam op8n04c.krn | strophe -x A > amsterdm/op8n04ca.krn

# Choices for op8n05a.krn:
thru -v Selfridge-Field op8n05a.krn | strophe -x S > critical/op8n05as.krn	# Selfridge-Field edition.
thru -v Manchester op8n05a.krn | strophe -x M > manchest/op8n05am.krn	# Manchester part-books.
thru -v Amsterdam op8n05a.krn | strophe -x A > amsterdm/op8n05ca.krn

# Choices for op8n05b.krn:
Strophes: S A
#thru -v Selfridge-Field op8n05b.krn | strophe -x S > critical/op8n05bs.krn	# Selfridge-Field edition.
#thru -v Manchester op8n05b.krn | strophe -x M > manchest/op8n05bm.krn	# Manchester part-books.
#thru -v Amsterdam op8n05b.krn | strophe -x A > amsterdm/op8n05cb.krn

# Choices for op8n05c.krn:
#Strophes: S A D M
thru -v Selfridge-Field op8n05c.krn | strophe -x S > critical/op8n05cs.krn	# Selfridge-Field edition.
thru -v Manchester op8n05c.krn | strophe -x M > manchest/op8n05cm.krn	# Manchester part-books.
thru -v Dresden op8n05c.krn | strophe -x D > dresden/op8n05cd.krn	# Dresden manuscript.
thru -v Amsterdam op8n05c.krn | strophe -x A > amsterdm/op8n05ca.krn

# Choices for op8n06a.krn:
strophe -x S op8n06a > critical/op8n06sa.krn	# Selfridge-Field
strophe -x A op8n06a > amsterdm/op8n06aa.krn	# Amsterdam

# Choices for op8n06b.krn:
strophe -x S op8n06b > critical/op8n06sb.krn	# Selfridge-Field
strophe -x A op8n06b > amsterdm/op8n06ab.krn	# Amsterdam

# Choices for op8n06c.krn:
strophe -x S op8n06c > critical/op8n06sc.krn	# Selfridge-Field
strophe -x A op8n06c > amsterdm/op8n06ac.krn	# Amsterdam

# Choices for op8n07a.krn:
strophe -x S op8n07a > critical/op8n07sa.krn	# Selfridge-Field
strophe -x A op8n07a > amsterdm/op8n07aa.krn	# Amsterdam

# Choices for op8n07b.krn: No alternatives for op8n07b.krn

# Choices for op8n07c.krn:
strophe -x S op8n07c > critical/op8n07sc.krn	# Selfridge-Field
strophe -x A op8n07c > amsterdm/op8n07ac.krn	# Amsterdam

# Choices for op8n08a.krn:
thru -v Selfridge-Field op8n08a.krn | strophe -x S > critical/op8n08as.krn	# Selfridge-Field edition.
thru -v Turino op8n08a.krn | strophe -x T > turino/op8n08at.krn
thru -v Amsterdam op8n08a.krn | strophe -x A > amsterdm/op8n08ca.krn

# Choice for op8n08b.krn:
# In the Turino autograph, violino 1 duplicated violino 2 for the first
# seven measures (spine 4);  later this was changed to "Unisoni" so
# that violino 1 duplicates violino principale throughout (spine 5).
extract -f 1-3,5-7 op8n08b.krn > turino/op8n08bt.krn	# Revised Turino
extract -f 1-4,6-7 op8n08b.krn > turino/op8n08bt.krn	# Original Turino

# Choices for op8n08c.krn:
thru -v Selfridge-Field op8n08c.krn | strophe -x S > critical/op8n08cs.krn	# Selfridge-Field edition.
thru -v Turino op8n08c.krn | strophe -x S > turino/op8n08ct.krn
thru -v Amsterdam op8n08c.krn | strophe -x A > amsterdm/op8n08ca.krn

# Choices for op8n09a.krn:
# Oboe concerto RV 454 (Turino manuscript):
thru -v Selfridge-Field op8n09a.krn | strophe -x S | extract -f 1-4,6-7 > critical/op8n09ao.krn	# Selfridge-Field edition.
# Violin concerto RV 236:
thru -v Selfridge-Field op8n09a.krn | strophe -x S | extract -f 1-5,7 > critical/op8n09as.krn	# Selfridge-Field edition.
thru -v Amsterdam op8n09a.krn | strophe -x A | extract -f 1-5,7 > amsterdm/op8n09aa.krn

# Choices for op8n09b.krn:
# Oboe concerto RV 454 (Turino manuscript):
thru -v Selfridge-Field op8n09b.krn | strophe -x S | extract -f 1,3,4 > critical/op8n09bo.krn	# Selfridge-Field edition.
# Violin concerto RV 236:
thru -v Selfridge-Field op8n09b.krn | strophe -x S | extract -f 1,2,4 > critical/op8n09bs.krn	# Selfridge-Field edition.
thru -v Amsterdam op8n09b.krn | strophe -x A | extract -f 1,2,4 > amsterdm/op8n09ba.krn

# Choices for op8n09c.krn:
# Oboe concerto RV 454 (Turino manuscript):
thru -v Selfridge-Field op8n09c.krn | extract -f 1-4,6-7 > critical/op8n09co.krn	# Selfridge-Field edition.
thru -v Turino op8n09c.krn | extract -f 1-4,6-7 > turino/op8n09ct.krn
# Violin concerto RV 236:
thru -v Selfridge-Field op8n09c.krn | extract -f 1-5,7 > critical/op8n09cs.krn	# Selfridge-Field edition.
thru -v Amsterdam op8n09c.krn | extract -f 1-5,7 > amsterdm/op8n09cc.krn

# Choices for op8n10a.krn:
thru -v Selfridge-Field op8n10a.krn > critical/op8n10as.krn	# Selfridge-Field edition.
thru -v Turino op8n10a.krn > turino/op8n10at.krn
thru -v Amsterdam op8n10a.krn > amsterdm/op8n10aa.krn

# Choices for op8n10b.krn:
# This movement has a binary (A-B) form; repeats are marked for both
# the A and B sections.  In the following versions, the label "rep"
# means that both A and B sections are repeated, the lable "norep"
# means that none of the sections are repeated.  Without either "rep"
# or "norep", the A section is repeated, but not the B section.
thru -v Selfridge-Field op8n10b.krn > critical/op8n10bs.krn	# Selfridge-Field edition.
thru -v Selfridge-Field_rep op8n10b.krn > critical/op8n10bs.krn	# Selfridge-Field edition.
thru -v Selfridge-Field_norep op8n10b.krn > critical/op8n10bs.krn	# Selfridge-Field edition.
thru -v Amsterdam op8n10b.krn > amsterdm/op8n10ba.krn
thru -v Amsterdam op8n10b.krn_rep > amsterdm/op8n10ba.krn
thru -v Amsterdam op8n10b.krn_norep > amsterdm/op8n10ba.krn

# Choices for op8n10c.krn:
thru -v Selfridge-Field op8n10c.krn > critical/op8n10cs.krn	# Selfridge-Field edition.
thru -v Amsterdam op8n10c.krn > amsterdm/op8n10ca.krn
thru -v Dresden op8n10c.krn > dresden/op8n10cd.krn	# Dresden manuscript.
thru -v Turino op8n10c.krn > turino/op8n10ct.krn

# Choices for op8n12a.krn:
strophe -x S op8n12a.krn > critical/op8n12sa.krn
strophe -x A op8n12a.krn > amsterdm/op8n12aa.krn

# Choices for op8n12b.krn: No alternatives for op8n12b.krn

# Choices for op8n12c.krn:
thru -v Selfridge-Field op8n12c.krn | strophe -x S > critical/op8n12cs.krn	# Selfridge-Field edition.
thru -v Amsterdam op8n12c.krn | strophe -x A > amsterdm/op8n12ca.krn
