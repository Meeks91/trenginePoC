[r/StableDiffusion](https://www.reddit.com/r/StableDiffusion/) • 1y ago
#  How to install SageAttention, easy way I found 
- SageAttention alone gives you 20% increase in speed (without teacache ), the output is lossy but the motion strays the same, good for prototyping, I recommend to turn it off for final rendering.- TeaCache alone gives you 30% increase in speed (without SageAttention ), same as above.- Both combined gives you 50% increase. 
1- I already had VS 2022 installed in my PC with C++ checkbox for desktop development (not sure c++ matters). can't confirm but I assume you do need to install VS 2022.2- Install cuda 12.8 from nvidia [website](https://developer.nvidia.com/cuda-downloads) (you may need to install the graphic card driver that comes with the cuda ). restart your PC later.3- Activate your conda env , below is an example, change your path as needed:- Run cmd- cd C:\z\ComfyUI- call C:\ProgramData\miniconda3\Scripts\activate.bat- conda activate comfyenv4- Now we are in our env, we install triton-3.2.0-cp312-cp312-win_amd64.whl from [here ](https://github.com/woct0rdho/triton-windows/releases) we download the file and put it inside our comyui folder, and we install it as below:- pip install triton-3.2.0-cp312-cp312-win_amd64.whl5- (updated, instead of v1, we install v2):- since we already are in C:\z\ComfyUI, we do below steps,- git clone <https://github.com/thu-ml/SageAttention.git>- cd sageattention- pip install -e .- now we should see a succeffully isntall of sag v2. 
~~5- (please ignore this v1 if you installed above v2) we install sageattention as below:~~~~- pip install sageattention (this will install v1, no need to download it from external source, and no idea what is different between v1 and v2, I do know its not easy to download v2 without a big mess).~~
6- Now we are ready, Run comfy ui and add a single "patch saga" (kj node) after model load node, the first time you run it will compile it and you get black screen, all you need to do is restart your comfy ui and it should work the 2nd time. 
--- 
* Your first or 2nd generation might fail or give you black screen.* v2 of sageattention requires more vram, with my rtx 3090, It was crashing on me unlike v1, the workaround for me was to use "ClipLoaderMultiGpu" and set it to CPU, this way, the clip will be loaded to RAM and give a room for the main model. this won't effect your speed based on my test.* I gained no speed upgrading sageattention from v1 to v2, probbaly you need rtx 40 or 50 to gain more speed compared to v1. so for me with my rtx 3090, I'm going to downgrade to v1 for now. i'm getting a lot of oom and driver crashes with no gain. 
--- 
Here is my speed test with my rtx **3090** and wan2.1:Without sageattention: 4.54minWith sageattention v1 (no cache): 4.05minWith sageattention v2 (no cache): 4.05minWith 0.03 Teacache(no sage): 3.16minWith sageattention v1 + 0.03 Teacache: 2.40min 
--As for installing Teacahe, afaik, all I did is pip install TeaCache (same as point 5 above), I didn't clone github or anything. and used kjnodes, I think it worked better than cloning github and using the native teacahe since it has more options (can't confirm Teacahe so take it with a grain of salt, done a lot of stuff this week so I have hard time figuring out what I did). 
workflow:pastebin dot com/JqSv3Ugw 
--- 
Btw, I installed my comfy using this guide: [Manual Installation - ComfyUI](https://docs.comfy.org/installation/manual_install)
"conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia" 
And this is what I got from it when I do conda list, so make sure to re-install your comfy if you are having issue due to conflict with python or other env:python 3.12.9 h14ffc60_0pytorch 2.5.1 py3.12_cuda12.1_cudnn9_0pytorch-cuda 12.1 hde6ce7c_6 pytorchpytorch-lightning 2.5.0.post0 pypi_0 pypipytorch-mutex 1.0 cuda pytorch 
bf16 4.54min 
bf16 4.54min 
bf16 with sage no cache 4.05min 
bf16 with sage no cache 4.05min
bf16 no sage 0.03cache 3.32min.mp4 
bf16 no sage 0.03cache 3.32min.mp4
bf16 with sage 0.03cache 2.40min.mp4 
bf16 with sage 0.03cache 2.40min
Read more 
Share 
• [ Promoted ](https://www.reddit.com/user/FigmaOfficial/)
Get started for free.
Learn More
figma.com 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgpsse2/)
I wrote a script to install triton/sage 2 but went on holiday the day the new beta version of the triton wheel was released, so couldn’t try it with Cuda 12.8 . This install is for installs using miniconda. When I get back I’ll write the install script for this for embeded portable versions and for making a new cloned version with a venv. Thanks for the heads up on this op - feel free to take the steps from my script to get Sage 2 (in my posts), it’s fairly easy to read what my script is doing. 
Sage 2 trials - speed initially run with sdpa, went down from 30s/it to 20s/it with Sage 2. 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgptmuu/)
That would be great, thanks! 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgr7cm7/)
Can you update us when that will be done? I would love to try that 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgrn63n/)
I get back on Tuesday, so it’ll be Wednesday or Thursday - I hereby give you permission to send me “bump” messages to remind me on this 
5 more replies 
5 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgrn63n/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgr7cm7/?force-legacy-sct=1) 2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgpsse2/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgq1042/)
> pip install sageattention (this will install v1, no need to download it from external source, and no idea what is different between v1 and v2, I do know its not easy to download v2 without a big mess). 
Like already was said, there is a big difference. But it is not hard to download and install v2 if you already did all the previous steps and your environment doesn't have any issues (like Stability Matrix's), You'd just need to clone the repo and then pip install .\SageAttention (a folder), which would compile the code. 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgq6dhf/)
I see, from what I read, I needed a different version of Python, but I'm going to give it a go now. thanks for the info.I wonder if I could get torch compile to work too. 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgq6n4k/)
I installed it with both Python 3.10 and 3.12, should be fine 
> I wonder if I could get torch compile to work too 
It depends on your GPU and which precision you're using. GGUF and fp16/bf16, etc - would work fine if you have GPU with 8.6 (don't know about lower) computational capability, while fp8 and others wouldn't since it requires 8.9 (needs 40xx series and above). 
3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgq6n4k/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgq6dhf/?force-legacy-sct=1)
[ Numerous-Aerie-5265 ](https://www.reddit.com/user/Numerous-Aerie-5265/)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgqkx7l/)
Anyway to do this if we do use Stability Matrix? 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgqmjtb/)
There is a way. You need to fix its venv first - copy some stuff from your main python folder and put it in the venv of the Stability Matrix, as well as setting up some variables.Like how it is done under this issue: <https://github.com/LykosAI/StabilityMatrix/issues/954>More detailed step by step [guide](https://www.reddit.com/r/StableDiffusion/comments/1iztzbw/comment/mf6d9ae/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button).Or wait for when they would fix it. 
4 more replies 
4 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgqmjtb/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgqkx7l/?force-legacy-sct=1) 4 more replies 
4 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgq1042/?force-legacy-sct=1)
[ superstarbootlegs ](https://www.reddit.com/user/superstarbootlegs/)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgsx0h4/)
I think it gives you less value the lower down the graphics card you go tbh. I have 3060 and havent seen much improvement. Other than it destroyed my comfyui install irreparably forcing me into a 24 hour overhaul after which comfyui ran faster but thats about it. So I guess you could say it brought some imrpvoements. 
4 more replies 
4 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgsx0h4/?force-legacy-sct=1)
• [ Promoted ](https://www.reddit.com/user/OpenAI/)
Put a twist on your selfies with ChatGPT images.
Sign Up
chatgpt.com 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgq81uh/)
you can also install teacache by going to the "custom nodes manager" in comfyui and search for "comfyui-teacache" 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgrrcbs/)
I just tried that, got some import error, sort of fixed it. Tried with flux and wow, my gens now are like x3 times faster. Thanks! 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgq81uh/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mh862vq/)
successfully installed Triton by following this guide: 
<https://github.com/woct0rdho/triton-windows?tab=readme-ov-file>
I wasn't aware your setup uses a Conda Python environment, so I just followed your guide blindly, And it didn’t work, lol. Gave me error code when generating with sage attn node. 
My setup uses an embedded Python environment (I'm using SwarmUI), so I had to slightly adjust the installation steps. After following the tutorial above, both Triton and Sage were successfully installed and sage node works, no error code. Generation time from 400-500 sec only with tea cache to 350 sec with tea + sage. 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mhj45t9/)
I use SwarmUI too. It wasn't obvious to me how to launch the embedded Python environment to properly install the packages (e.g. bleeding-edge triton, sageattention, etc). How is that done, for example in your case? Separately, does SwarmUI detect sageattention and display an option, or does it require loading a workflow manually? 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mhjbljb/)
i just simply install triton and sage inside the comfyui embedded_python folder on my swarmUI folder using this guide : <https://github.com/woct0rdho/triton-windows?tab=readme-ov-file>Before that i install CUDA 12.8 and Visual Studio Build Tools globally (in the visual studio installer i checked the desktop development with C++) 
  * Install triton : `C:\path to your embedded_pyhton folder\python.exe -m pip install -U triton-windows`
  * Install sage : `C:\path to your embedded_pyhton folder\python.exe -m pip install sageattention`
  * example :`C:\aigens\StableSwarmUI\dlbackend\comfy\python_embeded\python.exe -m pip install -U triton-windows`


Next step is download and put two folders **"include"** and **"libs"** into my python_embeded folder to make Triton work, the link to download to these **"include"** and **"libs"** folder is provided in the guide. 
  * And lastly check the triton if it works by copying the script in the guide and save as "[test_triton.py](http://test_triton.py/)" then copy to python_embeded folder and run :`C:\path to your embedded_pyhton folder\python.exe python`[`test_triton.py`](http://test_triton.py/)
  * if the triton installation is correct the script will give you this message : `"`**If you see tensor([0., 0., 0.], device='cuda:0'), then it works**`"`


SwarmUI can use sage attention by adding `--use-sage-attention` on ExtraArgs field in backend setting. If you restart you should see the message `"Using sage attention"` on the console. Or you can use the sage attention node in the comfyUI. if you use the "`--use-sage-attention`" flag, you dont need the sage node on the comfyUI, just pick one of them (flag or node). 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mhjbljb/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mhj45t9/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mh862vq/?force-legacy-sct=1)
[ Ashamed-Variety-8264 ](https://www.reddit.com/user/Ashamed-Variety-8264/)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgpowmr/)
> - pip install sageattention (this will install v1, no need to download it from external source, and no idea what is different between v1 and v2, I do know its not easy to download v2 without a big mess). 
The difference between v1 and v2 is ABSOLUTELY MASSIVE. I just managed to install SageAttention2 on windows on my 5090 and it cut generation time (first block cache @ 0.09) of hunyuan 1024x576x89f 40 step video from 490sec to 158sec(!!!). Generation speed almost tripled. 720x400x85f 40 step generation time 65sec. This is bonkers. 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgq8ogn/)
Is sageatt 2 usefull for 4090? And what is the github? Does it work with comfyui? 
I think I have the first installed not the second. 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgpru86/)
But what about without the cache @ 0.09? I'm going to assume your x3 speed is due to 0.09 since that will triple the speed compared to 0.03.Did you try to compare v1 vs v2 speed to confirm the jump in speed is due to v2?And are there any Tensor accelerators released for wan? That would be awesome to have. 
[ Ashamed-Variety-8264 ](https://www.reddit.com/user/Ashamed-Variety-8264/)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgpt7xs/)
No, cache @ 0.09 was used in both generations. This speedup is from the sage attenion2 alone. Sage attenion 1 gave me more or less 15-20% speedup. 
9 more replies 
9 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgpt7xs/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgpru86/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgpowmr/?force-legacy-sct=1)
• [ Promoted ](https://www.reddit.com/user/adobe/)
Easily clean up anything from your photos with Generative Remove in Lightroom.
Learn More
adobe.com 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgrizdi/)
Easiest way is just to make one portable Comfy with compiled and installed Sage Attention and other optimisation stuff. So you can just download it and use. 
Now it's pain to install it. 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgsbni0/)
The problem is, every single day we get new update, a new model, and new nodes, so making it portable is even harder to maintain, I usually just back up my comfy to another place just to be safe from breaking it. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgsbni0/?force-legacy-sct=1) 1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgrizdi/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgt8a8d/)
Thanks 
• [ 10mo ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/msw1bzp/)
Do you have the exact workflow you are using to generate this videos? I followed the steps and would like to replicate this one. Thanks! 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/msw1bzp/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgpdg0p/)
My cuda installation just gets stuck on installing VS night 
5 more replies 
5 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgpdg0p/?force-legacy-sct=1)
[ FourtyMichaelMichael ](https://www.reddit.com/user/FourtyMichaelMichael/)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgqhacm/)
The work you go through to just not run Linux, is a lot. 
6 more replies 
6 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgqhacm/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgrkiq3/)
Going to try this! I haven't been able to get triton/sage working in ComfyUI so I've been stuck on Wan2GP. I think my issues are bc I'm on python 3.10 and cuda 12.4 but idk since I was able to get them working on my Wan2GP venv 
[ ThatsALovelyShirt ](https://www.reddit.com/user/ThatsALovelyShirt/)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgrr6ds/)
Worth noting if you need to disable "Use Coefficients" if using teacache at 0.03. Otherwise you need to multiply that value by 10. 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgsbdut/)
If I use Coefficients, I don't get any speed up, not sure why. 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgsbdut/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mgrr6ds/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mhujhvs/)
Point 5 - pip install -e . didnt work for me but i used ".\pyhton.exe [setup.py](http://setup.py) install" instead 
Besides that - the whole python/triton/sageattention installation process is a pure nightmare. Almost 2 full days on it and its still not working.. 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mhujhvs/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mhw2uwn/)
OP, is it possible to do these in a Linux environment? I am running comfy on runpod 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mi036vl/)
I think its even easier with linux, you just copy past the nodes and comfy will downlaod it for you. not sure just google it and its more easy than windows from what I've heard. 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mhw2uwn/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mhwsumw/)
Hey, can anyone help me? When i use Sage2 (using custom node, in console there is info ComfyUi patched to sageattention2 or something) i get error SM89 kernel is not available. When i restart comfy and bypass that node everything works just fine. I'm using RTX 3090. Is this GPU not compatible with Sage2 or am I missing something very important? :P 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mhwsumw/?force-legacy-sct=1)
• [ 10mo ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mq7t8wx/)
If you are like me and use **venv** instead of some half-hacked Python distribution, don't fall in a trap of Python not honoring its best practices of using venv. 
Inside venv, it will try to create yet another build environment where torch does not exist and will fail. You must force pip to use the currently active venv: 
```
pip install -e . --no-build-isolation
```

This forces pip to use your existing environment instead of a temporary build sandbox. 
Also, you may skip checking for dependencies if you install PyTorch with cudnn12.x baked-in and have problems with proper detection of the package, like so: 
```
>pip show torch
Version: 2.7.0+cu128
```

... you might even use the following format of the pip command: 
```
pip install -e . --no-build-isolation --no-deps
```

This will both use your venv and skip checking for dependencies, assuming everything is there. I used this format to install it under my venv. 
I was banging my head for the entire afternoon why it constantly fails, even if all online tutorials come down to this tutorial here. It seems I might be one of the rare cases using venv within ComfyUI (old habits die hard), but there it is, for those who might be in the same boat. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/mq7t8wx/?force-legacy-sct=1)
• [ 8mo ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/n40ykiv/)
I have just found that triton-windows can be installed from pip using the below command`pip install triton-windows`
• [ 8mo ago ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/n4fc222/)
i installed sage 2.2 and triton 3.3 and all the related cudas and torches and it keeps failing asking for a sdf...i cannot find this anywhere on the net and it defaults back to pytorch and i have no acceleration from it... 
AttributeError: module 'sageattention' has no attribute 'sdp' 
and no builds have attribute sdp...so how do i make it work..no one else even seems to have this issue either 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1j6kqtd/comment/n4fc222/?force-legacy-sct=1)
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of March 8, 2025 ](https://www.reddit.com/posts/2025/march-8-1/global/)
  * [ Reddit  reReddit: Top posts of March 2025 ](https://www.reddit.com/posts/2025/march/global/)
  * [ Reddit  reReddit: Top posts of 2025 ](https://www.reddit.com/posts/2025/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
