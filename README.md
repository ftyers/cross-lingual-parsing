# Multi-source synthetic treebank creation for improved cross-lingual dependency parsing

This is an open source implementation of our approach to creating synthetic treebanks for cross-lingual dependency parsing. It includes a combination of:
* machine translation
* annotation projection 
* maximum spanning tree algorithm

Francis Tyers, Mariya Sheyanova, Aleksandra Martynova, Pavel Stepachev and Konstantin Vinogorodskiy.
[*Multi-source synthetic treebank creation for improved cross-lingual dependency parsing*](https://aclweb.org/anthology/W18-6017) *In Proceedings of the Second Workshop on Universal Dependencies (UDW 2018)* EMNLP18 

A part of software created during our research is reused in a [feature UD Annotatrix](https://github.com/hseling/hseling-web-universal-dependencies). The feature aims to make treebanks annotation easier by automatically annotating the sentences.

At the moment, we have a custom extantion of UD Annotatrix with this feature.

In future, it will be merged to [the main repository](https://github.com/jonorthwash/ud-annotatrix).

___
# FAQ

Q: How to use [feature UD Annotatrix](https://github.com/hseling/hseling-web-universal-dependencies)?

A: Please, read our [guide](docs/instructions_docs/how_to_use_OUR_feature.md).

Q: How to deploy?

A: Please, read our [deploy guide](docs/instructions_docs/docker_deploy.md).

Q: Where can I find all useful information about UD Annotatrix tool?

A: Please, check [the main repository](https://github.com/jonorthwash/ud-annotatrix).

___

## Publication

If you use this software for academic research, please cite the paper in question:
```
@InProceedings{W18-6017,
  author = 	"Tyers, Francis
		and Sheyanova, Mariya
		and Martynova, Aleksandra
		and Stepachev, Pavel
		and Vinogorodskiy, Konstantin",
  title = 	"Multi-source synthetic treebank creation for improved cross-lingual dependency parsing",
  booktitle = 	"Proceedings of the Second Workshop on Universal Dependencies (UDW 2018)",
  year = 	"2018",
  publisher = 	"Association for Computational Linguistics",
  pages = 	"144--150",
  location = 	"Brussels, Belgium",
  url = 	"http://aclweb.org/anthology/W18-6017"
}
```
___
## Team and Mentors

### Mentors

* Olga Lyashevskaya
* Francis Tyers

### Team

* Kostya Vinogorodskiy kvinog54@gmail.com
* Sasha Martynova alex250396@gmail.com
* Pasha Stepachev pavel.stepachev@yandex.ru
* Masha Sheyanova masha.shejanova@gmail.com

## Acknowledgements
The article was prepared within the framework of the Academic Fund Programme at the National Research University Higher School of Economics (HSE) in 2016 — 2018 (grant No17-05-0043) and by the Russian Academic Excellence Project «5-100».