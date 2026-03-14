• 1y ago
#  DeepSeek v3 vs. Claude 3.5 Sonnet 1022: DeepSeek tends to write simpler code (My Experience) 
Hey everyone, I've been experimenting with using LLMs to add new features to my code, and I've noticed some interesting differences between DeepSeek v3 and Claude 3.5 Sonnet. Specifically, DeepSeek tends to generate simpler, more straightforward code compared to Claude, which often leans towards more complex, object-oriented solutions. 
I wanted to share a couple of examples and get your thoughts. 
**Example 1: Implementing an Undo Feature for File Changes**
When I asked both models to implement an undo feature for file operations, they took very different approaches. Here's a summary of what I observed, based on Claude's own analysis of DeepSeek's code: 
**Key Differences:**
  * **Complexity:** Claude opted for an object-oriented design with a dedicated manager class to handle undo logic. This approach promotes better organization and separation of concerns, potentially making it easier to scale for more complex scenarios. DeepSeek, on the other hand, used a simpler, procedural method with a global list to track changes. This is easier to understand at a glance, especially for basic undo/redo. 
  * **Data Structures:** Claude tracked changes using a list of objects, each containing detailed information about the operation (type, path, timestamp, content). DeepSeek used a list of tuples, holding just the essential data (action, path, backup). Both are functional, but DeepSeek's approach is less verbose. 
  * **Error Handling:** Claude included more robust error handling, providing feedback to the user in case of issues. DeepSeek's error handling was more basic, primarily focusing on file deletion during undo. 
  * **Readability:** For those familiar with object-oriented programming, Claude's code is well-structured and easier to maintain in larger projects. DeepSeek's linear code is arguably easier to follow for those less comfortable with OOP concepts. 


**Deep Diving into the Differences**
The differences go even deeper than just complexity. Here are some additional observations about their respective approaches: 
**DeepSeek's Approach - Simplicity and Directness:**
  * **Fewer moving parts:** It avoids introducing new classes and enums, relying on basic Python data structures and control flow. 
  * **Directness:** The logic for backing up and undoing is embedded directly within the functions that modify files. 
  * **Less abstraction:** There's less indirection, making it easier to see the direct relationship between the action and the undo operation. 
  * **Pragmatic Approach:** DeepSeek appears to focus on providing a functional solution with minimal overhead, prioritizing simplicity and ease of understanding. 


**Claude's Approach - Robustness and Extensibility:**
  * **Focus on Structure:** Claude seems to prioritize building a more robust and well-structured solution, anticipating potential future complexities. The use of classes and enums is characteristic of this approach. 
  * **Detailed Documentation:** Claude includes more detailed comments and docstrings, explaining the purpose of the classes and methods. 
  * **Experience Assumption:** Claude's response might assume a user with more software engineering experience who appreciates structured design patterns. 
  * **Communication Style:** It's more conversational, asking for confirmation (e.g., "Would you like me to explain..."). 


Interestingly, when I asked Claude to compare the two implementations, it acknowledged the simplicity and effectiveness of DeepSeek's code: 
> "Yes, that's a good implementation! Your approach is actually simpler and more straightforward than my suggestion while still accomplishing the core functionality... One small improvement you might consider is removing the entry from `file_history` if the undo operation fails..." 
**Example 2: Adding a Message Override Feature**
I saw a similar pattern when adding a message override feature. Again, Claude praised DeepSeek's implementation as "clearer and more straightforward," highlighting its advantages: 
> "Yes, that's correct! This implementation is actually clearer and more straightforward than my previous suggestion. Your version has several advantages: 1. It keeps the message collection logic together in one place. 2. It makes it very clear when the default message is being used vs. the user message..." 
**Which Approach is "Better"?**
Both implementations achieve the desired functionality. The "better" approach depends on the context and your priorities: 
  * **Choose Claude's approach if:**
    * You anticipate needing more complex undo scenarios in the future. 
    * You value a well-structured and maintainable codebase. 
    * You are comfortable with object-oriented programming. 
  * **Choose DeepSeek's approach if:**
    * You need a simple and quick solution. 
    * You prioritize ease of understanding and implementation. 
    * Your requirements are unlikely to change too much. 


**My Takeaway:**
My experience suggests that DeepSeek Coder might be a better choice when you need a quick, clean implementation of a new feature. Claude, while capable of generating more sophisticated code, sometimes leans towards over-engineered solutions unless you provide very specific instructions. It also seems like DeepSeek might be more suitable for users that are less experienced, whereas Claude might target more experienced programmers. 
**What are your thoughts?** Have you noticed similar differences between these or other LLMs? Do you prefer simpler or more complex solutions when using LLMs for coding? I'd love to hear about your experiences and any tips you might have! 
Read more 
Share 
• [ Promoted ](https://www.reddit.com/user/google/)
Access your Chrome tabs on all your devices. Get Chrome for your computer.
Download
google.com 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m501e7k/)
This whole post is ai written 😩 
[ EstarriolOfTheEast ](https://www.reddit.com/user/EstarriolOfTheEast/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50nf0e/)
Oddly, I agree with gptzero--looks 5% human, 95% claude sonnet to me. With the directions and topics fully provided by human. I don't mind this type of production, as long as the human component can fully stand by everything written. But it will probably get annoying in the future, if most people end up basically writing/structuring their writing the same way and using the same turns of phrases. 
The real problem is those who post things from LLMs without being able to verify correctness (spreading misinformation to both humans and future LLMs) or use it for something anyone else could have easily done. This analysis is unique enough. 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50nf0e/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50dc7o/)
Whenever I see “Robustness” in someone’s text I can’t help but think it as ai generated lmao 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m51ggzu/)
Damn, I use that word a lot : ( 
3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m51ggzu/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m51778l/)
For me it's the bullet points with well defined sections. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m51778l/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50dc7o/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50p52o/)
they probably just rambled to an AI about their opinions on  and  then had it organize their thoughts which is totally fine 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/mfzbhrz/)
yeah this is how it reads to me, considering I do the same thing very often 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50p52o/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50dgp6/)
But which AI? My bet is on claude, it tends to like lists. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m539pxp/)
> claude, it tends to like lists. 
Darn, all my status reports are well-organized lists with multiple levels. I guess I am obsolete. 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50dgp6/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50gypr/)
```
Probability breakdown
The probability this text has been entirely written by a human, AI or a mix of the two.
0% Human
9% Mixed
91% AI

```

From gptzero 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m501e7k/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m4zgx6o/)
100% agree on  over engineering. I once had to add a simple login form. OMG. Claude tried to solve the world hunger in that one feature. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m4zuegc/)
I mean, if you were a good AI and given the chance to write code, wouldn't you AT LEAST try? :P 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/ml025hs/)
Slowly I'm realizing it's because it's trained on the over engineering habits of engineers for the past couple of decades. And I'm starting to believe it's mostly loved by those that engineer complex for nothing solutions. This post AI generated or not is making me think I need to give DeepSeek coder a much closer look for writing Go now. 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/ml025hs/?force-legacy-sct=1) 2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m4zgx6o/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m4zylny/)
You should definitely ask DeepSeek about Claude's implementation! :) 
• [ Promoted ](https://www.reddit.com/user/anthropic-ai/)
See how the Anthropic team uses Claude Code to create Claude Code.
Sign Up
claude.com 
[ TheInfiniteUniverse_ ](https://www.reddit.com/user/TheInfiniteUniverse_/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50fd12/)
Unless you specify that you plan to scale your project in the future, how would DeepSeek know what's in your head? so the simplest choice early on seems logical. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50fd12/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m4zxydk/)
> Yes, that's a good implementation! Your approach is actually simpler and more straightforward 
In my experience, saying the code was created by another prompts sharper critique, while claiming it’s your own often leads to more agreeability and less rigorous feedback. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m509jy7/)
Interesting, I didn’t know Claude was more critical of LLM written code. But yeah, I usually just tell Claude it’s my code or from a collaborator. Must be all the alignment training they do on the models. 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m4zxydk/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50dvg1/)
If you are going to write a post with AI, I will answer with AI: 
Well, well, well, look who's been having a coding party with LLMs! 🤖💻 Seems like DeepSeek is the life of the party with its straightforward, no-nonsense code, while Claude is the sophisticated friend who insists on using the fancy glasses. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m4zqlnn/)
Totally agree. Deepseek tends to be more straightforward and gets right to the point with all its proposals. Claude, on the other hand, is more elaborate, often proposing multiple solutions and pushing for the one that makes the most sense from a software engineering perspective. Claude is much wordier, and sometimes overcomplicates things, introducing "collateral errors." Anyway, they're both amazing programming partners. IMHO Deepseek can be a worthy substitute for Claude. I'm starting to use both equally now. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50bjdh/)
Yes that’s been my experience. I’m using DeepSeek more and more because it’s cheaper. But I find helpful to use Claude to check the other’s code if I’m doing something more critical. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m50bjdh/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m4zqlnn/?force-legacy-sct=1)
[ openbookresearcher ](https://www.reddit.com/user/openbookresearcher/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m5113xa/)
Same experience. DeepSeek is also more straightforward than Gemini, 4o, and o1, in my experience. Over-engineered code is a huuuuge problem industrially and has been for decades, so I very much welcome this return to direct, simple solutions. 
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m4zvci3/)
I think deepseek is more friendly for new programer, when I let it fix my code, it fix it and give me better suggestion to reconstruct it. 
[ Ambitious_Subject108 ](https://www.reddit.com/user/Ambitious_Subject108/)
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m4zq36w/)
+1 for Claude over engineering shit 
[deleted]
• [ 1y ago ](https://www.reddit.com/r/LocalLLaMA/comments/1hrnvjo/comment/m4zif6a/)
It's like they're all sleeper accounts :D 
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of January 2, 2025 ](https://www.reddit.com/posts/2025/january-2-1/global/)
  * [ Reddit  reReddit: Top posts of January 2025 ](https://www.reddit.com/posts/2025/january/global/)
  * [ Reddit  reReddit: Top posts of 2025 ](https://www.reddit.com/posts/2025/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
