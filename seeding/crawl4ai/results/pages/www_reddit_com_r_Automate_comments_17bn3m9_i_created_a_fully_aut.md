• 2y ago
#  I created a fully automated AI youtube channel 
**Content Acquisition:**
I use the Wikipedia API to retrieve articles. 
**Content cleaning and Validation:**
I clean the articles to grab the main text and then I use Spacy to validate if the articles are "safe" aswell as other criteria and then score the articles. I then store the articles and scores in a database. 
**Article Selection:**
An article is chosen based on its score. 
**Script Creation:**
LlamaV2, a local large language model, processes the raw article to create the video script. 
**Visual Creation:**
I used stable diffusion to generate the actor. 
The background was then removed and replaced with a green screen. 
**Audio Production:**
The video script is converted into audio using tortoise-tts. 
For the background music I am using Facebook's audio-craft. 
**Head Animation:**
A one-shot talking face is used for the head animation, which is then enhanced using wav2lip and codeformer. 
**Frame Optimization:**
Rife is used for frame interpolation to make the animations smooth. 
**Background Animation:**
LlamaV2 crafts scene prompts based on the script. These prompts are then forwarded to animatediff to produce the background animation. 
**Metadata Creation:**
LlamaV2 is also responsible for generating video titles and hashtags. 
**Subtitles :** Whisper for Subtitles 
**Uploading:**
I use the YouTube API to upload the final video. 
**Additional Integration:**
A significant amount of custom code has been written to integrate with all of the tools, as well as optimisations.A cronjob and a taskfile 
This is running on 6Gb vram old laptop and takes 2-3 hours to finish the whole pipeline. 
It's by no means flawless, but I enjoyed working on this project.<https://www.youtube.com/@uncannyagent><https://www.youtube.com/shorts/S3RmJ9YMk1A>
I also have a tiktok channel but its not automated like youtube. 
Read more 
Share 
• [ Promoted ](https://www.reddit.com/user/Altium_Official/)
What if you didn’t have to pay for enterprise features you never use? Altium Develop delivers professional-grade electronics design—without the enterprise price tag.
Learn More
altium.com 
[deleted]
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5lv8ns/)
Is there a git repo I'd like to make a talking head to introduce my music videos 
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5lw12e/)
Hey, the one I’m using is from <https://github.com/camenduru/one-shot-talking-face-colab>
But there’s easier projects like <https://github.com/OpenTalker/SadTalker>
its probably better than the one I’m using. 
[ Continue this thread  ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5lv8ns/?force-legacy-sct=1)
[ Spirited_Employee_61 ](https://www.reddit.com/user/Spirited_Employee_61/)
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5mt1iw/)
6GB VRAM for animatediff???? Along with using Llama-2???? You must tell me how you did that! also are you using 7b model for llama2? 
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5o1bsc/)
I had to tweak animation.py to move some latents to cpu, I believe it was with gif processing function and xformers, I can’t confirm now but I’ll add some details later, for llama I’m using llama_cpp 13b one of the newest orcas finetunes 
[ Continue this thread  ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5mt1iw/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5nzcmr/)
Nice! I have one too: <https://www.youtube.com/@TheAIgorithm/shorts>
I like that yours does animation too :) 
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5o1f6n/)
That’s really cool thanks for sharing, I’ll subscribe 
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5o1vnw/)
You don’t have animation, but your content is definitely cleaner and more interesting than what I’m doing, keep it up 
[ Continue this thread  ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5nzcmr/?force-legacy-sct=1)
• [ Promoted ](https://www.reddit.com/user/XeroGlobal/)
As a sole trader or landlord, you can get ahead of MTD for Income Tax with Xero’s HMRC-recognised software. Go beyond compliance by bringing all your income streams together under one plan, for one price, in one organised place.
Learn More
xero.com 
Terms Apply* 
[ IntelligentAirport26 ](https://www.reddit.com/user/IntelligentAirport26/)
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5va6dz/)
Automated as in it just constantly puts out content? 
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5vr693/)
Correct, I have it disabled currently, but the whole pipeline runs on a cronjob 
[ IntelligentAirport26 ](https://www.reddit.com/user/IntelligentAirport26/)
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k63pggu/)
how do you automate animatediff? 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k63pggu/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5vr693/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k5va6dz/?force-legacy-sct=1)
[ Glad-Syllabub6777 ](https://www.reddit.com/user/Glad-Syllabub6777/)
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/kxthonf/)
How do you produce the final video? 
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k68nq2q/)
really would love to explore this concept script to upload and cron the uploads except checking to see if the final version fits the needs of you tube integration. Is this a java script that runs it or some other style .. let me know 
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k69pzph/)
for the pipeline I'm using<https://taskfile.dev/>Calling different python scripts/ tools 
For the cronjob I am using crontab in linux I have a basic debian server running all that 
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k69qd55/)
Its easier than just using a Makefile with targets, so I highly recommend that for simple local pipelines 
[ Continue this thread  ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k69pzph/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k68nq2q/?force-legacy-sct=1)
• [ Promoted ](https://www.reddit.com/user/Try_Luma_AI/)
Create without limits. Imagine without compromise.
lumalabs.ai 
Learn More
[ Routine_Mechanic4962 ](https://www.reddit.com/user/Routine_Mechanic4962/)
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/k6w8lyt/)
I find the head animation very interesting, however the only "negative" thing I could say is that the videos didn't feel coherent because of the randomly generate visuals (at least the ones I saw), you should probably use static imagery and generate images via api using dall-e 3 and maybe hope something local similar gets released with feats similar to pikalabs. I guess since the whole point is full automation maybe there is no space for reviewing footage, etc... Still it is impressive even more so for something running on an old laptop and I'm sure you will benefit even more as these AI tools become more efficient and accurate. 
[deleted]
• 2y ago
Comment deleted by user
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/lg7elg9/)
I will be messaging you in 7 days on [**2024-08-09 21:25:19 UTC**](http://www.wolframalpha.com/input/?i=2024-08-09%2021:25:19%20UTC%20To%20Local%20Time) to remind you of [**this link**](https://www.reddit.com/r/Automate/comments/17bn3m9/i_created_a_fully_automated_ai_youtube_channel/lg7egjr/?context=3)
[**CLICK THIS LINK**](https://www.reddit.com/message/compose/?to=RemindMeBot&subject=Reminder&message=%5Bhttps%3A%2F%2Fwww.reddit.com%2Fr%2FAutomate%2Fcomments%2F17bn3m9%2Fi_created_a_fully_automated_ai_youtube_channel%2Flg7egjr%2F%5D%0A%0ARemindMe%21%202024-08-09%2021%3A25%3A19%20UTC) to send a PM to also be reminded and to reduce spam. 
Parent commenter can  [delete this message to hide from others.](https://www.reddit.com/message/compose/?to=RemindMeBot&subject=Delete%20Comment&message=Delete%21%2017bn3m9)  
[ JicamaComfortable344 ](https://www.reddit.com/user/JicamaComfortable344/)
• [ 2y ago ](https://www.reddit.com/r/Automate/comments/17bn3m9/comment/lg7fhbm/)
RemindMe ! 7 day 
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of October 19, 2023 ](https://www.reddit.com/posts/2023/october-19-1/global/)
  * [ Reddit  reReddit: Top posts of October 2023 ](https://www.reddit.com/posts/2023/october/global/)
  * [ Reddit  reReddit: Top posts of 2023 ](https://www.reddit.com/posts/2023/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
