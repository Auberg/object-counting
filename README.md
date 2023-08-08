# object-counting

This repository is created to do the task of `object counting` and `object color classification`, with specific object that I choose at the moment are [`apple`]. 
This file have two files `count.ipynb` and `classify.ipynb`. Each of the notebook contain the explanation on how its being done based on the task. To use it simply run the notebook from top to bottom as each of them have been build using a wrapper for easier access.

Please find the required library in the `requirement.txt`.
* the `requirement.txt` works for both the files and also the extra exploration. 

# Other Solution

During the creation of this task I also explore the possibilities of approaching the problem using different task framework of framing it as `object counting` problem. After looking at top papers with available code for the problem I found 2 workable solution which is the following paper called `SAFEcount` [(Github link)](https://github.com/zhiyuanyou/SAFECount/tree/main) and called `CounTR` [(Github link)](https://github.com/Verg-Avesta/CounTR/tree/main), both ranking in the top 5 performer to solve the task. At first I was working with the `SAFEcount` project and try to tweak it a lot, but since it looks like there is a lot of bug to implement (especially with python  3.11), after spending about a day I decided to move on and work with the other paper. For the `CounTR` project I have tweak with it to some level to make the code works, but sadly with the time frame given I am unable to finish the whole pipeline. I have uploaded my current exploration in a different repository [here](https://github.com/Auberg/CounTR-Experiment). Feel free to take a look at the exploration I have done in the `demo.ipynb` file.