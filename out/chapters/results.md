# Proximal Policy Optimization
When only using \gls{ppo} the model had difficulties finding an exit in the 1024 steps within each epoch and bumping into
walls a lot, which was visible as the number of episodes was constantly 1 and the accumulated rewards were large and negative.
The model learned to avoid running into walls quickly but was mostly unable to escape dead ends which left the number of
episodes at 1 but the rewards increased.
Finding the exit consistently could never be observed because the computation time was limited.

# Pre-training
## Finding the Best Model
It became clear really quickly, that the model, the activation and the maze size have big influence on the success
of the training.
Different activation functions \gls{tanh} and \gls{relu} were also compared.
The evaluation accuracy is used as a measure for training success and all available data as provided in 
table \ref{table:dataset} was used in this comparison.

### Opening Encoding
The opening encoding uses a more complex but also more compact encoding as described in \ref{data-encoding} as seen in listing \ref{encoded-data}.

| Model Size | Activation \gls{tanh} | Activation \gls{relu} |
|:----------:|:---------------------:|:---------------------:|
|   64,64    |        0.9439         |        0.9348         |
|  128,128   |        0.9711         |        0.9598         |
|  256,256   |        0.9770         |        0.9865         |
|  512,512   |        0.9785         |        0.9903         |

Table: Training results for 5 by 5 mazes.\label{table:training-5}

| Model Size | Activation: \gls{tanh} | Activation: \gls{relu} |
|:----------:|:----------------------:|:----------------------:|
|   64,64    |         0.5724         |         0.5121         |
|  128,128   |         0.5960         |         0.5473         |
|  256,256   |         0.6186         |         0.5868         |
|  512,512   |         0.6507         |         0.5812         |
| 1024,1024  |         0.5777         |         0.5891         |

Table: Training results for 10 by 10 mazes.\label{table:training-10}

### Binary Encoding

The opening encoding uses a more complex but also more compact encoding as described in \ref{data-encoding} seen in listing \ref{encoded-data-bin}.

| Model Size | Activation: \gls{tanh} | Activation: \gls{relu} |
|:----------:|:----------------------:|:----------------------:|
|   16,16    |         0.8777         |         0.7335         |
|   32,32    |         0.9665         |         0.8680         | 
|   64,64    |         0.9942         |         0.9645         |
|  128,128   |         0.9939         |         0.9962         |
|  256,256   |         0.9981         |         0.9979         |
|  512,512   |         0.9949         |         0.9968         |

Table: Training results for 5 by 5 mazes.\label{table:training-5-bin}


| Model Size | Activation: \gls{tanh} | Activation: \gls{relu} |
|:----------:|:----------------------:|:----------------------:|
|   64,64    |         0.5052         |         0.4651         |
|  128,128   |         0.5638         |         0.4656         |
|  256,256   |         0.5642         |         0.4631         |
|  512,512   |         0.4635         |         0.4449         |
| 1024,1024  |         0.4031         |         0.4454         |

Table: Training results for 10 by 10 mazes.\label{table:training-10-bin}

## Decision for the Model
One notable difference is, that \gls{tanh} activation is better than \gls{relu} activation across all the examples.
There was no notable slowdown from using \gls{tanh} opposed to \gls{relu}.

For small mazes, the binary encoding vastly outperformed the openings encoding and allowed a reduction in model size.
For big mazes, the openings encoding performed substantially better than the binary encoding.
However, for big mazes there was no sufficient accuracy for use in a recursive model like solving a maze so this
approach was not continued.
There were also signs of reduced accuracy when models got too large, especially for large mazes.
The accuracy of the 64,64 model for 5 by 5 mazes was deemed desirable for further study about the influence of the 
amount of training data for pre-training effectiveness. 

## Influence of Available Training Data
After the decision to use binary encoded 5 by 5 mazes, \gls{tanh} activation and 64,64 models, the results in figure \ref{fig:final.png} were obtained.
For the \gls{ppo}, the maximum episode length was set to 64 steps and the first 10 episodes were used to calculate the return after pre-training.

\bigskip
\image{final.png}{Influence of the number of observations on the training effectiveness.}{}

<!--
| Observations | Pre-training Accuracy | Mean \gls{ppo} Return |
|:------------:|:---------------------:|:---------------------:|
|      0       |           0           |         -3.31         |
|     4096     |        0.4951         |         -3.13         |
|     8192     |        0.5732         |         -2.70         |
|    16384     |        0.6760         |         -1.67         |
|    32768     |        0.8563         |         0.74          |
|    49152     |        0.8812         |         3.07          |
|    65536     |        0.9382         |         5.52          |
|    81920     |        0.9623         |         5.27          |

Table: Influence of the number of observations on the training effectiveness. \label{final}
-->
