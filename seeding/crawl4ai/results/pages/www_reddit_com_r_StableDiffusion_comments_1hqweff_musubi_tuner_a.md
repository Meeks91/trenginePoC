[r/StableDiffusion](https://www.reddit.com/r/StableDiffusion/) • 1y ago
[Cheap_Fan_7827](https://www.reddit.com/user/Cheap_Fan_7827/)
#  Musubi Tuner, another trainer for Hunyuan Video 
<https://github.com/kohya-ss/musubi-tuner>
Also it supports block swap! Training lora on 12GB is possible. 
The usage is almost the same as sd-scripts. 
Read more 
Share 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4tmv9l/)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4u5fva/)
Here we go again 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4tmv9l/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4t8ajt/)
Can you train with videos? There's a huge difference in requirements between video and image training. Images was already possible under 24 gig vram. 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4tbo1t/)
**This repository is under development. Only image training has been verified.**
according to readme 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4txon8/)
What does that mean please? I train 10 images of character X and the model will automatically guess the movement and action? 
6 more replies 
6 more replies 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4txon8/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4tbo1t/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4t8ajt/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4t55ir/)
my training command; 
accelerate launch --num_cpu_threads_per_process 1 --mixed_precision bf16 hv_train_network.py --dit D:\HunyuanVideo\hunyuan-video-t2v-720p\transformers\mp_rank_00_model_states.pt --dataset_config C:\Grabber\doto\dataset_config.toml --sdpa --mixed_precision bf16 --fp8_base --optimizer_type adamw8bit --learning_rate 2e-3 --gradient_checkpointing --max_data_loader_n_workers 1 --persistent_data_loader_workers --network_module=networks.lora --network_dim=32 --timestep_sampling sigmoid --discrete_flow_shift 1.0 --max_train_epochs 16 --save_every_n_epochs=1 --seed 42 --output_dir C:\AI_related --output_name name-of-lora --blocks_to_swap 20 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4tz5ea/)
Script? 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4uhrac/)
I'm currently stuck at this step: 
In order to save GPU memory resources for model loading, we separate the language model parts of llava-llama-3-8b-v1_1-transformers into text_encoder. 
cd HunyuanVideo python hyvideo/utils/preprocess_text_encoder_tokenizer_utils.py --input_dir ckpts/llava-llama-3-8b-v1_1-transformers --output_dir ckpts/text_encoder 
I've downloaded the script from the HunyuanVideo repo on git, put the file in a folder named "utils" and tried to execute the command from the main folder but it gives me a syntax error: 
J:\AI\musubi-tuner>python hyvideo/utils/preprocess_text_encoder_tokenizer_utils.py --input_dir ckpts/llava-llama-3-8b-v1_1-transformers --output_dir ckpts/text_encoder File "J:\AI\musubi-tuner\hyvideo\utils\preprocess_text_encoder_tokenizer_utils.py", line 112 <title>HunyuanVideo/hyvideo/utils/preprocess_text_encoder_tokenizer_utils.py at main · Tencent/HunyuanVideo · GitHub</title> ^ SyntaxError: invalid character '·' (U+00B7) 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4zjbql/)
you forgot to do cd HunyuanVideo 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4zjbql/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m7o4sc6/)
it doesn't like the middle dot character in the title. Rename things and it should be fine. 
You can also try replacing it with `&#x00B7;`
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4uhrac/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4t55ir/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4uzq8n/)
This is great ! 
Happy New Year ! 
[deleted]
• 1y ago
Comment deleted by user
[ Secure-Message-8378 ](https://www.reddit.com/user/Secure-Message-8378/)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m56xspl/)
There's a Lora for Ghibli Studio.<https://civitai.com/models/1084814/studio-ghibli-style-hunyuanvideo>
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4uzq8n/?force-legacy-sct=1)
[ Secure-Message-8378 ](https://www.reddit.com/user/Secure-Message-8378/)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4ylybn/)
Really it needs 64GB RAM? 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4zihcm/)
No. 32GB with swap is enough for training and generating. 
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m5br85z/)
_cries with 16GB_
[ Secure-Message-8378 ](https://www.reddit.com/user/Secure-Message-8378/)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m5187e7/)
Thanks! 
[ Secure-Message-8378 ](https://www.reddit.com/user/Secure-Message-8378/)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m5646ot/)
Is it easy setup the app? 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4zihcm/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4ylybn/?force-legacy-sct=1)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m4tnny3/)
[ Secure-Message-8378 ](https://www.reddit.com/user/Secure-Message-8378/)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m56xfqn/)
Anyone is using for Hunyuan Loras? In Windows, I mean. 
[ Aromatic-Low-4578 ](https://www.reddit.com/user/Aromatic-Low-4578/)
• [ 1y ago ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/mdwtisf/)
Yes. I have a slightly modified version I'm using in windows without issue. Message me if you want a copy. 
[ Continue this thread  ](https://www.reddit.com/r/StableDiffusion/comments/1hqweff/comment/m56xfqn/?force-legacy-sct=1)
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of January 1, 2025 ](https://www.reddit.com/posts/2025/january-1-1/global/)
  * [ Reddit  reReddit: Top posts of January 2025 ](https://www.reddit.com/posts/2025/january/global/)
  * [ Reddit  reReddit: Top posts of 2025 ](https://www.reddit.com/posts/2025/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
