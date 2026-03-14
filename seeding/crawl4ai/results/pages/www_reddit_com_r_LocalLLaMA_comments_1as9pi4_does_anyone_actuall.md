• 2y ago
[deleted]
#  [deleted by user] 
Share 
Sort by: 
Best
Open comment sort options
* * Controversial
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqoznzt/)
I honestly tried, but after about a week or so each time, I end up falling back to github copilot and chatgpt. It’s not the quality of the results, rather the convenience. The fastest to get up and running is llama.cpp, but that is still no where near readily available as just using copilot. 
Even autocomplete plugins are super slow and not usable by any productive standards unless you have a beefy PC. I still do revisit every once a while when something substantial comes out, but as of today, haven’t been able to find something that can beat the convenience of copilot and chatgpt 
Reply  Share 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqph1o7/)
Yeah, running them on your workstation on as needed basis is not as convenient as using copilot or chatgpt. 
Its better if you have a server pc running 24/7 which is always available. But not everyone can afford that for financial or other reasons. 
2 more replies 
2 more replies 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqph1o7/?force-legacy-sct=1)
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqraweo/)
Yeah, my best answer is keep a tab open with gpt or bars/Gemini and just alt tab and copy and paste. I tried ollama with continue and it was easy to setup, but not nearly as good as the big boys. I mean it's a difference of billions of parameters and less compute 
1 more reply 
1 more reply 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqoznzt/?force-legacy-sct=1)
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqqosp7/) • Edited 2y ago
As a professional engineer, I've yet to find a model that is actually useful. 
ChatGPT was very helpful as a syntax reference for an obscure language I had to pick up on the job. I haven't yet found an open-source model that can tell me anything useful about that same language. I've tried _many_. 
But, I don't even find copilot useful. The thing with complex software is that you subconsciously build a mental model of it as you work on it over time. That mental model is very important for writing the _right_ solution. 
A truly useful code LLM, to me, currently has too many unsolved problems in it's way. When we can get a substantial chunk of the codebase in high-quality context, and get quick high-quality responses on our local machines while doing so, local code LLMs will be a different beast. But, we could be ages away from that. 
We need either massively better hardware, a whole new architecture for these things, or the ability to truly understand how to optimize training datasets... I think all of those are things that could easily be very far away. I mean, look at the insanity of these big AI companies' compute pools. We are brute-forcing advancement through unsustainable hardware requirements and that kind of feels like a dead-end to me. 
3 more replies 
3 more replies 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqqosp7/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqoxaae/)
I tried continue on vscode. The problem was that the messages were not sent correctly to the LLM. Other than that, it had some features that copilot didn't. But I still go back to gpt-4 if I can. 
4 more replies 
4 more replies 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqoxaae/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqpc9o1/)
Codellama was made completely obsolete by deepseek. 
9 more replies 
9 more replies 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqpc9o1/?force-legacy-sct=1)
[ Disastrous_Elk_6375 ](https://www.reddit.com/user/Disastrous_Elk_6375/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqox32f/)
codellama-13b is a base model. You'd want an instruct model in order to work with instructions. The code model should work with pointer autocomplete (i.e. you start the definition and some docstrings and it should complete it) but I don't know if continue supports that. i believe tabby supports cursor completion. 
[deleted]
• 2y ago
Comment deleted by user
[ Disastrous_Elk_6375 ](https://www.reddit.com/user/Disastrous_Elk_6375/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqp9f7c/)
It's a mix of problems, not a single thing. 
First, the models themselves are obviously sub-par, definetly to gpt4, possibly even to gpt3.5, regardless of the scoreboards they aim to conquer. 
Then there's the difference between base and fine-tuned models. And between fine-tuned and chat models. And between fine-tunes by person A and person B. Much harder for people to target a variety of models. 
Also, there's more to autocomplete than just a code model. The extension does a lot of heavy lifting, provides context to the model, metrics such as where in the project you want to autocomplete and other stuff. All this can be and probably is used by copilot for suggestions. This is discussed in detail in one of the earliest attempts to create a local copilot - the repo was called fauxpilot, but it's been obsolete for a long time now. 
I've watched this space with interest, and there have been many attempts to solve this, but it's really difficult. There's not much money in this (if at all), and a lot of teams loose focus, have to work on something else to make money, or go work for someone else. Rift was really promising (they went the language server route), but that's been dormant for 4-5 months now. Continue is considered the best for chat-style stuff, and they have a lot of integrations, tabby is also recommended for completion. There was a team from israel working on an entire vscode fork + code assistant. There is certainly interest, and there are some efforts in this field, but there doesn't seem to be a clear winner at the moment. And there won't be a killer product without some top dog coming in and sponsoring a ton of engineering effort going into it. 
4 more replies 
4 more replies 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqp9f7c/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqpa87s/)
everything you said, the model will need specified 
that's the nature of open source models, and do not make the mistake of thinking you can just ignore the importance of 100% correct _prompt structure_ AND finding the _generation parameters_ that work for _that_ model for _that_ task. 
You can't bypass it. It won't work otherwise. If it does, it won't keep working. 
2 more replies 
2 more replies 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqpa87s/?force-legacy-sct=1) [ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqox32f/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqphdei/)
Yep - Tabby with 6.7B deepseek. More of a smart auto complete than big chunks of code. Pretty luck warm but its free and sometimes helpful 
Still use gpt4 for the conceptual heavy lifting on "how do I do xyz". 
Also made a powershell script that starts everything I need in one go. In this case I'm writing GCP code. 
```
#powershell -ExecutionPolicy Bypass -File .\develop.ps1

#Launch docker engine
Start-Process -FilePath "C:\Program Files\Docker\Docker\frontend\Docker Desktop.exe"

#Launch WSL, navigate to project and open vscode
wsl -e bash -c "cd ~ && cd myproject && code ."

#Wait for docker engine a bit
Start-Sleep -Seconds 15

#Launch Tabby for code completion
$dockerPath = "C:\Program Files\Docker\Docker\resources\bin\docker.exe"
$arguments = "run -it --gpus all -p 8080:8080 -v $HOME/.tabby:/data tabbyml/tabby serve --model TabbyML/DeepseekCoder-6.7B --device cuda"
Start-Process -FilePath $dockerPath -ArgumentList $arguments -NoNewWindow -PassThru

#Open Chrome to GCP
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$url = "https://console.cloud.google.com/firestore/databases?referrer=search&project=myproject"
Start-Process -FilePath $chromePath -ArgumentList $url
```

1 more reply 
1 more reply 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqphdei/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqply2e/)
I am one of the authors of [Continue](https://github.com/continuedev/continue). I use [DeepSeek Coder 33B](https://docs.together.ai/docs/inference-models) for chat (using the Together API) and [StarCoder 3B](https://continue.dev/docs/walkthroughs/tab-autocomplete) for tab autocomplete (using Ollama on my Mac). I find them to be quite useful 
As the top comment mentions, it looks like the reason you are seeing useless responses is because you are using a base model instead of an instruct model. If you can share your config.json, I could tell you if adjusting your settings also might help, though this might be easier / faster if we chat on the [Continue Discord](https://discord.gg/vapESyrFmJ)
6 more replies 
6 more replies 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqply2e/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqplkm6/)
Today I wrote a script that allows me to take a codebase and convert it into a markdown file so I can ask an LLM questions with it. 
I'm doing it to enlighten myself and learn what the optimal workflow is supposed to look like and I don't like copy and pasting. 
I have found for software design questions, non-coding models perform better than coding models, as the latter has a one track mind and that is usually the wrong track. I prefer mixtral instruct models for design. 
Still testing for the rest. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqp2v9v/)
I have a custom script to replace code blocks in vim with responses from openrouter with mixtral. Works just a bit less well than GP4 for my main use cases. 
1 more reply 
1 more reply 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqp2v9v/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqp9ss2/)
I have a dual 3090 setup and have had some luck with Phind-Codellama-34B, but I still just end up using GPT4 for code. I had hopes for CodeLlama 70B, but it seems like software is struggling with it's difficult prompting format. So I haven't really had the chance to mess with it. 
I wrote a simple Nodejs project with Miqu's help and it was passable, after a lot of back and forth. But again, GPT4 just knocked it out on the first run with cleaner code. 
1 more reply 
1 more reply 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqp9ss2/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqqitha/)
The only one that didn't suck was tabby with some deepseek 6.7b model, IIRC. I run models even with 4090. I wish I had more VRAM, interactive use does need very fast response. The models have to be small and quantized to work well. 
1 more reply 
1 more reply 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqqitha/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqp48jd/)
I pay for it one of the big ones because I forgot to cancel it. And I don’t even use it because it useless. 
1 more reply 
1 more reply 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqp48jd/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqplzx9/)
You need to use an instruct tuned model. I would also suggest looking at the llama.cpp server endpoint for Filling in the Middle instead of completion. 
Reply  Share 
1 more reply 
1 more reply 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqplzx9/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqpoxli/)
Intellij has a opensource plugin called codeGPT, in the settings you can download a number of open source models and serve them with llamacpp. It works amazingly well! It writes really good unit tests. I use deepseekcoder34b Q4 on 32 GB macbook m1-max 
Reply  Share 
3 more replies 
3 more replies 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqpoxli/?force-legacy-sct=1)
[ TopCryptographer8236 ](https://www.reddit.com/user/TopCryptographer8236/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqqafw3/)
Just wanted to give my two cent about this. Try to format your prompt into "Given X, then make me Y". For example : "Given `arr` as []int, make me a function that perform bubble sort on `arr`". It usually output better code than just letting it assume anything. Note that I'm using deepseek coder 33b for it. 
Reply  Share 
1 more reply 
1 more reply 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqqafw3/?force-legacy-sct=1)
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqp6rby/) • Edited 1y ago
Comment removed by moderator
3 more replies 
3 more replies 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqp6rby/?force-legacy-sct=1)
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqpyfym/)
Comment removed by moderator
1 more reply 
1 more reply 
[ More replies  ](https://www.reddit.com/r/LocalLLaMA/comments/1as9pi4/comment/kqpyfym/?force-legacy-sct=1)
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of February 16, 2024 ](https://www.reddit.com/posts/2024/february-16-1/global/)
  * [ Reddit  reReddit: Top posts of February 2024 ](https://www.reddit.com/posts/2024/february/global/)
  * [ Reddit  reReddit: Top posts of 2024 ](https://www.reddit.com/posts/2024/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
