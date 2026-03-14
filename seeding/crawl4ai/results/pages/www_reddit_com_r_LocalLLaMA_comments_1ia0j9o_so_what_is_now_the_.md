• 1y ago
[deleted]
#  So what is now the best local AI for coding? 
Sorry, this post was deleted by the person who originally posted it. 
Share 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m96qhkd/)
Qwen2.5-72B-Instruct holds a hair advantage over Qwen2.5-Coder-32B. 
They're roughly equivalent at codegen, but the 72B is better at following complex instructions, so is less likely to generate code for something you didn't ask. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m989g13/)
Have you tried Athene V2? It's a Qwen 2.5 72B finetune that is more specialized for coding and math 
[ Glittering_Mouse_883 ](https://www.reddit.com/user/Glittering_Mouse_883/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m9966nh/)
In my personal experience athene-v2 is much better at generating successful code in fewer iterations vs qwen 2.5. this is with C, can't speak for other languages. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m9a256v/)
I am quantizing Athene V2 now to GPTQ INT8 after reading your comment. Have you personally compared it to Qwen 2.5 32B Coder, how does it compare? 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m989g13/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m98piy0/)
What's your recommendation for us GPU poor dudes 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m9c3t02/)
How GPU poor? Qwen2.5-Coder-14B and Phi-4 (after the tokenizer fixups) which is also 14B are pretty good at codegen, for their sizes. Phi-4 is better at taking complex instructions. 
5 more replies 
5 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m9c3t02/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m98piy0/?force-legacy-sct=1) 1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m96qhkd/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m988rak/)
Do you guys just ignore the programming language when you talk about this? 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m9assde/)
Seems like they do but st the same time can it really be that much worse at C or JavaScript vs Python? 
3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m9assde/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m988rak/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m96i1p2/)
Balancing speed, ram requirements and quality qwen 32b coder is the best model you can reasonably expect to actually run locally. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m97xrdk/)
How do you think it compares to cursor with sonnet 3.5? 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m97xrdk/?force-legacy-sct=1) 1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m96i1p2/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m98r59y/)
Anyone tried the non-coder R1 distill Qwen 32B merged with Qwen 32B Coder, further finetuned by FuseAI will perform better for coding?<https://huggingface.co/FuseAI/FuseO1-DeepSeekR1-Qwen2.5-Coder-32B-Preview>
[ ForsookComparison ](https://www.reddit.com/user/ForsookComparison/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m98bjh2/)
From my personal experience: 
  * **Qwen Coder 70b** - king right now 
  * **Qwen Coder 32b** - best for most workstations 
  * **Codestral 22b** - best non-qwen model (useful if you're in a business that won't tolerate a non-friendshored model for whatever reason..) and fast inference 
  * **Llama 3.3 70b** - best at following instructions and best when the context gets large 


• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m9b3mk2/)
Thank you for teaching me "friendshored"! Great word. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m98ejxy/)
Got a link to Queen coder 70b? Never heard of that 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m98kjm8/)
Indeed, he probably meant regular Qwen 2.5 72b. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m98kjm8/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m98ejxy/?force-legacy-sct=1) 3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m98bjh2/?force-legacy-sct=1)
[deleted]
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m96khjg/)
Even the full version of R1 isn't that great at coding. I had to use Gemini Flash 2.0 Thinking to fix its mistakes. 
[deleted]
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m96l2vm/)
I've been using that too even though it gets no mentions on reddit. 
And by "coding" I mean I'm too lazy to do any real work so I just throw half assed prompts at it and hope something useful comes out. 
[ ElectronSpiderwort ](https://www.reddit.com/user/ElectronSpiderwort/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m97b1f8/)
i feel seen 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m96l2vm/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m96khjg/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m97owg6/)
These two finetunes look good on paper: <https://huggingface.co/Nexusflow/Athene-V2-Chat> <https://huggingface.co/rombodawg/Rombos-LLM-V2.5-Qwen-72b>
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m9avnyz/)
You could take a look at some of the top Coding models on my [UGI-Leaderboard](https://huggingface.co/spaces/DontPlanToEnd/UGI-Leaderboard). Other than 405b and 671b models, you're right that 72b models are currently the best non-reasoning models for coding. 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m9avnyz/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m98xvxm/)
In my experience Qwen2.5 coder 32b q8 quantisation has better coding performance than Qwen2.5 72b q4. 
Additionally it has faster tokens per second (tps). 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/mkr57xl/)
Is there any table to check which Q variant would be possible to run on my HW or what would I need to run it with 30 token/sec at least? 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m98xvxm/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m96yaor/)
I used qwen 2.5 72b, and the coder 32b, deepseek r1 70b and Claude, in my experience Claude is the best. 
[deleted]
• 1y ago
Comment deleted by user
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m97e4r5/)
Qwen2.5 72b second in my experience. In more than one time, Claude helps me out of a problem I spent hours on, while the others not. Do not trust the rank, try it in your real work. 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m97e4r5/?force-legacy-sct=1) 2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1ia0j9o/comment/m96yaor/?force-legacy-sct=1)
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of January 25, 2025 ](https://www.reddit.com/posts/2025/january-25-1/global/)
  * [ Reddit  reReddit: Top posts of January 2025 ](https://www.reddit.com/posts/2025/january/global/)
  * [ Reddit  reReddit: Top posts of 2025 ](https://www.reddit.com/posts/2025/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
