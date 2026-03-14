• 2y ago
[GreedyWorking1499](https://www.reddit.com/user/GreedyWorking1499/)
#  best 7b coding LLM? (java) 
I'm looking for a 7-13B AI model to run locally with LM Studio for Java coding, and I'm wondering what would be the top-performing option for my hardware (Nvidia GeForce RTX 2070 Super (mobile) or M2 MacBook Pro with 16GB RAM). Can anyone recommend a model and suggest which quantization I should use? 
Read more 
Share 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0id2ug/)
llama 3 8b 
[ GreedyWorking1499 ](https://www.reddit.com/user/GreedyWorking1499/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0idl1b/)
Won't a less advanced more fine tuned model perform better for coding? Or am I completely wrong in assuming that 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0inw7b/)
I mean, this thing beats Qwen1.5-32B and llama-2-70b in chat. Less advanced than llama-3 means stone age in comparison now. Just give it a week or two and someone will make a coding tune of it that'll destroy everything in its size range. 
3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0inw7b/?force-legacy-sct=1)
[ AdHominemMeansULost ](https://www.reddit.com/user/AdHominemMeansULost/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0inxpb/)
right now llama 3 8b is cutting edge 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0inxpb/?force-legacy-sct=1)
[ LocoLanguageModel ](https://www.reddit.com/user/LocoLanguageModel/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0kpxnk/)
I tested this and deepseek 33b is way better for c# code than llama-3-70b for my quick tests, but maybe im prompting llama-3 wrong. 
Edit: Yup, when I fixed the prompt format it actually just 1 shot one of my harder tests, nice, now I can keep one model loaded for all tasks lol. 
3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0kpxnk/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0idl1b/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0id2ug/?force-legacy-sct=1)
[ MustBeSomethingThere ](https://www.reddit.com/user/MustBeSomethingThere/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0ieej8/)
codeqwen-1_5-7b-chat 
[ GreedyWorking1499 ](https://www.reddit.com/user/GreedyWorking1499/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0if20c/)
I was thinking that too but, I don't remember where, I saw that CodeQwen performs significantly worse in English than it does in Chinese so all the benchmarks saying it's super awesome don't correlate to its accuracy in English. Do you know anything about that? 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0ihrcv/)
I haven’t had that problem yet 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0if20c/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0ieej8/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0io4py/)
OpenCodeInterpreter-DS-6.7B 
Q3 is already really good. 
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l669kdj/)
Comment removed by moderator
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l6bgjsb/)
You need a low temperature like 0.1 or 0.2 and a system prompt like "You are a forward thinking coding assistant. You consider special cases if needed and you preferred programming language is Java." You could also add "You always respond with full implementations." if you want to prevent lean answers. 
I haven't compared both models yet. OpenCodeInterpreter-DS-6.7B is based on an older version of Deepseek-Coder, so an improvement is easily conceivable. There are also big differences between the programming languages. 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l6bgjsb/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l669kdj/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0io4py/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0iewgn/)
Have you considered using the new LLaMa-7B model? It's specifically designed for coding tasks and works well on various hardware configurations. 
[ GreedyWorking1499 ](https://www.reddit.com/user/GreedyWorking1499/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0ifa02/)
I have tried it for just chat uses like asking what to make with some ingredients and similar boring things but nothing coding wise yet. I just assumed that a model fine tuned for code, even if less weights or less advanced would perform better. Am I wrong in assuming this? 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0iewgn/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0l9o1b/)
I've been doing some testing on the "can-ai-code" senior questions with a variety of 7B models. Here are the results sorted by performance: 
I need to do some more testing as the results vary a lot depening on the params passed and llama3 sometimes get's stuck not finishing, so it's been qutie difficult to evaluate it. I would definetely play around with wavecoder and CodeQwen1.5. Im not sure what's going on with codegemma, but it fails miserably, possibly i've messed up something.. Here is the results: 
### Deepseek-coder-33b-instruct-4.65bpw-h6-exl2:
  * **topk.json:**
    * Python: Passed 70 of 74 
    * JavaScript: Passed 67 of 74 
  * **greedy-vllm.json:**
    * Python: Passed 70 of 74 
    * JavaScript: Passed 67 of 74 


### wavecoder-ultra-6.7b-exl2_8_0:
  * **topk1:**
    * Python: Passed 69 of 74 
    * JavaScript: Passed 68 of 74 
  * **greedy:**
    * Python: Passed 49 of 74 
    * JavaScript: Passed 68 of 74 


### CodeQwen1.5-7B-Chat_exl2_8.0bpw:
  * **topk.json**
    * Python: Passed 53 of 74 
    * JavaScript: Passed 50 of 74 
  * **greedy-vllm.json**
    * Python: Passed 49 of 74 
    * JavaScript: Passed 49 of 74 


### Meta-Llama-3-8B-Instruct-8.0bpw-h8-exl2:
  * **custom.json**
```
{
    "temperature": 0.1,
    "max_new_tokens": 1024,
    "top_p": 0.75,
    "top_k": 40,
    "num_beams": 4,
    "skip_special_tokens": false,
    "stopping_strings": [""]
}
```

    * Python: Passed 42 of 74 
    * JavaScript: Passed 50 of 74 


### LoneStriker/Meta-Llama-3-70B-Instruct-2.4bpw-h6-exl2:
  * **custom.json:**
```
{
    "temperature": 0.6,
    "max_new_tokens": 1024,
    "top_p": 0.9,
    "top_k": 40,
    "num_beams": 4,
    "skip_special_tokens": false,
    "stopping_strings": [""]
}
```

    * Python: Passed 32 of 74 
    * JavaScript: Passed 67 of 74 


### codegemma-7b-it-exl2_8_0:
  * **topk1:**
    * Python: Passed 19 of 74 
    * JavaScript: Passed 51 of 74 
  * **greedy:**
    * Python: Passed 23 of 74 
    * JavaScript: Passed 34 of 74 


• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0iitoh/)
Looking for similar, tho I have 26gb usable VRAM. 
[ AdHominemMeansULost ](https://www.reddit.com/user/AdHominemMeansULost/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0io1hi/)
llama 3 8b 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0iqtc9/)
Will be doing so soon to test anyway 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0io1hi/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0iitoh/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0iu2gk/)
This leaderboard is for python but it still might be informative: [evalplus.github.io](http://evalplus.github.io)
[ GreedyWorking1499 ](https://www.reddit.com/user/GreedyWorking1499/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0iv7zc/)
I was actually looking at this exact one. I heard from someone else that Llama 3 is in fact trained on everything code llama was trained on which is why I was curious as to why the llama 3-7b was below code llama-13b which is why I posted this lol 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0iu2gk/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l0ktxqf/)
for pre llama 3 era models, codeqwen, deepseek etc. 
[ Pleasant-Cupcake-998 ](https://www.reddit.com/user/Pleasant-Cupcake-998/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l7xc06u/)
Hey [u/GreedyWorking1499](https://www.reddit.com/user/GreedyWorking1499/) Which model did you end up going with? 
[ GreedyWorking1499 ](https://www.reddit.com/user/GreedyWorking1499/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l7xe35f/)
I've been using Llama 3 instruct q6_k mostly, at least when using something local. Just recently downloaded mistroll 7b v2.2 as it was the highest <10b model on the openLLMLeaderboard and codeQwen chat (both q6_k) but haven't had the chance to use them enough to give you a proper recommendation. Honestly with my computing power I’ve been resorting to not so local LLaMA 😔 
[ Pleasant-Cupcake-998 ](https://www.reddit.com/user/Pleasant-Cupcake-998/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l7xjjth/)
How have you been evaluating the performance of the models? I am working for a client where we have some use cases involving Java code generation and since our SME for Java is OOO for a week (and also knows nothing about Gen AI), I am stuck with the task of figuring out how the models are performing, and fixing the prompts somehow. I have a bunch of models at my disposal, where I found phi3 mini 128k the worst (It was writing Python code), as we speak I am testing on Mistral 7B instruct v0.2 and I have a couple more that I am planning to test on like llama 3 8b instruct, llama 3 70b instruct, llama 3 70b chat and mistral 8x7b instruct v1) 
My approach has been asking GPT 4 to evaluate it which we can't however use for production 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l7xe35f/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1c90zkn/comment/l7xc06u/?force-legacy-sct=1)
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of April 20, 2024 ](https://www.reddit.com/posts/2024/april-20-1/global/)
  * [ Reddit  reReddit: Top posts of April 2024 ](https://www.reddit.com/posts/2024/april/global/)
  * [ Reddit  reReddit: Top posts of 2024 ](https://www.reddit.com/posts/2024/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
