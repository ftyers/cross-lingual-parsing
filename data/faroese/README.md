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
* `fao_wiki.apertium.fao-nob.txt`: Translation of Faroese to Norwegian Bokmål using Apertium
* `fao_wiki.apertium.nob-XXX.txt`: Translation from Norwegian Bokmål to XXX using Apertium
* `fao_wiki.yandex.nob-XXX.txt`: Translation from Norwegian Bokmål to XXX using Yandex
* `fao_wiki.google.nob-XXX.txt`: Translation from Norwegian Bokmål to XXX using Yandex
* `fao_wiki.apertium.fao-XXX.input.txt`: Faroese and XXX for input into `fast_align`
* `fao_wiki.apertium.fao-XXX.align.txt`: Alignments produced by `fast_align` + `atools` (symmetrised with `grow-diag-final-and`)
* `fao_wiki.apertium.fao-XXX.udpipe.parsed.conllu`: XXX parsed with a model trained using UDPipe
* `fao_wiki.apertium.XXX-fao.udpipe.projected.conllu`: Projected UDPipe trees from XXX to Faroese

