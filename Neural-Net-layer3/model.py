# The main purpose of this code is to define an LSTM model.
import torch.nn as nn
import torch
from dataclasses import dataclass

class Rnn(nn.Module):
    # Initializes the basic parameters of the model
    def __init__(self,vocab_size,output_size,embedding_dim,hidden_dim,num_layers,dropout):
        super(Rnn,self).__init__()
        self.output_size = output_size
        self.num_layers = num_layers
        self.hidden_dim = hidden_dim
        # Transforms input word indices into embedding vectors
        self.embedding = nn.Embedding(vocab_size,embedding_dim)
        # Use for processing sequential data
        self.lstm = nn.LSTM(embedding_dim,hidden_dim,num_layers,dropout=dropout,batch_first=True)
        # Generate the final output from the LSTM layer's output
        self.fc = nn.Linear(hidden_dim,output_size)

        # prevent overfitting
        self.dropout = nn.Dropout(p=0.2)

    # Computes the output through the embedding layer, LSTM layer, dropout layer, and fully connected layer.
    # Returns the final output and the updated hidden layer state.  
    def forward(self,nn_input,hidden):
        batch_size = nn_input.size(0)
        embeds = self.embedding(nn_input)
        lstm_out,hidden = self.lstm(embeds,hidden)
        lstm_out = lstm_out.contiguous().view(-1,self.hidden_dim)
        output = self.dropout(lstm_out)
        output = self.fc(lstm_out)
        output = output.view(batch_size,-1,self.output_size)
        out = output[:,-1]
        return out,hidden
    
    # Initializes the hidden and cell state for the LSTM layer.
    def init_hidden_weights(self,batch_size,gpu_avail):
        weight=next(self.parameters()).data
        if gpu_avail:
            hidden = (weight.new(self.num_layers, batch_size, self.hidden_dim).zero_().cuda(),
            weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().cuda())
        else:
            hidden = (weight.new(self.num_layers, batch_size, self.hidden_dim).zero_(),
            weight.new(self.num_layers, batch_size, self.hidden_dim).zero_())
        
        return hidden

# Stort and manage various hyperparameters of the model
@dataclass
class HyperParams:
    output_size: int 
    vocab_size: int
    epochs: int = 10
    learning_rate: int = 0.0005
    embedding_dim: int = 256
    hidden_dim: int = 500
    num_layers: int = 3 # The RNN model will have 3 LSTM layers
    dropout: int = 0.5