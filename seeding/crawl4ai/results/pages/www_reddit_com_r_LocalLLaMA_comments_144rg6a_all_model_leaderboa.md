• 3y ago
#  All Model Leaderboards (that I know) 
Sorry, this post was removed by Reddit’s filters. 
Share 
• [ Promoted ](https://www.reddit.com/user/google/)
Download Chrome to safely store your passwords and sign in with a simple click.
Download
google.com 
[ Ok_Neighborhood_1203 ](https://www.reddit.com/user/Ok_Neighborhood_1203/)
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnhcoiu/)
There's also : 
<https://github.com/my-other-github-account/llm-humaneval-benchmarks>
GPT-3.5 and GPT-4's specifically optimized for humaneval, their paper mentions contamination, and they got a lower result than this repo. So, I'd take their much higher performance with a grain of salt. They are still better than the open source models, but perhaps not by such a wide margin. 
That also calls into question the rest of the results, and by extension can-ai-code since it was run by the same person. But until I go over the code and reproduce it, I'll reserve judgment and assume only the GPT-3.5 and GPT-4 results are skewed. 
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnh8kp9/)
I'd really like more specific Leader boards in the future. 
Leader boards that score just on things like , , coding, or other tasks. I feel that the future is more likely to be multiple small to mid-size specialized LLMs rather than Larger, more generalized LMMs. 
Yours is nice because if focuses just on Logic problems. 
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/k1mh9oo/)
<https://chat.lmsys.org/> probably has the data to compute that. Take the prompts that people are submitting for ELO arena and have a GPT model categorize them and then calculate ELOs for each category. 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnh8kp9/?force-legacy-sct=1)
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jni4uue/)
Three I have that are missing from the list: 
  * Chain-of-Thought Hub <https://github.com/FranxYao/chain-of-thought-hub> - these are mostly gathered although Yao Fu, the author is working on specific CoT runs 
  * C-Eval <https://cevalbenchmark.com/static/leaderboard.html> - Chinese eval, found this w/ InternLM announcement (interesting that GPT-4 is still #1 here) 
  * <https://bellard.org/ts_server/> - older, but Fabrice Bellard tested basically all the open models available from the beginning of the year w/ lm-eval on his TextSynth API server 


While not quite a leaderboard, [u/catid](https://www.reddit.com/user/catid/) did some interesting evals a while back for programming, here: <https://docs.google.com/spreadsheets/d/1TYBNr_UPJ7wCzJThuk5ysje7K1x-_62JhBeXDbmrjA8/edit#gid=0> and <https://github.com/catid/supercharger/tree/main/airate>
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnirywg/)
Great resource! 
[Here's](https://github.com/underlines/awesome-marketing-datascience/blob/master/llm-tools.md#benchmarking) my take on it 
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnju428/)
My LLM vs. Jeopardy leaderboard is : 
<https://github.com/aigoopy/llm-jeopardy>
Updated after every airing and new models added as GGML becomes available. 
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnibpuq/)
Man, Falcon’s been on top for a hot minute now. Anybody know if there’s a ggml based 4bit version? I’m super happy with the uncensored CoT Storytelling model, but I’m just curious how much better things could be. 
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnis91e/)
it's not trivial to quantise falcon because you can't just use quantisation code built for llama models. 
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnisj7r/)
Oh wow! Thank you so much for explaining that to me. I’m good at some things, but in the realm of the finer more technical points of ML architecture, I am a village idiot. 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnis91e/?force-legacy-sct=1)
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnk0qye/)
Note, Falcon _may_ be on the top of HF's list because MMLU is not being run properly: <https://twitter.com/Francis_YAO_/status/1666833311279517696>
If you read that thread, you'll see that the rankings really change depending on the benchmark. They're very close. I think the big differentiator is going to be 1) licensing (Falcon is Apache 2.0, but OpenLLaMA basically matches LLaMA and is also Apache 2.0 license) 2) hardware support - falcon-40b is a bit of an odd size - it won't fit onto 24GB consumer cards, while llama-33b does and 3) software support - right now, Falcon runs terribly and has almost no tooling, while the community has really gotten to understand llama models. 
One thing worth noting, Falcon uses MQA, which makes for [much more efficient kvcache size](https://huggingface.co/blog/falcon) for longer context lengths, so it might make it worthwhile, but there are so many other architectural improvements coming down the pipeline that I guess we'll see how quickly tooling gets built before the next hot new thing comes. 
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnk16bl/)
Yeah, it’s crazy. Once Modular releases their full suite of toys, things are going to get even better even faster. It’s absolutely insane and it frequently breaks my brain. 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnk0qye/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnibpuq/?force-legacy-sct=1)
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnulaa1/)
I'm a little upset that there are only like two benchmarks that compare Airoboros and Nous Hermes. These seem like the best overall outside in most benchmarks. 
EDIT - I finished up my (very informal) personal testing. I can confidently say I like nous hermes more, it was a much better all-rounder and made fewer mistakes. 
[ letsgetretrdedinhere ](https://www.reddit.com/user/letsgetretrdedinhere/)
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnhih9v/)
<https://crfm.stanford.edu/helm/latest/?group=core_scenarios>
[ letsgetretrdedinhere ](https://www.reddit.com/user/letsgetretrdedinhere/)
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnhiw5m/)
This used to be good but now it's missing LLaMA, Falcon, GPT4 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jnhih9v/?force-legacy-sct=1)
• [ 3y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/jou7a2g/)
<https://gpt4all.io/index.html>
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/144rg6a/comment/mbxaj3d/)
<https://oobabooga.github.io/benchmark.html> shows which ones are best for different hardware capabilities 
[Note to self: This is the "Pareto frontier" one that you keep thinking of but can never find.] 
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of June 9, 2023 ](https://www.reddit.com/posts/2023/june-9-1/global/)
  * [ Reddit  reReddit: Top posts of June 2023 ](https://www.reddit.com/posts/2023/june/global/)
  * [ Reddit  reReddit: Top posts of 2023 ](https://www.reddit.com/posts/2023/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
