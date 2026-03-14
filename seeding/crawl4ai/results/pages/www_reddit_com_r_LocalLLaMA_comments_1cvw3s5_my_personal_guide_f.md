• 2y ago
[SomeOddCodeGuy](https://www.reddit.com/user/SomeOddCodeGuy/)
#  My personal guide for developing software with AI assistance 
Sorry, this post was removed by Reddit’s filters. 
Share 
• [ Promoted ](https://www.reddit.com/user/iGPT_ai/)
Every week you spend on parsing, chunking, and reranking is a week you're not shipping. iGPT handles context engineering. You handle product.
Learn More
igpt.ai 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4ryzj6/)
[u/someoddcodeguy](https://www.reddit.com/user/someoddcodeguy/) gave me this workflow and I tried it out. I have to say that I like it a lot. I actually think this is a great way to do your own "pair programming". Plus you get to QA your code as you go. 
You also get the benefit of an extra AI looking at the code and verifying what the first model gave you. 
Also, it looks like a lot to do, but it really isn't. It's pretty fast once you get the hang of it a couple of times. 
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4s0gj5/)
Comment removed by moderator
7 more replies 
7 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4s0gj5/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4ryzj6/?force-legacy-sct=1)
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4s77op/)
And watch out for strange imports. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4vfo6j/)
Indeed, AI often hallucinates imports, or it mixes versions. So one import is from an older version and another import is from the most recent version. 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4s77op/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4s8f8r/)
Check out <https://aider.chat>, I think it fits really well with your mindset you outlined here. This will just cut down on the mechanical aspects of copy-pasting code, allowing you to iterate faster. 
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4s8txb/)
Comment removed by moderator
5 more replies 
5 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4s8txb/?force-legacy-sct=1) 1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4s8f8r/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4smdla/)
> When asking the LLM to review code, do it in a new chat and tell it ANOTHER AI wrote the code. Not you, not it, but a separate AI. 
I wonder how the training data looks like so that makes such a difference. 
And does it make a difference compared to just writing "analyze the following code" without mentioning where it comes from? 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4smdla/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4ugddz/)
Something that helped me with AI generated code was asking it to produce unit tests for the functions generated, using a unit test framework. This makes the AI 'think' more about uses cases and parameters. It also makes testing each function/class easier as you can paste back the failing test results and it can readily identify them from its context. The steps from here to a semi automated agent based work flow are getting clearer every day. Another coding project for an AI perhaps..... 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4ukvae/)
That pretty much mirrors my own approach, it really works best when you know exactly what needs to be done and how but can't be arsed to actually write it so you can work around the shortcomings by actively helping it with hints and tips on how to proceed. Doubly so when it involves established algorithms that they've seen 100 billion times in the training data and can tailor them perfectly for your use case, while you know what they're a good fit for but have forgotten how to implement them by hand since college/interview and would need a refresher. 
They may be meh at architecture, but can still help in forming it by listing all the options that you might be forgetting about or haven't yet considered. The old GPT-4 saved me so much time on a few occasions by just listing some libraries that fit my use case perfectly which I'd never heard about. 
> I always use 2 AI. Always. 
Honestly, I just throw the problem into _all_ of the flagship models that are available for free from every company if it's not immediately solved by the first one you tried. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4srq89/)
Thanks for sharing! Super helpful 
[ ai_did_my_homework ](https://www.reddit.com/user/ai_did_my_homework/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/llnv60d/)
Really good, you could sell this as a course lol 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4s83hx/)
What models do you use and have the most success with? I only find it useful for creating starting points for a feature. Describe the feature and iterate with small task on top until all falls apart. That is when I fully take over. With larger code calling other code it becomes mostly useless beside fill in the middle to generate some boilerplate code. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4u2dmk/)
I find that functional programming practices (especially pure functions) work well with these models since FP inherently keeps context limited 
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4s9jvf/)
Comment removed by moderator
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4s9jvf/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4s83hx/?force-legacy-sct=1)
[u/adobe_acrobatdc](https://www.reddit.com/user/adobe_acrobatdc/) • [ Promoted ](https://www.reddit.com/user/adobe_acrobatdc/)
Organise, ideate, and share insights with PDF Spaces.
Learn More
adobe.com 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4s2arv/)
That's a great guide with some interesting ideas. I like "tell the AI another AI wrote it", so simple! Can't wait to try it out. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4vj6rx/)
Thanks, it is help for me. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4yyh5f/)
Would be nice to have this workflow setup in an IDE 
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4z6lnj/)
Comment removed by moderator
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4z6lnj/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4yyh5f/?force-legacy-sct=1)
[ olddoglearnsnewtrick ](https://www.reddit.com/user/olddoglearnsnewtrick/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l5byhlq/)
My personal experience (ChatGPT-4 paid) is that often times it helps me jotting down simple mainstream code (I mostly code python) but for the overall flow it often sucks and sucks badly when you go into lesser common environments (e.g. SvelteKit) and unlike someone below said I am not inclined to grumble or disparage this technology. As a matter of fact I'd love it could make me even more productive since I'm a freelance paid by results, not time. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/lc8j03f/)
Do you use any copilots like [double.bot](https://double.bot)? 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/lc8j03f/?force-legacy-sct=1)
[ here_for_the_boos ](https://www.reddit.com/user/here_for_the_boos/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/llt9lx6/)
I love this. Any updates or changes in the past 3 months since you originally wrote it? 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/llt9lx6/?force-legacy-sct=1)
[ Comprehensive_Law552 ](https://www.reddit.com/user/Comprehensive_Law552/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/m02i0z1/)
  1. Are you using DEVIN? 
  2. If you are, how do you use it? 
  3. If not, are you using any of the paid ai coding assistants? 


1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/m02i0z1/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/m2xeo2w/)
I LOVE this. I am NOT a coder. I am a photographer who needs a local LLM and have been struggling to set it up. I am however a thinker, and planner and was looking for an addition to how I have been brainstorming HOW to get my amd gpu to be recognised in either Win 11 or Ubunutu. I even went as far as installing Linux on a separate drive to have a couple of boot images... no luck. The issue is apparently is the kernel... and I found out the hard way, simply installing python, VSCode, and all the updated drivers to recognise my gpu, does NOT guarantee success. I've been at the cutting edge of tech since Photoshop came out as V1 back in like '92 and so have got used to which OS, which Program, and which peripherals? 
So today with all the AI nonsense (read fun), I thought perhaps I could flush out the idea by doing exactly what you've been doing. 
I've been brainstorming with GPT4.0, revising, commenting and then pasting it back into the chat as if it was new info. Even if I don't agree with what comes back, it often jogs my mind to an original thought about something I wanted to investigate. 
So, now I'm using chatgpt, gemini and google AI studio with VSCode thrown in for good measure just to see how much horse manure is being thrown back at me. 
My goal is to create a stand alone app which can 'sniff' your system and then based on the user being like me - wants to find the right version of all the backend apps to recognise their amd gpu. I am SURE there are at least thousands of people who don't want to throw money at Nvidia, and just like amd... I want this app to be something that makes their life easier when they too have the insane idea of running a local LLM to create something that works specifically for them in their world and profession. 
Thoughts? Comments? Findings? Suggestions? 
I found your situation meaningful, given you work with people whose time you do NOT want to waste, including your own. Plus, wow it's fun to have your thoughts thrown back at you with some version of insight. lol 
anyway - thank you for your post - hope you see mine and have the time to comment. cheers. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/m2xeo2w/?force-legacy-sct=1)
[ blasterbrewmaster ](https://www.reddit.com/user/blasterbrewmaster/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/mjocvre/)
Have you thought about automating steps 2-4? Have a script that does the following: 
  * take in the requirements and fits into a standard prompt 
  * feeds the prompt to the AI and waits for the response 
  * Logs the response 
  * Takes the code from the AI response and feeds it into another AI fit into the standard prompt 
  * Logs the response 
  * Spits out the code 


I could see this speeding up the workflow even more, to where if you had the requirements in a file you could set it up to feed in a bunch of files and have it produce all the code for each requirement and leave you to review each of them and see which ones may need to be thrown back in for another cycle, which you could make a modified version of the script for that. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4v9yfn/)
Personally, the biggest thing for me improving my coding workflow with LLMs has been to start with working tests and keep a very small change set while working on a project, then when something breaks you can use just dump git diff into the context. 
Also, lots of small, strongly typed functions is the way to go. Get the LLM to write the function and the test in one go, which is pretty doable when they're small. 
Finally, I've had decent success with iteratively asking the LLM to update a given piece of code with new features before finally doing a rewrite. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/l4zvm6l/)
I work similarly. You can use Jan and switch local-ai/api mid conversation, so you dont have to copy paste. Although you cant change the role from assistant to user from the code ao it might double down 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/mgal132/)
Hey man, 
came across your post while researching best practices to augment my work flow. 
I'm a Technical PM (code literate, not code savvy) and have a very similar process. 
i think of it as an Agency model, you lay out your req. - consult the AI as an expert to chart architecture, edge cases, and overlooked issues. have it high level design 
then ask the AI as a dev manager to break the features into rather detailed work plans. 
then have the AI as a junior dev execute the plan, while reviewing everything along the way 
[ Emotional-Match-7190 ](https://www.reddit.com/user/Emotional-Match-7190/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1cvw3s5/comment/mmamjn1/)
Thanks again for sharing your insights! This is super helpful 
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of May 19, 2024 ](https://www.reddit.com/posts/2024/may-19-1/global/)
  * [ Reddit  reReddit: Top posts of May 2024 ](https://www.reddit.com/posts/2024/may/global/)
  * [ Reddit  reReddit: Top posts of 2024 ](https://www.reddit.com/posts/2024/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
