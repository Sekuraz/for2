# Effectiveness
As seen in the previous figure \ref{fig:final.png}, the amount of collected data has a significant influence over the
collected reward of the agent.
This proves, that pre-training, even with a small amount of data, is an effective start for a subsequent \gls{ppo} training.
However, those results were obtained after carefully optimizing the model and the environment representation to make
learning as efficient as possible for the agent.

# Mapping of the Problem
In the use case presented in this work, mapping the game output to the machine learning input is comparatively easy,
because the \gls{rl} model and the human players have the same task.
That allowed for this work to be implemented quickly and see first promising results.
However, finding proper levels of abstraction between the game and the \gls{rl} application in the real world requires future study.

It seems to be most promising to look at the input of the \gls{rl} task and develop a game which can generate those inputs.
Especially in micro robotics, like SwarmRL, this can be a problem, if there is more than one agent involved in a task.
This would require cooperation of every player involved in order to present a realistic policy for this multi-agent system.
