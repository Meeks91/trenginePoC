[r/StableDiffusion](https://www.reddit.com/r/StableDiffusion/) • 3y ago
[Most-Background3274](https://www.reddit.com/user/Most-Background3274/)
#  How to fix the error No module 'xformers'. Proceeding without it. in Stable diffusion automatic 1111? 
Share 
• [ Promoted ](https://www.reddit.com/user/google/)
Translate the web to your language. Download Chrome.
Download
google.com 
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/j88zygz/)
add `--xformers` to the command line args line in webui-user.bat. 
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/j8lniwb/)
its not working for me for some reason, always getting the same error. even edited the bat file. 
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/jdf5b05/)
I'm not sure if you're still having this issue. But I was having the same exact issues as you and this fixed it for me. 
> I fixed it by editing the launch.py 
> commandline_args = os.environ.get('COMMANDLINE_ARGS', "--xformers") 
> WebUI does not look for xformers otherwise. It also seems to have installed its own version inside its own venv. 
Source: <https://forums.rockylinux.org/t/rocky-8-7-stable-diffusion-v2/8550/26?page=2>
59 more replies 
59 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/jdf5b05/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/j8lniwb/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/k7n35ye/)
> --xformers 
works, thx! 
• [ 2y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/l37g4fp/)
thank you! works great 
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/j8yy8b5/)
ty, I had too, but what does that xformers thing do? was it bad to not have it? 
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/jdi4nns/)
in a nutshell: allows you to create image with larger size than you would normally be able to without it 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/j8yy8b5/?force-legacy-sct=1)
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/j9nls1u/)
this works in windows, but linux? 
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/jbjz5yt/)
> --xformers 
Thank yoi. Worked for me 
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/jbrdo0p/)
aa100f21a22b1c3bfd5edb45b48d110c99335db8b6821ed4010fa8e4a356aa1f 
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/jj364ar/)
> --xformers 
thanks you mate 
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/jj36mtk/)
You don' need xformers any more on an nvidia card, the latest automatic111 has torch2 which is higher performing in many cases and you can just use 
--opt-sdp-attention 
or --opt-sdp-no-mem-attention instead : <https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Optimizations>
For the same or better performance without the problems of the xfromers binary. 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/jj364ar/?force-legacy-sct=1)
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/k1409uj/)
Thanks , it worked out. 
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/k18xvgk/)
> add --xformers to the command line args line in webui-user.bat. 
This worked for me. It installed xformers and the error didn't appear during webui startup. I thought xformers was already installed. 
3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/j88zygz/?force-legacy-sct=1)
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/j89jnda/)
Please consider using [r/SDtechsupport](https://www.reddit.com/r/SDtechsupport/) for questions like this in the future. 
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/jan0rrf/)
Every time I google something to find an answer this guy in the thread of the top result. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/j89jnda/?force-legacy-sct=1)
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/j88rkys/)
<https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Xformers>
• [ Promoted ](https://www.reddit.com/user/sage_uk/)
Connected data. Clear view.
View More
sage.com 
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/jv5l86d/)
None of the solutions in this thread worked for me, even though they seemed to work for a lot of others. 
Here is a solution that I found online that worked for me. 
Delete the venv folder, and then run webui-user.bat again. This will download xformers and a whole bunch of packages and then install them. The process will create a new venv folder and put the newly installed files in it. This whole process can take a while - about 10-15 minutes or more, if I can recall correctly. 
Have fun! 
• [ 2y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/kpb1ors/)
mine worked after adding --xformers in webui-user.bat 
• [ 2y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/kj8vcth/)
None of the solutions worked. I still get cream colored blank files no matter what model I choose. there is no apparent error in logs. 
version: **v1.7.0** • python: 3.10.6 • torch: 2.0.0+cu118 • xformers: 0.0.20 • gradio: 3.41.2 • checkpoint: **e49e206246**
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/jg6rvkx/)
I used: pip install xformers and it complained about a python location not in PATH. 
I edited System Properties > Environment Variables > System Variables table; New paste path from xformers install error. 
[ Obvious-Strategy-379 ](https://www.reddit.com/user/Obvious-Strategy-379/)
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/jij87w2/)
<https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/5303>
check this 
" No module 'xformers'. Proceeding without it" 
• [ 3y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/jlrtxn9/)
FYI this is not an error. It is a warning at most, but really it is just a message. 
[ Popular_Nail_8692 ](https://www.reddit.com/user/Popular_Nail_8692/)
• [ 2y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/kjwkkqq/)
When you run it in Linux, run `./webui.sh --xformers`
[ Alternative_News3039 ](https://www.reddit.com/user/Alternative_News3039/)
• [ 2y ago ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/l99ctqv/)
This solution worked for me in Linux, Thanks 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/110gizt/comment/kjwkkqq/?force-legacy-sct=1)
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of February 12, 2023 ](https://www.reddit.com/posts/2023/february-12-1/global/)
  * [ Reddit  reReddit: Top posts of February 2023 ](https://www.reddit.com/posts/2023/february/global/)
  * [ Reddit  reReddit: Top posts of 2023 ](https://www.reddit.com/posts/2023/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
