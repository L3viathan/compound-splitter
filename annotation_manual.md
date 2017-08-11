Annotation manual
================

For each line:
- Check whether it is valid:
	- Not mainly punctuation (e.g. 500mg/day).
	- Not fragmented or otherwise "unfair".
	- If invalid, remove.
- Remove remaining punctuation (with the exception of hyphens etc.)
- Annotate as many lines as possible.

Annotation:
----------

The first column is the original token, the second column the annotated version:

- Seperate compound parts with a plus sign: dampf+schiff
- Split off binding morphemes with a pipe symbol: lösung|s+mittel
- Put morphological suffixes in parantheses: dampf+schiff(e)
- Where morphology also changed letters inside the word (e.g. ablaut), capitalize them: krebs+fAll(e) (from Krebsfälle)

Whenever a word is a non-compound, no annotation is necessary at all (i.e. leave the second column as an exact copy of the first, do not annotate morphology etc.)

Do not decompound brand and other names.

Compounds that are parts of a word the current word is *derived* from, are not to be annotated:
"verstoffwechselt" contains "Stoffwechsel", but as a single unit and you can not split the adjective into "verstoff" and "wechselt".

Foreign words do not get split, unless they are lexicalized, but are also not skipped.

Trivial changes that make a un-annotatable example annotatable can be done, like frankreich2 -> frankreich.


Example: Beginning of the German annotations:
---------------------------------------------
anwendung	anwendung
beachten	beachten
weitere	weitere
warnhinweise	warn+hinweis(e)
vorsichtsmaßnahmen	vorsicht|s+maßnahme(n)
anwendung	anwendung
cholestagel	cholestagel
angewendet	angewendet
einnahme	einnahme
bondenza	bondenza
