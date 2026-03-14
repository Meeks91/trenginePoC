Actually TikTok offers some endpoints for developers, but that doesn't have many functionality and flexibility.
In this post, we will use the following. 
##  [ davidteather ](https://github.com/davidteather) / [ TikTok-Api ](https://github.com/davidteather/TikTok-Api)
###  The Unofficial TikTok API Wrapper In Python 
# Unofficial TikTok API in Python
This is an unofficial api wrapper for TikTok.com in python. With this api you are able to call most trending and fetch specific user information as well as much more.
This api is designed to **retrieve data** TikTok. It **can not be used post or upload** content to TikTok on the behalf of a user. It has **no support for any user-authenticated routes** , if you can't access it while being logged out on their website you can't access it here.
## Sponsors
These sponsors have paid to be placed here or are my own affiliate links which I may earn a commission from, and beyond that I do not have any affiliation with them. The TikTokAPI package will always be free and open-source. If you wish to be a sponsor of this project check out my [GitHub sponsors page](https://github.com/sponsors/davidteather).
[ **TikAPI** is a paid TikTok…](https://tikapi.io/?ref=davidteather)
This python library allows us to use TikTok data easily and documents are organized very well.
The official doc <https://dteather.com/TikTok-Api/docs/TikTokApi.html>
###  Step1. install the library via pip 
```
$ pip install TikTokApi
$ python -m playwright install

```

Enter fullscreen mode Exit fullscreen mode
###  Step2. get custom_verifyFp 
Go to TikTok and open Dev Tool > Application > Storage > Cookies. Then copy `s_v_web_id` value and paste it to `verifyFp` in the following sample code.
You can see what you need to do to get `s_v_web_id` in the Youtube video. <https://youtu.be/zwLmLfVI-VQ?t=121>
In this sample code, I used `by_hashtag` method that gets the fixed number of videos that have `Messi` as a #tag. In the sample, I set 10 as `count`. <https://dteather.com/TikTok-Api/docs/TikTokApi/tiktok.html#TikTokApi.by_hashtag>
By the way the Youtube video uses `by_trending` <https://dteather.com/TikTok-Api/docs/TikTokApi/tiktok.html#TikTokApi.by_trending>
`test.py`
```
from TikTokApi import TikTokApi
verifyFp='xxx'
api = TikTokApi.get_instance(custom_verifyFp=verifyFp, use_test_endpoints=True)
results = 10
hashtag = 'Messi'
search_results = api.by_hashtag(count=results, hashtag=hashtag)
for tiktok in search_results:
    print(tiktok['video']['playAddr'])

```

Enter fullscreen mode Exit fullscreen mode
###  Step3. run the sample code 
You can get the video links. 
```
$ python test.py
https://v16-web.tiktok.com/video/tos/useast2a/tos-useast2a-pve-0068/f6d3605bceb3438d95d3fc15e1c12707/?a=1988&br=3614&bt=1807&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&expire=1628935350&ft=Q9BExEXk_4ka&l=202108140401520102450730214E194969&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&policy=3&qs=0&rc=M2k0ZmY1cGp0MzMzOTczM0ApaDY3Ojw0ODw4N2RoZmkzO2dhbW0xYzFjZG1gLS00MTZzczAxL2AyNDAyMzAuLy8zXzM6Yw%3D%3D&signature=5deb49d12d31945a3dd829845980247c&tk=0&vl=&vr=
---------------
https://v16-web.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/8644d857973643ff8338cf94b033261b/?a=1988&br=1604&bt=802&cd=0%7C0%7C0&ch=0&cr=0&cs=0&dr=0&ds=2&er=&expire=1628935342&ft=Q9BExEXk_4ka&l=202108140401520102450730214E194969&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&policy=3&qs=0&rc=ajdzcmp0bHk7MzMzNTczM0ApZmVmZzU7aDs0Nzw7aDZlM2djLWVybDBjbi9gLS0vMTRzczAyMy8vYDQtNTY1X15eYWA6Yw%3D%3D&signature=ac6a0aebbedf36463efa08062beca5c6&tk=0&vl=&vr=
---------------
https://v16-web.tiktok.com/video/tos/useast2a/tos-useast2a-ve-0068c003/03fdb77bdb7b4cd89feadd3347ea76d2/?a=1988&br=2438&bt=1219&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&expire=1628935323&ft=Q9BExEXk_4ka&l=202108140401520102450730214E194969&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&policy=3&qs=0&rc=MzZvcGhqNmtqNDMzNzczM0ApaGk6ZWU2M2U1NztpOmY5O2dzZmouNF5ybm5gLS1kMTZzczE0NDIwNTM1YTIwLV8yYTQ6Yw%3D%3D&signature=431b0bdedc5acd4a5d365685cc2bae43&tk=0&vl=&vr=
---------------
https://v16-web.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/3a3df3e144284842bca193e3c3be4c18/?a=1988&br=2718&bt=1359&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&expire=1628935371&ft=Q9BExEXk_4ka&l=202108140401520102450730214E194969&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&policy=3&qs=0&rc=am45bXF0bzk6dzMzMzczM0ApODk7ZWVpaDw6NzY4NjxmZGc1bl9sc2VwY3JfLS00MTRzcy5hMmJeNWA0NWA2MDY0YGM6Yw%3D%3D&signature=93bde49d5fb650e006c38242ce71d443&tk=0&vl=&vr=
---------------
https://v16-web.tiktok.com/video/tos/useast2a/tos-useast2a-ve-0068c002/8236a7de6b7d45f68534c340ff20704a/?a=1988&br=990&bt=495&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&expire=1628935366&ft=Q9BExEXk_4ka&l=202108140401520102450730214E194969&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&policy=3&qs=0&rc=am1xcTQ6ZnBuNzMzNzczM0ApOWY0aWU0OGRpNzM0ZDZpOWdiMmRscjQwcTNgLS1kMTZzc18vNjAzYl4uXjJhNDBjLTA6Yw%3D%3D&signature=da88c5351234be29a34a06f7fe85dc32&tk=0&vl=&vr=
---------------
https://v16-web.tiktok.com/video/tos/useast2a/tos-useast2a-ve-0068c003/123acb35db624af0ace6c4cc9f08d98f/?a=1988&br=5028&bt=2514&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&expire=1628935342&ft=Q9BExEXk_4ka&l=202108140401520102450730214E194969&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&policy=3&qs=0&rc=M2R5b2tvajp3NDMzZDczM0ApNTs3OGVlOjw8Nzs3OzNmNmdhM2Rzcl9wazVgLS1iMTZzcy8tNC8yLzE0MGE2M2A1MS86Yw%3D%3D&signature=8d0a6ea7e6cd392ec1c1b21a683a3764&tk=0&vl=&vr=
---------------
https://v16-web.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/db36a067db27458c9eb975e729951244/?a=1988&br=2436&bt=1218&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&expire=1628935335&ft=Q9BExEXk_4ka&l=202108140401520102450730214E194969&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&policy=3&qs=0&rc=MzRneWc6ZmhtNjMzODczNEApOWQ1NmVlZmRoNzQ6NTk0OWc2NmktcjRfZWtgLS1kMS1zc18zNC82YDRiMDJiMjYtMmE6Yw%3D%3D&signature=b60291c707247f301dd61dd161a1182d&tk=0&vl=&vr=
---------------
https://v16-web.tiktok.com/video/tos/useast2a/tos-useast2a-ve-0068c001/27d1b30e58df44d99e008c1928e9cba9/?a=1988&br=2388&bt=1194&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&expire=1628935363&ft=Q9BExEXk_4ka&l=202108140401520102450730214E194969&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&policy=3&qs=0&rc=M2d4aGR1MzpkMzMzNjczM0ApM2RoaGgzZGQzN2U5Njk4NGdlaC5jbGtyaWFgLS0vMTZzczU1MWJgNDJgMi8uNTFiNWI6Yw%3D%3D&signature=c7df3d189e5e7bd449969f34d50cab3e&tk=0&vl=&vr=
---------------
https://v16-web.tiktok.com/video/tos/useast2a/tos-useast2a-pve-0068/bcb98c935ab443de9658dcd5760f939f/?a=1988&br=1448&bt=724&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&expire=1628935330&ft=Q9BExEXk_4ka&l=202108140401520102450730214E194969&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&policy=3&qs=0&rc=M2V2dTM1cDk1NjMzNzczM0ApOTxnaTkzZDw3N2UzZWk6M2dyMmAwYzE0XmRgLS1kMTZzczZhNDViYTNiNV9eXjNgLzQ6Yw%3D%3D&signature=9c5d5009e266981b310682a2df1d3cdf&tk=0&vl=&vr=
---------------
https://v16-web.tiktok.com/video/tos/useast2a/tos-useast2a-pve-0068/55c9cb8875174673b81a67db4b0c7be1/?a=1988&br=1338&bt=669&cd=0%7C0%7C1&ch=0&cr=0&cs=0&cv=1&dr=0&ds=3&er=&expire=1628935340&ft=Q9BExEXk_4ka&l=202108140401520102450730214E194969&lr=tiktok_m&mime_type=video_mp4&net=0&pl=0&policy=3&qs=0&rc=M3BldTczaWRldTMzMzczM0ApNmQ4Nmc0NWRoNzZmOjkzZWdfMmEyYTY0MmhfLS1iMTZzc2AvNi0uMTEtLTAzY18yMTA6Yw%3D%3D&signature=26cd0d759ece16582dbd0fa3985040b7&tk=0&vl=&vr=
---------------

```

Enter fullscreen mode Exit fullscreen mode
If you want to know the general return, you can see it ↓
<https://gist.github.com/koji/143ea8387403899c069464cbde61efae>
[ MongoDB ](https://dev.to/mongodb) Promoted
Dropdown menu
##  [Scale globally with MongoDB Atlas. Try free.](https://www.mongodb.com/cloud/atlas/lp/try3?utm_campaign=display_devto-broad_pl_flighted_atlas_tryatlaslp_prosp_gic-null_ww-all_dev_dv-all_eng_leadgen&utm_source=devto&utm_medium=display&utm_content=scalbglobally-v1&bb=241233)
MongoDB Atlas is the global, multi-cloud database for modern apps trusted by developers and enterprises to build, scale, and run cutting-edge applications, with automated scaling, built-in security, and 125+ cloud regions.
Read More 
[ AdemVincen  ](https://dev.to/ademvincen)
AdemVincen 
[ AdemVincen  ](https://dev.to/ademvincen)
Follow
  * Joined 
6 Feb 2023


• [ 6 Feb 23 • Edited on 6 Feb • Edited ](https://dev.to/0xkoji/get-tiktok-video-with-less-10-lines-python-code-328o#comment-24ihc)
Dropdown menu
  * Hide 


Great post on how to get TikTok videos with just a few lines of Python code. As a fellow Python enthusiast, I really appreciate the simplicity of the code you shared. This is a great place to start for those new to programming or just beginning to explore the world of Python. And for those already familiar with the language, this code provides a quick and easy solution for downloading TikTok videos. Have you tried using the [Download TikTok Video](https://www.sstiktok.org/en) tool? It's a great way to quickly download and save TikTok videos to your device without having to go through the hassle of writing any code. If interested, give it a try and let us know what you think!
[ GellRows  ](https://dev.to/gellrows)
GellRows 
[ GellRows  ](https://dev.to/gellrows)
Follow
  * Joined 
31 Jan 2023


• [ 31 Jan 23 ](https://dev.to/0xkoji/get-tiktok-video-with-less-10-lines-python-code-328o#comment-24epa)
Dropdown menu
  * Hide 


As a programmer, I really enjoyed these videos.
[ Macmarisha  ](https://dev.to/macmarisha)
Macmarisha 
[ Macmarisha  ](https://dev.to/macmarisha)
Follow
  * Joined 
25 Oct 2023


• [ 31 May 24 ](https://dev.to/0xkoji/get-tiktok-video-with-less-10-lines-python-code-328o#comment-2ffdd)
Dropdown menu
  * Hide 


You can use the requests library to fetch the video content. 
For further actions, you may consider blocking this person and/or [reporting abuse](https://dev.to/report-abuse)
[ Postmark ](https://dev.to/postmark) Promoted
Dropdown menu
##  [Seamless email integration with excellent deliverability ✅ 👀](https://postmarkapp.com/lp/postmark-email-api-alt?utm_medium=devto-static&utm_campaign=devto-static-ad-video-thumbnail&utm_source=devto&bb=261207)
Start sending in minutes with Postmark's powerful email API.
DEV Community
Dropdown menu
#  Celebrate Underrepresented Voices in Tech 
**Draw what comes to mind for you when you think of gender equity in tech.**
Whether it’s a symbolic representation of the "glass ceiling" being shattered, a detailed portrait of a pioneer who paved the way, or a piece of abstract art representing the strength of a diverse community, we want to see your interpretation through code. You may use any frontend tools 
