import sys
sys.path.append(r'/Users/kadriansyah/Projects/personal/python/anago')

import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import json
import anago
MODEL_PATH = os.path.dirname(os.path.abspath(__file__)) + '/model'

model = anago.Sequence.load(MODEL_PATH)
words_1 = 'Pagi dok. Saya mau menanyakan, ibu saya setahun yg lalu di diagnosa kanker nasofaring stadium IV B dan sudah menjalani proses pengobatan dan ini dinyatakan sembuh secara outlook namun belum dilakukan CT Scan utk melihat lebih jelas nya dan dijadwalkan di akhir januari nanti. Nah dalam tahap penyembuhan ini, ibu saya masih mengeluh tentang telinga yang berdengung dan masih ada seperti ingus di hidung yang tersumbat meskipun tidak ada darah lagi. Apakah itu normal dok? Dan beberapa hari lalu ibu saya merasakan ada benjolan di bagian bawah dagu dan di bawah telinga kiri. Apakah itu berarti kanker yg diderita belum total sembuh? Terimakasih dokter'.split()
print(model.analyze(words_1))
