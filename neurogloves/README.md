#### Model Types
`predictor_basic.py` uses a classifier to predict the pose for each emg input. It keeps track of the previous predictions and then predicts the finger position to be `the most common pose/history length`. It started out as a quick hack but then it seems to work well.   

`predictor_grasp.py` is a non ML conversion between EMG signal and hand grasp.  

`predictor.py` loads a Keras model with an input and output scaler and then predicts the curl value for each finger.   

`predictor_rnn.py` keeps track of a deque of the sequence length of an RNN, loads a keras model and predicts the curl value for each finger.  

