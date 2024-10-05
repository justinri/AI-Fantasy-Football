import tensorflow as tf
from data_open import get_data 
import sys

year = 2017

### Creating and loading stored data
[team_names, team_stats, current_rosters, past_rosters, bio_and_combine, players_stats] = get_data(year)


## Starting Weights and biases
weights = tf.Variable([.3], tf.float32)
biases = tf.Variable([-.3], tf.float32)

### placeholders for input data. X = data to train, y = correct out come
x = tf.placeholder(tf.float32)
y = tf.placeholder(tf.float32)

### Input data
#train = [stats[2:5] for team in team_names for stats in team_stats[team]][::2]
train = [stats[2:5] for stats in team_stats['Dallas_Cowboys']][::2]
train_x = train[0]
current = train[1]

print(train_x)
print(current)


### Model type
linear_model = (weights*x) + biases

with tf.Session() as sess:
	init = tf.global_variables_initializer()
	sess.run(init)

	square_diff = tf.square(linear_model - y)
	loss = tf.reduce_sum(square_diff)

	### Optimizing
	optimizer = tf.train.GradientDescentOptimizer(0.01)
	train = optimizer.minimize(loss)	
		
	for i in range(2):
		sess.run(train, {x: train_x, y: current})
	
	###
	print(sess.run([weights, biases]))

