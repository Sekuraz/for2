# Proximal Policy Optimization
When only using \gls{ppo} the model had difficulties finding an exit in the 1024 steps within each epoch and bumping into
walls a lot, which was visible as the number of episodes was constantly 1 and the accumulated rewards were large and negative.
The model learned to avoid running into walls quickly but was mostly unable to escape dead ends which left the number of
episodes at 1 but the rewards increased.
Finding the exit consistently could never be observed because the computation time was limited.

# Pre-training
