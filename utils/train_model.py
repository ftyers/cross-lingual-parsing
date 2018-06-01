import random
import os
import sys

# the path to your UDPipe binary
UDPIPE_PATH = '~/Documents/udpipe-1.2.0-bin/bin-linux64/udpipe'


def make_tmp_dirs():
    dirnames = ['models', 'predicted']
    for dirname in dirnames:
        if not os.path.exists(dirname):
            os.mkdir(dirname)


def train(corp_name, model_name):
    if not os.path.exists('models/{}'.format(model_name)):
        os.system(UDPIPE_PATH + ' --train models/{model} {corp}'\
            .format(model=model_name, corp=corp_name))
        print('===\nThe model {} is trained\n==='.format(model_name))
    else:
        print('Model {} already exists'.format(model_name))


def main():
    if len(sys.argv) != 2:
        print("""
            Usage: \npython3 train_model.py [corpus] [output_model_name]
            corpus -- the path to the corpus you train the model on
            output_model_name -- hoe do you want to call the resulting model
            Example:\npython3 train_model.py rus.conllu rus.udpipe
            """)
    corp_name, model_name = sys.argv[:2]
    make_tmp_dirs()
    train(corp_name, model_name)
    print('The model is trained!')


if __name__ == '__main__':
    main()
