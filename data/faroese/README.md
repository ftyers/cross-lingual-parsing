
# Files


* `fao_wiki.txt`: Original Wikipedia without test sentences in
* `fao_wiki.apertium.fao-nob.txt`: Translation of Faroese to Norwegian Bokmål using Apertium
* `fao_wiki.apertium.nob-XXX.txt`: Translation from Norwegian Bokmål to XXX using Apertium
* `fao_wiki.apertium.fao-XXX.input.txt`: Faroese and XXX for input into `fast_align`
* `fao_wiki.apertium.fao-XXX.align.txt`: Alignments produced by `fast_align` + `atools` (symmetrised with `grow-diag-final-and`)


# Todo

* Tokenise the text with UDpipe before running `fast_align` ?
