• 1y ago
[No-Conference-8133](https://www.reddit.com/user/No-Conference-8133/)
#  You're all wrong about AI coding - it's not about being 'smarter', you're just not giving them basic fucking tools 
Every day I see another post about Claude or o3 being "better at coding" and I'm fucking tired of it. You're all missing the point entirely. 
Here's the reality check you need: These AIs aren't better at coding. They've just memorized more shit. That's it. That's literally it. 
Want proof? Here's what happens EVERY SINGLE TIME: 
  1. Give Claude a problem it hasn't seen: _spends 2 hours guessing at solutions_
  2. Add ONE FUCKING PRINT STATEMENT showing the output: "Oh, now I see exactly what's wrong!" 


NO SHIT IT SEES WHAT'S WRONG. Because now it can actually see what's happening instead of playing guess-the-bug. 
Seriously, try coding without print statements or debuggers (without AI, just you). You'd be fucking useless too. We're out here expecting AI to magically divine what's wrong with code while denying them the most basic tool every developer uses. 
"But Claude is better at coding than o1!" No, it just memorized more known issues. Try giving it something novel without debug output and watch it struggle like any other model. 
I'm not talking about the error your code throws. I'm talking about LOGGING. You know, the thing every fucking developer used before AI was around? 
All these benchmarks testing AI coding are garbage because they're not testing real development. They're testing pattern matching against known issues. 
Want to actually improve AI coding? Stop jerking off to benchmarks and start focusing on integrating them with proper debugging tools. Let them see what the fuck is actually happening in the code like every human developer needs to. 
The fact thayt you specifically have to tell the LLM "add debugging" is a mistake in the first place. They should understand when to do so. 
Note: Since some of you probably need this spelled out - yes, I use AI for coding. Yes, they're useful. Yes, I use them every day. Yes, I've been doing that since the day GPT 3.5 came out. That's not the point. The point is we're measuring and comparing them wrong, and missing huge opportunities for improvement because of it. 
Edit: That’s a lot of "fucking" in this post, I didn’t even realize 
Read more 
Share 
[deleted]
• 1y ago
Comment deleted by user
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3b8757/)
My favorite prompt trailer: "Do you have any questions?" 
Every once in a while it catches something I missed, very useful 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bz3um/)
Also works really well with people. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bpwea/)
“Please restate my requirements to ensure we are aligned. Do not write code until I say so”. 
If you don’t tell it to wait, it will always eager beaver the code.. you can even tell it something like “if this was an interview you’d fail if you didn’t ask questions about this project before diving into code”. 
also somewhere in there is making sure it asks questions. I find the best way is to say something like “ask me 3 questions” but in a more specific way. The trick is to give it a count of how many to ask me. 
5 more replies 
5 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bpwea/?force-legacy-sct=1) 2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3b8757/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3az64d/)
Sorry this comment won't make much sense because it was subject to automated editing for privacy. It will be deleted eventually. 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3az64d/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3f50nq/)
> It's not AGI yet. It can't actually do the thinking for you. 
It's definitely not AGI, but I think it can do a lot of thinking for you. 
I have been coding for almost 30 years, and professionally for ~15, so I am coming at this from the perspective of someone who does know how to code, and how to manage junior developers (skilled and unskilled). 
I'd say that AI's at the moment are like highly skilled junior developers. I've trained up some young, developers with basically no real programming experience, who had a real natural flare for it. And that is what it feels like. The only difference is the AI doesn't learn from your guidance. 
I agree that they need constrained problems, context and instructions/goals. I always give every conversation with an AI the context of the project, e.g. 
"We are working on a saas application for ABC Ltd. who does XXX. They are developing product YYY, for the market ZZZ to help them AAA. 
The Tech stack is: ... 
The existing functionality is: ... 
The project structure is:| ...| -- /Types - all types are defined here| -- /Store - we manange data and states here 
We are currently working on a new feature, XYZ." 
Something like this to frame what we are doing, then specific context for the thig we are actually working on. 
While the AI is like a skilled programmer, it needs a technical architect to steer it. Whenb coding with AI, I feel a lot more like I'm wearing my archiotect hat than my programming hat. However I am doing more programming than when I worked as an architect, with a small team of human devs. 
The difference is, the AI get's through tasks much faster than human devs, and therefore needs feedback and guidance more frequently. It will smash through creating code much faster, and then innevitably run in to problems much sooner. I might give a junior dev a task, and then two days later they hit a problem. I code with AI, and within an hour, it gets to the same problem. 
I've heard some success stories from non-coders developing impressive apps using AI, where the AI has both taught them about coding, and done most of the coding for them, and in these cases, the people using AI were very logical, analytical and capable, but had no coding experience. I think AI can be an extremely powerful coding tool for non-coders, but you do need to have a certain skillset to get the most out of it. 
3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3f50nq/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3b574y/)
Yes, this is very important. I have resorted to structuring my prompts into 3 parts: 
  1. Description (give a broader context of the problem and the project) 
  2. Task 
  3. Output conditions 


Working with this + a file parser saves so much time and the output is much better than if done via “freestyle prompting”. 
That said, Claude 3.5 Sonnet solves more problems with my requests than the latest 4o, so I have to slightly disagree with op here. I mean, after all, 3.5 Sonnet scores higher in coding benchmarks and that’s noticeable when working with it. 
6 more replies 
6 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3b574y/?force-legacy-sct=1)
[deleted]
• 1y ago
Comment deleted by user
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bywaw/)
If you can map out the data, intentions, policy and so on you're 90% of the way to coding it anyway. All the LLM is doing then is saving you the chore of looking up API calls 
4 more replies 
4 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bywaw/?force-legacy-sct=1) 13 more replies 
13 more replies 
[ Altruistic-Land6620 ](https://www.reddit.com/user/Altruistic-Land6620/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3auiph/)
It's not even the users. Companies training the models and focusing on creating the tech are tunnel-visioned in to goals that are short-sighted. 
5 more replies 
5 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3auiph/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3asz43/)
This but with less fucking. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3atqbu/)
AI + some basic fucking tools= a good time 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bepue/)
a fucking good time 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3atqbu/?force-legacy-sct=1)
[ MediocreHelicopter19 ](https://www.reddit.com/user/MediocreHelicopter19/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3aukqk/)
It is a way to prove that the text is not AI written 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3auts7/)
It is a way to **fucking** prove that the **fucking** text is not **fucking** AI written* 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3auts7/?force-legacy-sct=1) 3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3aukqk/?force-legacy-sct=1)
[ Strange-History7511 ](https://www.reddit.com/user/Strange-History7511/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3atsuv/)
But he’s fucking tired of it 
5 more replies 
5 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3asz43/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bufqd/)
They haven't just memorized more. They've been trained on more and better data, been trained differently, and been structured to operate differently, which sometimes makes them more effective coders. But this isn't just about coding; it's about inference in any situation. 
If you ask it a question that can be answered from an existing document or article online, then it's easy to think that it just memorized that content and regurgitated it back to you, but that's not what is happening. If you want to better understand this, then [This video on Transformers](https://youtu.be/wjZofJX0v4M?si=dCEmvKSH-lqnmJIk) by 3Blue1Brown is excellent, but you can also gain an appreciation about the LLMs ability to be creative by asking it to create things that couldn't possibly exist in its training data. For example, ask it to write you a short story about a puppy made of spaghetti sauce who saved the world from the popsicle stick monster by making the best vanilla ice cream ever. It'll write an impressively creative and coherent story. You can do the same in code and give it something novel. This is basically the whole point of trying to achieve AGI. We're trying to create models that do more than they're trained to do. We want them to understand a novel problem space and come up with creative solutions beyond anything that's already known. 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bufqd/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bfm74/)
This post is absurd. Yes, of course give the LLM as much context and debugging feedback etc as possible. This is just not being dense. 
But to pretend that more memorization does not DIRECTLY contribute to better 1 shot attempts is ridiculous. More memorization DOES equal better code generation regardless of how much information you have given it. When adding context and information during run time you are directly lowering a models ability to retain prompt adherence. Information directly in the model weights is far more valuable. Information in weights can be thought of as “instinct” while information in context can be thought of as “logic”. Which would you rather have? An excellent human programmer with inherently better knowledge and excellent instinct? Or a programmer with lesser knowledge and instinct and slightly more information? 
If a lesser model given more information can do what a greater model can do on the first shot…..imagine what a greater model can do given the same extra information. (It’s more. And it’s better.) 
To prove that this argument is nonsense - go give a high parameter model from a year ago all of the information in the world and try to remotely reproduce the code quality results of these newer higher benching models. 
Benchmarks absolutely do not tell the whole story about how good a model is. There is absolutely no doubt about that - but a better model is a better model and not having to fight with it to get excellent code in 1 or 2 shots is worth everything. 
I don’t understand this take at all. 
3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bfm74/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3aus5t/)
Agreed. 
AI is outstanding at doing the boring stuff. And it still needs guidance; otherwise it’s going to be one hot mess if you have a medium-sized codebase. 
I couldn’t care less if the latest and greatest model does a 1-shot 4d snake in any language. 
And I think you nailed it with the one ultimate tool for coding: THE print statement. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3c1yd3/)
Seriously, never understood why the first prompt to test coding capability is to ask for it to write a snake game app 🤷‍♂️ 
3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3c1yd3/?force-legacy-sct=1) 3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3aus5t/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3b0ogb/)
Agents running swe-bench have access to tools. They probably aren't clever enough to use debuggers, but they get the unit test output: <https://www.anthropic.com/research/swe-bench-sonnet>
[ a_reply_to_a_post ](https://www.reddit.com/user/a_reply_to_a_post/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bq2uz/)
ever rely on AI that was trained on outdated docs? 
AI is not sentient yet, it doesn't maintain a mental model of your projects needs, but if you know exactly what you want from it and can provide clear instructions, it's a great tool. I like to think of things like copilot or chatGPT as a really eager intern that can look shit up on stack overflow and do simple tasks like they're on meth 
i still am in the camp that sometimes you need to try and fail a few approaches before you know what the best approach is...AI assistants might help you get an approach started faster, or come to a conclusion faster, which is valuable... 
[ Vegetable_Sun_9225 ](https://www.reddit.com/user/Vegetable_Sun_9225/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3b99nh/)
This is not actually true, and seems to be rooted in a misunderstanding of how training works and the improvements that have happened on the training side that have resulted in models that are better at providing code that solves a problem. 
You are right that a lot of people are focused on the wrong things, which is often rooted in a misunderstanding of what's happening and why and how to leverage what is possible today to solve the core business problem. 
You can absolutely prompt Claude to produce code it's never seen before, that's the whole point of GPTs and having distinct training and test sets. But the prompts are importantly and the context you provide and how that context is organized makes all the difference as to whether it produced working code or not. 
Like you mentioned debug statements are critical, which is why computer use since it means you can build up the context necessary for Claude to solve the problem well in an agent system and why someone who understands how to use tools like cline can get get a 10x productivity boost. 
I agree that a number of benchmarks aren't particularly helpful, and it's likely that a lot of training pipelines are over fitting to these benchmarks since that's what people are looking at. Kinda like when every manufacturing focused on cpu clock speed back in the 90s and early 2000s. That said there are some really good benchmarks like swe-bench that are actually worth looking at and show fantastic improvements over the last year. 
You have some good points, but it seems to me that you may not quite understand how everything works and end up glancing ran there than hitting the target with your rant. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3b1k2t/)
This is why the first thing I did was write a vscode plugin that let the LLM see execution traces and memory and let it step through code. I thought everyone did this. How else are you using this stuff? Are you debugging the LLM-generated code? Why? Fuck CoPilot, mines AutoPilot! 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3b505k/)
You may be smarter by sharing it! 
5 more replies 
5 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3b505k/?force-legacy-sct=1) 4 more replies 
4 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3b1k2t/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3b30fp/)
also, i believe that LLMs should ask for details .. most of the times i am asking it for something and it just guesses the details .. its kinda off-putting for me. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3doivq/)
So wow. That’s quite a rant. Lots of copy and pastes will get you this with the AIs website interface or use Cursor at al and you’ll quickly learn that Claude Sonnet is the best developer now, until it’s not anymore. 
[deleted]
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bere3/)
I'd like to see you try and code without a memory. This isn't the point you think it is 😭 
[deleted]
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bqm8h/)
Comment removed by moderator
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bqm8h/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3bere3/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3athvp/)
I mean, I guess. But AI is just dumb as hell sometimes. 
I think the core issue is that they're too agreeable, and try to be too helpful. Given a problem, they will fall over themselves trying to praise you for pointing it out, or will tunnel vision on fixing a bug without considering larger context. And these are all fixable things, but when you reach the point that you have to write crafted prompts with XML tags, repeat yourself over and over, look for hallucinations, give it thorough context (but not too much!), etc. it becomes a pain in the ass. 
I just spent this weekend building my own personal vscode extension to handle the above prompt strategies + automate injecting my prompts with dynamic context because it's too tedious to do manually...the ultimate irony that prompting an AI feels like too much work. So I agree that proper tooling is everything but it's not just as simple as print statements, unless the code you're writing is that simple. 
3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3athvp/?force-legacy-sct=1)
View more comments
View more comments
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3b4yy7/)
I get where you’re coming from, but these models doing better on these benchmarks is still a good thing. I agree that the LLMs need more to really succeed at coding and accomplish goals with code, but with the way things are going right now, it’s looking like a lot of the reasoning and planning will be done with an orchestration agent that will be better trained to handle and then pass these requests off to a LLM that scores high in coding benchmarks. It will probably have to do recursive analysis of outputs and nudge it more in the right direction e.g. adding comments, reminding it to log in the right file, error handling to address the very valid concerns you fucking expressed here today. 
Autogen provides a framework for an orchestration agent and gives it the ability to execute code in a docker container. Then, it feeds the console output back to the LLM. Clever bastards, the ones that came up with that. My only issue has been hitting context limits since I’m sending my requests to a single 3080, and it generates a ton of tokens. Super excited to see where it goes. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3cjym7/)
Many developers are better at coding than other developers because they have memorized more known issues and their solutions. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3f0a7q/)
This. It's called experience. 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3cjym7/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hk1lk3/comment/m3cem2t/)
This guy fucking fucks. 
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of December 22, 2024 ](https://www.reddit.com/posts/2024/december-22-1/global/)
  * [ Reddit  reReddit: Top posts of December 2024 ](https://www.reddit.com/posts/2024/december/global/)
  * [ Reddit  reReddit: Top posts of 2024 ](https://www.reddit.com/posts/2024/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
