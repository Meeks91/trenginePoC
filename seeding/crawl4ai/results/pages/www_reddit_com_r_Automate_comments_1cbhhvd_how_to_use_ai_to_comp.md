• 2y ago
#  How to use AI to completely automate your youtube channel 
Hi folks, 
I wanted to share with you a cool project I recently undertook that leverages the power of AI to help manage my YouTube channel! 
The idea was to use [CrewAI](https://www.crewai.com/) to automate tasks like competitor YouTube channel analysis and identify trending topics. This way, I could gauge these topics against my own content ideas to see if there is general interest in a given topic. 
The AI Crew was designed to crawl the web (Google) and call APIs like the YouTube API, Reddit API, and use Google Trends to determine how likely a given topic is to generate engagement. 
For this, I created the following AI Assistants (or agents in CrewAI lingo): 
  * A competitor analysis agent 
  * A Content Creator (to generate ideas from research) 
  * A Marketing advisor, to generate catchy titles and tags 
  * An Analytics consultant to measure the performance of the video 


I used a pretty straightforward setup that relied on the usual suspects: 
  * Anaconda 
  * Python 3.11 
  * A few modules like pytrend, praw, serper, and langchain 


I tested it with models like GPT-4, GPT-4-Turbo, and a few local models like nous-hermes 2, mistral, and codellama, among others. 
The results from GPT-4-Turbo were AMAZING, and I'm sure I can make them better by fine tuning the data going into the model, but they were not really that great with local AI, which was quite expected given the imense number of tokens. However I was quite positively surprised by the performance of Nous Hermes 2 - 13b. Not only did it actually run, but it used the tools I custom build for it! Quite impressive really 
The video is available below: 
<https://youtu.be/5JoVeYcxgpU?si=cxFwHO1x_zCghMYB>
You are more than welcome to try out the code for yourselves: <https://github.com/fmiguelmmartins/crewaiyoutube>
And here is an article on Medium with the step-by-step process (don't worry, I have a free account): 
<https://medium.com/@fmiguelmmartins/create-an-ai-team-to-manage-your-youtube-channel-5dc1e6c9b31b>
Hope you guys enjoy it, and if you are kind enough, please leave me some feedback so I can improve over time! 
Thank you! 
Filipe 
Read more 
Share 
• [ Promoted ](https://www.reddit.com/user/OpenAI/)
Put a twist on your selfies with ChatGPT images.
Sign Up
chatgpt.com 
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/1cbhhvd/comment/l0yh0u0/)
This is very cool! How hard was the programming of the agents? 
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/1cbhhvd/comment/l0ymrb9/)
YouTube removes Ai content channels, if those are not marked properly. 
Ai content channels compete with other Ai content channels. 
Future garbage pile. 
AI + human edits is the best ! 
[ Glad-Syllabub6777 ](https://www.reddit.com/user/Glad-Syllabub6777/)
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/1cbhhvd/comment/l103mng/)
Love the idea: AI + human edits is the best !. AI helps video editor to save time. 
[ thewolfofslovenia ](https://www.reddit.com/user/thewolfofslovenia/)
• [ 1y ago ](https://www.reddit.com/r/Automate/comments/1cbhhvd/comment/ma1jmsv/)
Not true, quick examples I found: 
  * <https://www.youtube.com/@BibleNutshells>
  * <https://www.youtube.com/@judahsketchanimation>
  * <https://www.youtube.com/@RealStoicJournal>
  * <https://www.youtube.com/@DreamSparks34>
  * <https://www.youtube.com/@wise_vibes>
  * <https://www.youtube.com/@10xincome>
  * <https://www.youtube.com/@bmresearch1>
  * <https://www.youtube.com/@taketheleapmotivation>


They are raking in a ton of views, first one is doing millions of views per video... Blue ocean right now, not a lot of creators know how to put out visually appealing AI content. I figured it out and its been going super super well. I just need to streamline and automate even more haha, hopefully by the end of this year I'll hit my goal of 100 yt automated channels 
[ Continue this thread  ](https://www.reddit.com/r/Automate/comments/1cbhhvd/comment/l0ymrb9/?force-legacy-sct=1)
[deleted]
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/1cbhhvd/comment/lgpklxe/)
Youtube Ai is shit content and i hope someone creates a tool to block trash like what you are creating 
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/1cbhhvd/comment/lgxvad1/)
I completely agree with you! AI content is garbage!! But if you watch the video, it's not AI content per say, it's just a few "assistants" to do things like ideas for titles and thumbnails, check if the content I am about to create is of any use or worth to anyone... etc... It's not a video generator, but more like a helper for the tasks that honestly are no fun (at least for me). Making a video demands a lot of hours, and since my videos are educational, I want to make sure that there is an audience and more important, that the content will add value to someone's life. But I agree with you, a purely created AI video (if that ever comes to fruition), music, authoring, etc... is a waste for our humanity! Don't worry my scripts, videos, b-role, tutorials, animations, editing, are all done by me! and boy... it's a LOT of hours hahaha! But as we say in Portugal "you don't get tired when you are running for fun!" :) 
[ Continue this thread  ](https://www.reddit.com/r/Automate/comments/1cbhhvd/comment/lgpklxe/?force-legacy-sct=1)
[ thewolfofslovenia ](https://www.reddit.com/user/thewolfofslovenia/)
• [ 1y ago ](https://www.reddit.com/r/Automate/comments/1cbhhvd/comment/ma1j5h0/)
That’s awesome! I love how you built a whole AI “team” for everything from competitor analysis to marketing. If you want to step it up and make it super automated, especially if you’re putting out a lot of content you can use all in one tool like Katalist AI to automate most of the production process. Also, if you need quick visuals or thumbnails, tools like Pikzels can churn decent ones pretty fast. I use these two + stack of ChatGpt and VidIQ and its been going super weel 
• [ 1y ago ](https://www.reddit.com/r/Automate/comments/1cbhhvd/comment/mlufpfl/)
I mean there is very easy way to get monetized, not something very hard, I started as noob, and discovered "How To AI" on Youtube with his courses... 
I paid the small amount it cost and I got nice results in few weeks, I am doing nice now. 
Check his shit, he is providing it for free, with his course having it all, step by step, you will suceed, just blindly follow fr, lmao : [https://whop.com/howtoai](https://whop.com/checkout/plan_wFfLMTOJv8irt/?a=arnost&d2c=true) , its few $, you can make it... 
Or this one, with a more entry cost, but also much more personal touch a pretty much guarantee of monetization... [https://whop.com/howtoai](https://whop.com/checkout/plan_mMR65P3H5u8qY/?a=arnost&d2c=true) Then it is just about you to get good content. 
• [ 8mo ago ](https://www.reddit.com/r/Automate/comments/1cbhhvd/comment/n1189ke/)
I think there is a new kid on the block that would be more efficient at what you are trying to do - Have you checked out Opus Clips? I'm obviously a huge fan, and it has some crazy AI capabilities. 
• [ 7mo ago ](https://www.reddit.com/r/Automate/comments/1cbhhvd/comment/n9b4uwo/)
Great workflow! One area often missed: comment automation. 
Built an AI agent that categorizes comments by business intent and auto-suggests replies. Perfect addition to your stack. 
PS. The Agent also replies to comments autonomously 
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of April 23, 2024 ](https://www.reddit.com/posts/2024/april-23-1/global/)
  * [ Reddit  reReddit: Top posts of April 2024 ](https://www.reddit.com/posts/2024/april/global/)
  * [ Reddit  reReddit: Top posts of 2024 ](https://www.reddit.com/posts/2024/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
