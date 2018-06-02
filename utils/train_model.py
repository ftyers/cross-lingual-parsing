import random
import os
import sys

DELEXICALIZE = True # should be true with original language treebanks, False with projections 
UDPIPE_PATH = '~/Documents/udpipe-1.2.0-bin/bin-linux64/udpipe' # the path to your UDPipe binary
FAR_TEST = '~/Documents/UD_Faroese-OFT/fo_oft-ud-test.conllu' # the path to faroese test treebank


def make_tmp_dirs():
    dirnames = ['models', 'predicted']
    for dirname in dirnames:
        if not os.path.exists(dirname):
            os.mkdir(dirname)


def train(corp_name, model_name):
    if not os.path.exists('models/{}'.format(model_name)):
        os.system(UDPIPE_PATH + ' --train --tokenizer=none models/{model} {corp}'\
            .format(model=model_name, corp=corp_name))
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
    if os.path.exists('models/{}'.format(model_name)):
        os.system(
            UDPIPE_PATH + ' --parse models/{0} test_{0}.conllu > result_{0}'\
            .format(model_name)
            )


def cleanup(model_name):
    os.remove('test_{}.conllu'.format(model_name))
    if DELEXICALIZE:
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
    if DELEXICALIZE:
        delexicalize(corp_name, model_name)
        corp_name = 'delexicalised.conllu'
    train(corp_name, model_name)
    predict(model_name)
    cleanup(model_name)


if __name__ == '__main__':
    main()
