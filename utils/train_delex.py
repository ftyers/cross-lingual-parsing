import random
import os
import sys

UDPIPE_PATH = '~/Documents/udpipe-1.2.0-bin/bin-linux64/udpipe' # the path to your UDPipe binary
FAR_TEST = '~/Documents/UD_Faroese-OFT/fo_oft-ud-test.conllu' # the path to faroese test treebank


def make_tmp_dirs():
    dirnames = ['models', 'predicted', 'results']
    for dirname in dirnames:
        if not os.path.exists(dirname):
            os.mkdir(dirname)


def train_tagger(corp_name, model_name):
    if not os.path.exists('models/{}'.format(model_name)):
        print('training {mod} on {corp}...'.format(mod=model_name, corp=corp_name))
        os.system(UDPIPE_PATH + ' --train --tokenizer=none --parser=none models/tagger_{mod} {corp}'\
            .format(mod=model_name, corp=corp_name))
    else:
        print('Model {} already exists'.format(model_name))


def train_parser(corp_name, model_name):
    if not os.path.exists('models/{}'.format(model_name)):
        print('training {mod} on {corp}...'.format(mod=model_name, corp=corp_name))
        os.system(UDPIPE_PATH + ' --train --tokenizer=none --tagger=none models/parser_{mod} {corp}'\
            .format(mod=model_name, corp=corp_name))
    else:
        print('Model {} already exists'.format(model_name))


def delexicalize(corp_name, model_name):
    with open(os.path.expanduser(corp_name), 'r') as f:
        lines = f.read().split('\n')
        for i, line in enumerate(lines):
            if '\t' in line:
                cols = line.split('\t')
                line = cols[0] + '\t_\t_\t' + '\t'.join(cols[3:])
                lines[i] = line
    with open('delexicalised.conllu', 'w') as f:
        f.write('\n'.join(lines))


def prepare_test_data(model_name):
    with open(os.path.expanduser(FAR_TEST), 'r') as f:
        lines = f.read().split('\n')
        for i, line in enumerate(lines):
            if '\t' in line:
                line = '\t'.join(line.split('\t')[:3])
                line = line + '\t_'*7
                lines[i] = line
    with open('test_{}.conllu'.format(model_name), 'w') as f:
        f.write('\n'.join(lines))


def predict(model_name):
    prepare_test_data(model_name)
    os.system(
        UDPIPE_PATH \
        + ' --tag models/tagger_{0} test_{0}.conllu > tagged_test_{0}.conllu'\
        .format(model_name)
        )
    os.system(
        UDPIPE_PATH \
        + ' --parse models/parser_{0} tagged_test_{0}.conllu > predicted/{0}.conllu'\
        .format(model_name)
        )


def evaluate(model_name):
    os.system(
        'python3 conll18_ud_eval.py --verbose {gs} predicted/{mod}.conllu > results/{mod}.md'\
        .format(gs=FAR_TEST, mod=model_name)
        )


def cleanup(model_name):
    os.remove('test_{}.conllu'.format(model_name))
    os.remove('tagged_test_{}.conllu'.format(model_name))
    os.remove('delexicalised.conllu')


def main():
    if len(sys.argv) != 3:
        print("""Usage: \npython3 train_model.py [corpus] [output_model_name]
    corpus -- the path to the corpus you train the model on (don't use '~')
    output_model_name -- how do you want to call the resulting model
Example:\n    python3 train_model.py rus.conllu rus.udpipe
            """)
        quit()
    corp_name, model_name = sys.argv[1:3]
    make_tmp_dirs()
    train_tagger(corp_name, model_name)
    delexicalize(corp_name, model_name)
    train_parser('delexicalised.conllu', model_name)
    predict(model_name)
    evaluate(model_name)
    cleanup(model_name)


if __name__ == '__main__':
    main()
