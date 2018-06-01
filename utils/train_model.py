import random
import os
import sys

# the path to your UDPipe binary
UDPIPE_PATH = '~/Documents/udpipe-1.2.0-bin/bin-linux64/udpipe'
PATH_TO_GS = ''

def make_tmp_dirs():
    dirnames = ['models', 'predicted']
    for dirname in dirnames:
        if not os.path.exists(dirname):
            os.mkdir(dirname)


def train():
    i = 0
    if not os.path.exists('models/model_' + str(i) + '.udpipe'):
        os.system('../udpipe-1.0.0-bin/bin-linux32/udpipe --tokenizer=\'epochs=10\' --train models/model_'
                  + str(i) + '.udpipe train/' + str(i) + '_training.conllu')
        print('\n===\nThe model ' + str(i) + ' is trained\n===\n')
    else:
        print('Model ' + str(i) + ' pretrained')



def main():
    make_tmp_dirs()
    train()
    print('The model is trained')


if __name__ == '__main__':
    main()
