• 2y ago
#  Is $2-3000 enough to build a local coding AI system? 
Id like to replicate the speed and accuracy of the coding helpers like cursor / anthropic, etc. 
What can i build with $2000 - $3000? 
would a mac studio be enough? 
Im looking for speed over accuracy...i think accuracy can be fined tuned by better prompting or retries 
Read more 
Share 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljwqpi9/)
I'm on a used $300 MacBook Pro cerca 2018 with 32GB of RAM. I run vscode with the "context" plugin. I tried the deepseek 2 api big boy version and frankly wasn't that impressed especially when you account for just how much I'm using it. 
So now I have ollama serving up deepseek-coder-v2-lite-instruct with 32k context enabled "num_ctx = -1", "num_predict = -2". There's also nomic-embed which is recommended by the people that make the plugin. 
My computer seems to have developed psychic powers as to what I'm about to do next. 
Honestly I've never been happier as a programmer. 
My point is, before going big and splurging, try a cheaper setup and then upgrade only if you have some good reason to. Otherwise you're always going to be disappointed. 
Also deepseek-coder-v2-lite-instruct with 32k context works great as a chat assistant in my other programs like open web-ui. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljyc0by/)
I do the same use Ollama and acually switch the smaller ones out. Llama, deepseek, claude, etc. I just used the smaller ones. I even feed it my own code base in the context. Works quite good actually it even provided me some improvements in my codebase. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljz1ujv/)
I'll switch back and forth when I think there's some specific skill I need. Like for legal writing Phi 3.5 can't be beat. But these days I'm mostly good with deepseek-coder-v2-lite-instruct and only switch if it's given an unsatisfactory result as opposed to trying to predict what model is best suited for the task. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljz1ujv/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljyc0by/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljwqpi9/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljyt497/)
As someone with a 2x3090 system, I use Claude for programming because it makes less errors, better understands requirements, is super fast and has higher context. If you only want to build it for programming I recommend you hold off at least a year. Nvidia will release their new AI hardware and the current Gen will flood the market. 
I still use my 2x 3090 system for messing with image generation and playing with uncensored LLMs, but I can't recommend it or any machine for your price point for serious programming. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljz3nbs/)
Which models for image gen and what interface? What uncensored models do you suggest, and how are you using them (rp, questions, erotica, etc)? 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljz3nbs/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljyt497/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljvk13b/)
If you wait until M4 max and ultra is introduced, you can get m3 max with 128gb or m2 ultra with 192gb for about $3k range. They will lose value once the m4 is released and I'm sure those machines will be mostly AI focused, lowering the value of m2 ultra and max3 substantially 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljvslfv/)
yeah im holding off to see what apple is going to release next. my savings will grow as well by that time 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljvk13b/?force-legacy-sct=1)
[ Pleasant-PolarBear ](https://www.reddit.com/user/Pleasant-PolarBear/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljwc834/)
People have been able to run 70b models on a single 3090 but it's highly impractical. If you're looking to even approach the performance of claude 3.5 sonnet (which is the best model for coding imo) you're out of luck, even llama 405 doesn't compete. I'd hold off on making any investments considering how companies are focusing much more on improving the efficiency of models and how much hardware optimized for running transformers will be released in the coming years. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljv8ge6/)
For autocomplete you just needs a small model. Even running locally on your coding machine might be a good enough option. Did you try anything out already? 
For the heavy lifting you need a lot of fast RAM, or better yet VRAM (GPU). How much? Depends on what models you want to run, and in turn what kind of assistance from the system you want. Project size, languages, etc. 
I'd suggest to give [continue.dev](http://continue.dev) a try with their recommended models : <https://docs.continue.dev/setup/select-model>
Run it locally as much as you can. After that extend to running on some kind of hosted service like [runpod.io](http://runpod.io) with a quick ollama installation. See what models you like, what amount of resources you need, etc. 
Only then, when you know what you actually want/need, it makes sense to build a system. Of course if you prefer to play around with other aspects you could just jump right in and build something anyway – but it might turn out to be a big waste of money if you go into the wrong direction. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljv8ge6/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljwcsq0/)
First off, as a software dev of 30 years, what makes you believe, that LLM can code? I yet have to see anything that surpasses trainee level "coding" personally, but I might be wrong here. Errror rate of 33% of the best models make this impossible, today. just my personal observation, your mileage might vary. 
I found that people with less experience in coding find code generation more helpful - but is it really? Does it not generate nonsense for beginners? I do not believe so. 
I can spend days debugging LLM generated code, and then end up writing it from scratch myself in 20 minutes, just because you get nowhere with this slick looking generated nonsense. 
Second, local vs service, production vs testing, you seem to be somewhere in between all of that. Before spending $3000 on hardware today, just to find out, that you cannot run any of your environment on anything less than $4000 hardware, I'd highly recommend you to run this on hosted services first, until you figure out, what you need. 
Just my 5 cents 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljxdl51/)
I am a software developer, and I use ChatGPT to help with coding. 
If I ask it to write me a full feature, it is usually not the best. 
But what I do, is that I know how I want to structure my code and exactly what functions I want, so I just ask it to write me an individual function that does a specific thing. 
It does that very quickly and effectively in my experience. 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljxdl51/?force-legacy-sct=1)
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljxrrtl/)
It sounds like the last time you coded with an LLM was 2023. 
25 years exp here and I effectively and quickly use LLMs every day. I use them as a second set of eyes on code reviews, to reword and improve requirements, to setup and write unit tests, and to generate code. I've even written an entire application with Claude Sonnet 3.5. I now use the application every week to speed up my other work. 
These great tools won't replace humans but they sure have helped my productivity. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljxrrtl/?force-legacy-sct=1)
[deleted]
• 2y ago
Comment deleted by user
2 more replies 
2 more replies 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljxo0xq/)
I'd wager with 99.999999% certainty that Andrej Karpathy is a better coder than you (and I know for certain myself) and he says most of his coding nowadays is in English with Claude Sonnet, so... 
<https://x.com/karpathy/status/1827143768459637073>
4 more replies 
4 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljxo0xq/?force-legacy-sct=1) 3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljwcsq0/?force-legacy-sct=1)
[ Grouchy-Friend4235 ](https://www.reddit.com/user/Grouchy-Friend4235/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljxfi7a/)
No. 50k+ 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljxfi7a/?force-legacy-sct=1)
[ ThenExtension9196 ](https://www.reddit.com/user/ThenExtension9196/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljvhkrt/)
No you’ll need at least a 70b model which will need 48g minimum. Dual 4090 is barely enough. You’ll want 2xRTX6000ADA at 8k a peice for 96g vram for a solid system. I’m building one now to do my work for me securely. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljx0pan/)
Did I miss something? Why does he NEED a 70b model? Whats gonna stop him from running codestral 22b? Or once the gguf drops, codestral 7b? 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljx0pan/?force-legacy-sct=1) 14 more replies 
14 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljvhkrt/?force-legacy-sct=1)
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljv1lug/)
Comment removed by moderator
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljv90tb/)
Too bad there is nothing between the 16B and 236B version for Deepseek Coder V2. Getting a machine that can run it probably won't pay off in comparison to just running any of the available services. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljvf56r/)
The cheapest way is to simply use deepseek api. State of the art coding model very, very cheap. Much cheaper than chatgpt4, has larger context, and in my tests, with c++, c, Python, it is better 
5 more replies 
5 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljvf56r/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljviefe/)
There’s the 70B llama 3.1. I don’t have experience with deepseek but llama is seemingly performing well on benchmarks so seems like a reasonable stand in 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljv90tb/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljvhf6j/)
Quoting from a previous post: 
> (DeepSeek Coder V2 236B) GGUF Q4_K_M quant with ktransformers runs on 24GB of VRAM + 130GB of RAM at 13.6 tokens/s by optimizing MoE data placement between RAM and VRAM <https://github.com/kvcache-ai/KTransformers>
Grab a used $600 RTX 3090 and $400 of 4x48GB DDR5 RAM on Ebay (or half the cost for DDR4, but slower inference) and $300 of other PC components. You should be good to go. 13-14 tokens/s is too slow? Buying a second 3090 should do the trick. 
But before buying anything, try DeepSeek Coder V2 Instruct (free on their website), and try to get a copy of your build on Runpod and run what experiment you plan to run on your future build. Please don't buy without proper research and testing. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljw75zz/)
how are you getting the 3090 for 600? 
6 more replies 
6 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljw75zz/?force-legacy-sct=1)
[ TopCryptographer8236 ](https://www.reddit.com/user/TopCryptographer8236/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljye84g/)
Check the issues, apparently they use server CPU which has 8 channels of RAM instead the standard consumer CPU which usually has 2. You can still use it though but it will just be 4~5T/s. Ref : <https://github.com/kvcache-ai/ktransformers/issues/21#issuecomment-2270644392>
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljye84g/?force-legacy-sct=1) 3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljvhf6j/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljw3p9k/)
None of those come close to matching either Claude or ChatGPT for real world coding. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljw3p9k/?force-legacy-sct=1) 7 more replies 
7 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1f0xg89/comment/ljv1lug/?force-legacy-sct=1)
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of August 25, 2024 ](https://www.reddit.com/posts/2024/august-25-1/global/)
  * [ Reddit  reReddit: Top posts of August 2024 ](https://www.reddit.com/posts/2024/august/global/)
  * [ Reddit  reReddit: Top posts of 2024 ](https://www.reddit.com/posts/2024/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
