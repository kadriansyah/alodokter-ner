import argparse
import os

from anago.utils import load_data_and_labels
from anago.models import BiLSTMCRF
from anago.preprocessing import IndexTransformer
from anago.trainer import Trainer
from keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.python.lib.io import file_io

def main(args):
    print('Loading dataset...')
    print(args.train_data)
    x_train, y_train = load_data_and_labels(os.path.join(args.data_dir, args.train_data))
    x_valid, y_valid = load_data_and_labels(os.path.join(args.data_dir, args.valid_data))

    print('Transforming datasets...')
    p = IndexTransformer(use_char=args.no_char_feature)
    p.fit(x_train, y_train)

    print('Building a model.')
    model = BiLSTMCRF(char_embedding_dim=args.char_emb_size,
                      word_embedding_dim=args.word_emb_size,
                      char_lstm_size=args.char_lstm_units,
                      word_lstm_size=args.word_lstm_units,
                      char_vocab_size=p.char_vocab_size,
                      word_vocab_size=p.word_vocab_size,
                      num_labels=p.label_size,
                      dropout=args.dropout,
                      use_char=args.no_char_feature,
                      use_crf=args.no_use_crf)
    model, loss = model.build()
    model.compile(loss=loss, optimizer=args.optimizer)

    print('Training the model...')
    callback = [EarlyStopping(monitor='loss', patience=5), ModelCheckpoint(filepath=os.path.join(args.save_dir, args.best_weights_file), monitor='f1', save_best_only=True)]
    trainer = Trainer(model, preprocessor=p)
    trainer.train(x_train,
                  y_train,
                  x_valid,
                  y_valid,
                  epochs=args.max_epoch,
                  batch_size=args.batch_size,
                  callbacks=callback,
                  verbose=1)

    print('Saving the model...')
    model.save(os.path.join(args.save_dir, args.weights_file), os.path.join(args.save_dir, args.params_file))
    p.save(os.path.join(args.save_dir, args.preprocessor_file))

    # work arround Keras issue using GCS, Copy model.h5 over to Google Cloud Storage
    # best_weights_file
    with file_io.FileIO(os.path.join(args.save_dir, args.best_weights_file), mode='r') as input_f:
        with file_io.FileIO(os.path.join(args.job-dir, args.best_weights_file), mode='w+') as output_f:
            output_f.write(input_f.read())
    
    # weights_file
    with file_io.FileIO(os.path.join(args.save_dir, args.weights_file), mode='r') as input_f:
        with file_io.FileIO(os.path.join(args.job-dir, args.weights_file), mode='w+') as output_f:
            output_f.write(input_f.read())

    # preprocessor_file
    with file_io.FileIO(os.path.join(args.save_dir, args.preprocessor_file), mode='r') as input_f:
        with file_io.FileIO(os.path.join(args.job-dir, args.preprocessor_file), mode='w+') as output_f:
            output_f.write(input_f.read())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Training a model')
    parser.add_argument('--data_dir', default=os.path.join(os.path.dirname(__file__), 'data'), help='training data directory')
    parser.add_argument('--save_dir', default=os.path.join(os.path.dirname(__file__), 'models'), help='models directory')

    # ml-engine requirement params
    parser.add_argument('--job-dir', default='/tmp/aloner_output', help='job dir')

    parser.add_argument('--train_data', default='train.txt', help='training data')
    parser.add_argument('--valid_data', default='valid.txt', help='validation data')
    parser.add_argument('--weights_file', default='weights.h5', help='weights file')
    parser.add_argument('--best_weights_file', default='best_weights.h5', help='best weights file')
    parser.add_argument('--params_file', default='params.json', help='parameter file')
    parser.add_argument('--preprocessor_file', default='preprocessor.json')

    # Training parameters
    parser.add_argument('--loss', default='categorical_crossentropy', help='loss')
    parser.add_argument('--optimizer', default='adam', help='optimizer')
    parser.add_argument('--max_epoch', type=int, default=15, help='max epoch')
    parser.add_argument('--batch_size', type=int, default=32, help='batch size')
    parser.add_argument('--checkpoint_path', default=None, help='checkpoint path')
    parser.add_argument('--log_dir', default=None, help='log directory')
    parser.add_argument('--early_stopping', action='store_true', help='early stopping')

    # Model parameters
    parser.add_argument('--char_emb_size', type=int, default=25, help='character embedding size')
    parser.add_argument('--word_emb_size', type=int, default=100, help='word embedding size')
    parser.add_argument('--char_lstm_units', type=int, default=25, help='num of character lstm units')
    parser.add_argument('--word_lstm_units', type=int, default=100, help='num of word lstm units')
    parser.add_argument('--dropout', type=float, default=0.5, help='dropout rate')
    parser.add_argument('--no_char_feature', action='store_false', help='use char feature')
    parser.add_argument('--no_use_crf', action='store_false', help='use crf layer')

    args = parser.parse_args()
    main(args)