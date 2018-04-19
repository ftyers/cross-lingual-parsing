# Pipeline

```
       		 ┌─>swe(Google Translate, Yandex Translate,Apertium)
       		 |
fao─>nob(Apertium)─>nno(Apertium)
       		 |
       		 └─>dan(Google Translate,Yandex Translate,Apertium)
```

# Files


* `fao_wiki.txt`: Original Wikipedia without test sentences in
 * This is the raw input text.
* `fao_wiki.apertium.fao-nob.txt`: Translation of Faroese to Norwegian Bokmål using Apertium
 * Produced using `apertium` and `apertium-fao-nor`
* `fao_wiki.apertium.nob-XXX.txt`: Translation from Norwegian Bokmål to XXX using Apertium
 * Produced using `apertium` and `apertium-XXX-YYY`
* `fao_wiki.yandex.nob-XXX.txt`: Translation from Norwegian Bokmål to XXX using Yandex
* `fao_wiki.google.nob-XXX.txt`: Translation from Norwegian Bokmål to XXX using Google
* `fao_wiki.tokenised.txt`: Tokenised version of `fao_wiki.txt`
 * This is generated using `tokeniser.py`
* `fao_wiki.apertium.fao-XXX.input.txt`: Faroese and XXX for input into `fast_align`
* `fao_wiki.apertium.fao-XXX.align.txt`: Token alignments for fao to XXX
 * Generated using `fast_align` + `atools` (symmetrised with `grow-diag-final-and`)
* `fao_wiki.apertium.fao-XXX.udpipe.parsed.conllu`: XXX parsed with a model trained using UDPipe
 * This is generated using `udpipe`
* `fao_wiki.apertium.XXX-fao.udpipe.projected.conllu`: Projected UDPipe trees from XXX to Faroese
 * This is generated using `project-aligned-trees.py`
