[r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/)
<https://x.com/localllamasub>
Subreddit to discuss locally hostable AI 
Weekly visitors Weekly contributions 
• 2y ago
[deleted]
#  [deleted by user] 
Share 
Sort by: 
Best
Open comment sort options
* * Controversial
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kirilv2/) • Edited 2y ago
There's the [BigCode leaderboard](https://huggingface.co/spaces/bigcode/bigcode-models-leaderboard) but seems it stopped being updated in November.. looks like the are sending folks over to the [can-ai-code](https://huggingface.co/spaces/mike-ravkine/can-ai-code-results) leaderboard which I maintain 😉 
My leaderboard has two interviews: junior-v2 and senior.. If a model doesn't get at least 90% on junior it's useless for coding. senior is a much tougher test that few models can pass, but I just started working on it in December so the test itself is still under development and doesn't have nearly as many models tested. 
To see more quants, uncheck "Show Best Result" 
Reply  Share 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kirsnwe/)
Ah thank you for adding a senior, basically every model having 100% on junior wasn't giving much insight into the differences 
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kirkrgt/)
Interesting. I was under the impression that deepseek coder was still close to the top. It seems those wizard models are solid all around. If you had to pick one coding model, would you choose it based on the senior or junior ranking? 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kirm0jz/)
Consider the junior results more as a binary pass/fail then an actual ranking, if a model can't get 90% on junior it's straight up bad at writing code. 
Senior should have some performance ranking capabilities, but I haven't run very many models yet instead have been focusing on quants and understanding the degradation tradeoffs at the different GGUF and EXL2 bpws. 
With that said if you have 24GB compare some CodeLlama-34B and Deepseek-33B finetunes to see which perform best in your specific code domain.. these are two wildly different foundational models. 
If you have 12GB you'd be looking at CodeLlama-13B and SOLAR-10.7B finetunes. 
If you have only 8GB, take a good DeepSeek 6.7B like MagiCoder-DS.. it is the only small model to pass senior. 
8 more replies 
8 more replies 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kirm0jz/?force-legacy-sct=1) [ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kirkrgt/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kirt7c2/)
How can we contribute more models like this one? <https://huggingface.co/bartowski/WizardCoder-33B-V1.1-exl2>
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kiruek8/)
You can raise an issue and I will get there in a week or two, or clone [the GitHub repo](https://github.com/the-crypt-keeper/can-ai-code) and use prepare.py + interview_cuda.py (with --runtime exllamav2) + evaluate.py to run the interviews locally on your machine. 
If you run into any issues let me know and I'll improve the documentation. 
3 more replies 
3 more replies 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kiruek8/?force-legacy-sct=1) [ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kirt7c2/?force-legacy-sct=1)
[ Ape_Togetha_Strong ](https://www.reddit.com/user/Ape_Togetha_Strong/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kitcsmk/)
Do people really only care about Python and Javascript benchmarks for LLMs? I'd like a model that doesn't fuck up ownership and try to use traits that a type doesn't implement every other line in Rust. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kitg3v9/)
Well I certainly care because these are the two languages I use, I am a simple plumber and don't do systems programming. 
Happy to collaborate on a Rust evaluator perhaps for senior interview especially, raise an issue on GH if you'd like. The big task is implementing treesitter to replace my homebrewed (and thus language specific) function entrypoint finder, if we can cross that moat then support for basically any language just means a runtime wrapper and a docker container. 
1 more reply 
1 more reply 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kitg3v9/?force-legacy-sct=1) [ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kitcsmk/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kiws3v2/)
Yes, your leaderboard is very good. Thanks for listing all my 4 models. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/l5ddovi/)
How can I see when one of these tables has been updated? Can't find it. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/l7ywuy9/)
Any reason why Gemini isn't on your leaderboard? 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/l7yxhb4/)
I'm Canadian and historically Google's AI offerings have been unavailable in my country. I haven't gone back to check if the restrictions have been lifted.. feel free to raise an issue on the GH, or even better if you already have access use interview-litellm to run the tests and submit a PR with results! 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/l7ywuy9/?force-legacy-sct=1)
[deleted]
• 2y ago
Comment deleted by user
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/l71djmb/) • Edited 2y ago
I update regularly if you look at the GitHub, but focus on open-source models I don't need to pay to evaluate (I am a hobbyist without finding), I spend enough on cloud GPU for the big guys already. 
OpenAI could use a revisit and addition of Omni, sure, but all openai models are tagged with their versions so not sure what you're trying to say there? If you raise an issue on GitHub we can work on refreshing them but it's not really a priority for the project. 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kirilv2/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kis1z9b/)
I found the [EvalPlus Leaderboard](https://evalplus.github.io/leaderboard.html) to be a good resource for code LLMs. 
[ Top_Statistician_615 ](https://www.reddit.com/user/Top_Statistician_615/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kvpie6c/)
Is this still being updated? 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kyfe0wb/)
Yes, there are the March Claude models for example. 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kvpie6c/?force-legacy-sct=1) [ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kis1z9b/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kwnnrov/)
i have 96GB DDR5 Ram, which model is the best out there. I want to use open interpreter with it, so i can have it write the file structure for the code in the folder. using the prompts from GPT pilot for the logic, can anyone else sort this out? 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kxo3rdk/)
doesn't it depend on VRAM mostly ? 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/kwnnrov/?force-legacy-sct=1)
[ jtgsystemswebdesign ](https://www.reddit.com/user/jtgsystemswebdesign/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/19bgnfc/comment/l3jqg8z/)
anyone find any model shine better than the others for aesthetically looking code, example ask it to do a login ui in bootstrap and watch the hot pile of garbage you get lol - I have found codelamma 70b to be the better looking designs of the pile so far but I'm just getting into testing each one, but id like something to really knock it out of the park. 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of January 20, 2024 ](https://www.reddit.com/posts/2024/january-20-1/global/)
  * [ Reddit  reReddit: Top posts of January 2024 ](https://www.reddit.com/posts/2024/january/global/)
  * [ Reddit  reReddit: Top posts of 2024 ](https://www.reddit.com/posts/2024/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
