[r/MachineLearning](https://www.reddit.com/r/MachineLearning/) • 3y ago
[Thin-Shirt6688](https://www.reddit.com/user/Thin-Shirt6688/)
#  [R] What are some papers that describe TikTok's algorithm? 
I'm looking for a recent conference paper that describes how TikTok's algorithm works. 
As an analogy, YouTube's algorithm was described by Zhao et al., (RecSys 2019) "Recommending what video to watch next: a multitask ranking system" 
Read more 
Share 
• [ Promoted ](https://www.reddit.com/user/AlibabaCloud_Ads/)
🚀 Vibe Code. Ship Faster. Spend Smarter. ⚡Qwen Coding Plan is LIVE on Alibaba Cloud Model Studio 💥Multi-model power on one platform. Seamless tool support. Faster shipping with the Qwen Coding Plan, with zero surprise bills.
Apply Now
int.alibabacloud.com 
[ _poisonedrationality ](https://www.reddit.com/user/_poisonedrationality/)
• [ 3y ago ](https://www.reddit.com/r/MachineLearning/comments/111e9hx/comment/j8elkeq/)
The paper you link does not describe YouTube's algorithm. YouTube's selection algorithm is proprietary and not revealed to the public. You just linked a paper from researchers at Google studying the topic of video recommendation. The extent to which it describes youtube's actual algorithm is not at all obvious. 
• [ 3y ago ](https://www.reddit.com/r/MachineLearning/comments/111e9hx/comment/j8ehkvl/)
Some researchers at tiktok's parent company released a paper on a  called Monolith here: <https://arxiv.org/abs/2209.07663>. 
I'm not sure its actually what tiktok is using, but they do say that "Monolith has successfully landed in the  product". 
• [ 3y ago ](https://www.reddit.com/r/MachineLearning/comments/111e9hx/comment/j8esd6k/)
These are their features: 
<https://www.cs.princeton.edu/courses/archive/spring21/cos598D/icde_2021_camera_ready.pdf>
The paper also references older [neural network architectures](https://www.reddit.com/search/?q=neural+network+architectures+recsys&cId=4808fc22-abb6-4ed9-8a59-9ba46ae0d1ba&iId=d26f2fed-68b5-4bf3-94f5-25bf1e71439f) used in late stages of the recsys stack. 
[ Kitchen_Tower2800 ](https://www.reddit.com/user/Kitchen_Tower2800/)
• [ 3y ago ](https://www.reddit.com/r/MachineLearning/comments/111e9hx/comment/j8gb25a/)
Typically, large companies don't use a single model, but rather a large number of different models, all performing different tasks (recommending, filtering, etc). It would very difficult to describe the complete recommendations pipeline (i.e from user request to final candidate) in a single academic paper. 
• [ 3y ago ](https://www.reddit.com/r/MachineLearning/comments/111e9hx/comment/j8gh6ci/)
Also interested been looking into this myself. Some materials of potential interest: 
Official  describing with very limited detail how it works: [How TikTok recommends videos #ForYou](https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you)
Papers: 
  * [An Empirical Investigation of Personalization Factors on TikTok (2022)](https://arxiv.org/pdf/2201.12271v1.pdf) - sock puppet methodology to identify the parameters and their strength in influencing the algo 
  * [Analysis on the “Douyin (Tiktok) Mania” Phenomenon Based on Recommendation Algorithms (2021)](https://pdfs.semanticscholar.org/ffe8/77e4093a8f879d5543c71cf294488effb0a7.pdf)
  * [Trick and Please. A Mixed-Method Study On User Assumptions About the TikTok Algorithm (2021)](https://dl.acm.org/doi/pdf/10.1145/3447535.3462512)
  * [Leveraging Rights of Data Subjects for Social Media Analysis: Studying TikTok via Data Donations (2023)](https://arxiv.org/pdf/2301.04945.pdf) - may be of interest 


WSJ did a video on them trying to reverse engineer the algorithm, not too technical though [Investigation: How TikTok's Algorithm Figures Out Your Deepest Desires](https://www.wsj.com/video/investigation-how-tiktok-algorithm-figures-out-your-deepest-desires/DADACF48-CE1D-48D5-A674-6692E7FA67FC.html)
Some blogs I came across that may or may not be reliable: 
  * [Why TikTok made its user so obsessive? The AI Algorithm that got you hooked.](https://towardsdatascience.com/why-tiktok-made-its-user-so-obsessive-the-ai-algorithm-that-got-you-hooked-7895bb1ab423)
  * [The App That Knows You Better than You Know Yourself: An Analysis of the TikTok Algorithm](https://chatbotslife.com/the-app-that-knows-you-better-than-you-know-yourself-an-analysis-of-the-tiktok-algorithm-be12eefaab5a)


• [ 3y ago ](https://www.reddit.com/r/MachineLearning/comments/111e9hx/comment/j8i53bg/)
Thanks! Much appreciated. 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/111e9hx/comment/j8gh6ci/?force-legacy-sct=1)
• [ 3y ago ](https://www.reddit.com/r/MachineLearning/comments/111e9hx/comment/j8h3qgi/)
Whatever you can read are outdated. They don't reveal what they actually use. They are rumored to have the best recommendation system. 
• [ 3y ago ](https://www.reddit.com/r/MachineLearning/comments/111e9hx/comment/j8iqbah/)
There is the claim that any system can be (approximately) reverse engineered if one has access to the results of the system. Are those too hidden from the public? 
What is "best" is subjective. At least I was reading last week that any moderate fitness related interest brings quite unhealthy content very quickly. But it has to be better than Amazon's system, anyway. 
[ new_name_who_dis_ ](https://www.reddit.com/user/new_name_who_dis_/)
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/111e9hx/comment/kc3zo16/)
I think OP is correct in that they have the best rec system. However i dont' think you can reverse engineer it because I don't think their algorithm has some magic bullet. I think they just have the best dataset / feature engineering / amount of views and time spent on app, of any other recommender system in the world. 
Each swipe is a datapoint for them. And it's the most used app in the world by time spent on the app (or at least it was but I imagine it still is). 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/111e9hx/comment/j8iqbah/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/111e9hx/comment/j8h3qgi/?force-legacy-sct=1)
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of February 13, 2023 ](https://www.reddit.com/posts/2023/february-13-1/global/)
  * [ Reddit  reReddit: Top posts of February 2023 ](https://www.reddit.com/posts/2023/february/global/)
  * [ Reddit  reReddit: Top posts of 2023 ](https://www.reddit.com/posts/2023/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
