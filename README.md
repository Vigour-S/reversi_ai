# reversi_ai
This is a project implementing a reversi agent as an opponent

This is a website where players can play reversi with AI online.
This website was implenmented with Javascript and django. Although it can be built with pure Javascript as a client side program, I put all computations in the cloud.
Because it requires a vast number of computations and Python is more efficient to deal with these computations.

The core algorithm of predicting the next move is [minimax](https://en.wikipedia.org/wiki/Minimax) and [alpha-beta algorithm](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning).

This site was deployed on http://sample-env.zesvu2ttmu.us-west-1.elasticbeanstalk.com/homepage.
