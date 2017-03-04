import tensorflow as tf
import numpy as np

from PIL import Image

def DisplayFractal(a):
    a_cyclic = (6.28*a/20.0).reshape(list(a.shape)+[1])
    img = np.concatenate([10+20*np.cos(a_cyclic),
                          30+50*np.sin(a_cyclic),
                          155-80*np.cos(a_cyclic)], 2)
    img[a==a.max()] = 0
    a = img
    im = Image.fromarray(np.uint8(np.clip(a, 0, 255)))
    im.show()

sess = tf.InteractiveSession()

Y, X = np.mgrid[-1.3:1.3:0.005, -2:1:0.005]
Z = X+1j*Y

xs = tf.constant(Z.astype(np.complex64))
zs = tf.Variable(xs)
ns = tf.Variable(tf.zeros_like(xs, tf.float32))

tf.global_variables_initializer().run()

zs_ = zs*zs + xs

not_diverged = tf.abs(zs_) < 4

step = tf.group(
    zs.assign(zs_),
    ns.assign_add(tf.cast(not_diverged, tf.float32))
)

for i in range(200): step.run()

DisplayFractal(ns.eval())
