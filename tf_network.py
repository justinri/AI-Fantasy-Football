import tensorflow as tf
from data_open import get_data 
import sys
import numpy as np

year = 2017

### Creating and loading stored data
[team_names, team_stats, current_rosters, past_rosters, bio_and_combine, players_stats] = get_data(year)

#2,3,4 = Total_Points,Total_Yards,Total_Plays... only doing stats for current team for now
#train = [stats[2:5] for team in team_names for stats in team_stats[team]][::2]
#train_x = train[:64]
#current = train[32:]

train = [stats[2:5] for stats in team_stats['Dallas_Cowboys']][::2]
train_x = train[:2]
current = train[1:]

#print(len(train_x))
#print(len(current))

### Number of nodes for hidden layers 1,2,3, etc....
nodes = [25, 50, 75]
num_hidden_layers = len(nodes)
len_of_input_data = len(train_x[0])

print(len_of_input_data)
#sys.exit()
### There were two classes, for mnist has numbers 0-9, therefore num of classes = 10
### Batch size, for mnist it would be how many images at a time
num_classes = 3    ### Number of classes, is number of stats your evaluating
batch_size = 1	   ### There are 32 football teams, we will evaluate one year at a time


#print(train_x[0])
#print(current[0])
#sys.exit()

### placeholders for input data. X = data to train, y = correct out come
x = tf.placeholder(tf.float32, [1, len_of_input_data])
y = tf.placeholder(tf.float32)

### Creates a tensor/array of random numbers for weights and biases for hidden layer 1
all_hidden_layers = [{'weights':tf.Variable(tf.random_normal([len_of_input_data, nodes[0]])),\
				      'biases':tf.Variable(tf.random_normal([nodes[0]]))}]

### Creating other hidden layers
for num in range(1,num_hidden_layers):
	hidden_layers = {'weights':tf.Variable(tf.random_normal([nodes[num-1], nodes[num]])),\
				     'biases':tf.Variable(tf.random_normal([nodes[num]]))}
	all_hidden_layers.append(hidden_layers)


### Creates a tensor/array of random numbers for weights and biases for output layer
all_hidden_layers.append({'weights':tf.Variable(tf.random_normal([nodes[-1], num_classes])),\
				  		  'biases':tf.Variable(tf.random_normal([num_classes]))})

def neural_network_model(data):
	## (input_data * weight) + biases - Formula for each layer
	for num in range(num_hidden_layers):
		layer = tf.add(tf.matmul(data, all_hidden_layers[num]['weights']), all_hidden_layers[num]['biases'])
#		layer = tf.add(tf.multiply(data, all_hidden_layers[num]['weights']), all_hidden_layers[num]['biases'])
#		layer = tf.add((data* all_hidden_layers[num]['weights']), all_hidden_layers[num]['biases'])
		layer = tf.nn.relu(layer) # Activation function
		data = layer

	## Output layertf.multiply
	output = tf.matmul(data, all_hidden_layers[-1]['weights']) + all_hidden_layers[-1]['biases']
#	output = tf.multiply(layer, all_hidden_layers[-1]['weights']) + all_hidden_layers[-1]['biases']
#	output = (layer * all_hidden_layers[-1]['weights']) + all_hidden_layers[-1]['biases']

	return output



def train_neural_network(x):
	prediction = neural_network_model(x)
#	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits = prediction, labels = y))

	square_diff = tf.square(prediction - y)
	loss = tf.reduce_sum(square_diff)
	
	## Does have a parameters learning_rate, default 0.001
	optimizer = tf.train.AdamOptimizer().minimize(loss)

	## Cycles of feed forwards + Backprop
	hm_epochs = 1

	with tf.Session() as sess:
		### All variables must initialized
		sess.run(tf.global_variables_initializer())

		## Training the network
		for epoch in range(hm_epochs):
			epoch_loss = 0
			for num in range(2):
				batch_x = np.array(train_x[num])
				batch_y = np.array(current[num])

				_, c = sess.run([optimizer, loss], feed_dict = {x: batch_x, y: batch_y}) 
#				epoch_loss += c
#				
#			print('Epoch', epoch+1, 'Completed out of', hm_epochs, 'Loss:', epoch_loss)


#		correct = tf.equal(tf.argmax(prediction,1), tf.argmax(y,1))
#		accuracy = tf.reduce_mean(tf.cast(correct,'float'))
#		print('Accuracy: ', accuracy.eval({x:current, y:current})*100,'%')
#		
#	return


train_neural_network(x)





