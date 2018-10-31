from dataset import load_dataset
from tf_functions import random_mini_batches, one_hot_matrix, model, forward_propagation

X_train_orig, X_test_orig, Y_train_orig, Y_test_orig = load_dataset()
# print ("y = " + str(np.squeeze(Y_train_orig[:, 0])))

X_train_flatten = X_train_orig.reshape(X_train_orig.shape[3], -1).T
#print(X_train_flatten[2])
X_test_flatten = X_test_orig.reshape(X_test_orig.shape[3], -1).T
# Normalize image vectors
X_train = X_train_flatten/1740.
X_test = X_test_flatten/1740.
# Convert training and test labels to one hot matrices
Y_train_orig = Y_train_orig.reshape(-1)
Y_test_orig = Y_test_orig.reshape(-1)
Y_train = one_hot_matrix(Y_train_orig, 5)
Y_test = one_hot_matrix(Y_test_orig, 5)

print ("number of training examples = " + str(X_train.shape[1]))
print ("number of test examples = " + str(X_test.shape[1]))
print ("X_train shape: " + str(X_train.shape))
print ("Y_train shape: " + str(Y_train.shape))
print ("X_test shape: " + str(X_test.shape))
print ("Y_test shape: " + str(Y_test.shape))

parameters = model(X_train, Y_train, X_test, Y_test)

