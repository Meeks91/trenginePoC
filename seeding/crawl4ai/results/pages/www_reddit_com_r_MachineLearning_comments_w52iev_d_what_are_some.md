[r/MachineLearning](https://www.reddit.com/r/MachineLearning/) • 4y ago
#  [D] What are some good resources to learn CUDA programming? 
I wanted to get some hands on experience with writing lower-level stuff. I have seen CUDA code and it does seem a bit intimidating. I have good experience with Pytorch and C/C++ as well, if that helps answering the question. Any suggestions/resources on how to get started learning CUDA programming? Quality books, videos, lectures, everything works. 
Read more 
Share 
• [ Promoted ](https://www.reddit.com/user/FigmaOfficial/)
Seeing is believing. Prove your work is worth it with a working proof of concept.
Learn More
figma.com 
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih5lowo/)
If you're familiar with Pytorch, I'd suggest checking out their [custom CUDA extension](https://pytorch.org/tutorials/advanced/cpp_extension.html) tutorial. 
They go step by step in implementing a kernel, binding it to C++, and then exposing it in Python. 
For learning purposes, I modified the code and wrote a simple kernel that adds 2 to every input. 
This is strongly Python/Pytorch related (obviously) but I found it a very decent introduction that helped me to breach the "what's going on and what does it look like" wall. 
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih5pt02/)
This one looks awesome. Thanks! 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih5lowo/?force-legacy-sct=1)
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih6jf9z/)
This is the CUDA series training provided to Oakland National Laboratory that is opened to the public : <https://www.olcf.ornl.gov/cuda-training-series/>
Best tutorial I’ve seen so far. There are actual cuda programming assignment that you can do after each session as well. 
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/li1kdbb/)
I could not find any video to check on that page, but I found them on vimeo:-> <https://vimeo.com/search?q=CUDA%20OLCF>.The order should be followed form the original page: <https://www.olcf.ornl.gov/cuda-training-series/>
The exercises are here: <https://github.com/olcf/cuda-training-series/tree/master/exercises>
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/li1kdbb/?force-legacy-sct=1)
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih6myk1/)
Wow this is awesome! Thanks for sharing 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih6jf9z/?force-legacy-sct=1)
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih5vz0r/)
If you already know some C++, the Nvidia [devblog](https://developer.nvidia.com/blog/even-easier-introduction-cuda/) is a great resource. Going further, [Cub](https://nvlabs.github.io/cub/) and [Cutlass](https://github.com/NVIDIA/cutlass) provide examples of efficient implementations for key operations at all hardware levels. Finally, this is more anecdotal but I always start my lectures on Cuda programming with the pictures in this [doc page](http://kernel-operations.io/keops/autodiff_gpus/what_is_a_gpu.html), to provide some intuition on the different memory layers that you can leverage to speed up a program. In any case, good luck :-) 
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih5woso/)
These are helpful. Thank you! 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih5vz0r/?force-legacy-sct=1)
• [ Promoted ](https://www.reddit.com/user/sage_uk/)
Connected data. Clear view.
View More
sage.com 
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih6j14n/)
I wrote a couple of [blog posts](https://learnopencv.com/demystifying-gpu-architectures-for-deep-learning/) about CUDA for ML practitioners. You may find it useful 
[ GOODAKDERZERSTOERER ](https://www.reddit.com/user/GOODAKDERZERSTOERER/)
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih69nj1/)
yes thats the book some of the very new stuff might be Missing but its great for getting into CuDA 
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih6a43k/)
Awesome, thanks 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih69nj1/?force-legacy-sct=1)
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ihahvef/)
Just thought I’d mention that there are alternatives like OpenCL. It prevents from being at the mercy of Nvidia, although comes at a performance penalty. 
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih5wp1l/)
I tried learning Cuda but was discouraged going forward with it because it serves no purpose for me as a developer when all I need is pytorch for the most part, where do you plan to use these skills and where else can they be used from an ML engineer perspective ? I enrolled in this one as for your question: <https://www.udemy.com/share/101Y8M3@DiU0Yxit6PHPdZPR1B_LMkAmUirg5PY5nyEwjVG-ZjAxj2p0v5oncf7CAZ9G4HMg/> and also there’s one officially by nvidia as well. 
[deleted]
• 4y ago
Comment deleted by user
1 more reply 
1 more reply 
4 more replies 
4 more replies 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih5wp1l/?force-legacy-sct=1)
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih81ww3/)
RemindMe! 3 months 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih81ww3/?force-legacy-sct=1)
• [ Promoted ](https://www.reddit.com/user/SimpleSkinUK/)
Hi Reddit! I'm Katherine, an R&D Scientist at Simple Skincare. Let's chat looking after your skin, the importance of skin barriers and much, much more! Ask Me Anything! March 17th @ 3PM GMT
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih8buyn/)
RemindMe! 1 month 
[ GOODAKDERZERSTOERER ](https://www.reddit.com/user/GOODAKDERZERSTOERER/)
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih5tnt7/)
Theres also a good book that goes in depth about the architectural stuff called programming massively parallel Computers i think Plus the official Nvidia documentation has Lots of examples to try out 
4 more replies 
4 more replies 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih5tnt7/?force-legacy-sct=1)
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih5xtjb/)
Practice puzzles: <https://github.com/srush/GPU-Puzzles>
[ treasure-robotics ](https://www.reddit.com/user/treasure-robotics/)
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih6tuos/)
This is the right answer for 99% of ML people, plus if you finish it Sasha Rush might mention you on Twitter 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih5xtjb/?force-legacy-sct=1)
[deleted]
• 4y ago
Comment deleted by user
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih67ua3/)
Thanks, though I couldn't find it. Could you share a link? 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih67ua3/?force-legacy-sct=1)
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih7atet/)
Depending on your use case, I would suggest learning Triton (<https://github.com/openai/triton>). It abstracts some of the detailed nitty-gritty lower level details of CUDA for you. 
3 more replies 
3 more replies 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih7atet/?force-legacy-sct=1)
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ih84g8k/)
[Applied GPU Programming - lecture recordings](https://www.youtube.com/playlist?list=PLPJwWVtf19Wgx_bupSDDSStSv-tOGGWRO) - Lectures from KTH Royal Institute of Technology course, delivered by Stefano Markidis 
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ihaftyn/)
Here is an awesome course from Dr. Paul Richard by university of Sheffield 
[GPU and CUDA Programming](http://paulrichmond.shef.ac.uk/teaching/COM4521/)
• [ 4y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ihb9l2d/)
NVIDIA CUDA examples, references and exposition articles. No courses or textbook would help beyond the basics, because NVIDIA keep adding new stuff each release or two. There are three basic concepts - thread synchronization, shared memory and memory coalescing which CUDA coder should know in and out of, and on top of them a lot of APIs for advanced synchronization, which are kind of added bonuses. 
[ Creative-Milk-8266 ](https://www.reddit.com/user/Creative-Milk-8266/)
• [ 3y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/iyyod4j/)
Udemy Course - CS344 <https://classroom.udacity.com/courses/cs344> This course is not supported anymore, but all videos are still available. I'm currently taking this. It's easy to follow and explained basic ideas very clearly. Good place to start. I'd like to do some CUDA projects to help me understand the concepts better. Did OP find any? 
• [ 1y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/lwm1fuf/)
Remind me! in one month 
[ PotentialDisastrous6 ](https://www.reddit.com/user/PotentialDisastrous6/)
• [ 1y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/m3pje5u/)
You guys are gems! 
[ KindWatercress5675 ](https://www.reddit.com/user/KindWatercress5675/)
• [ 1y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/mab7ynf/)
The best course if you want to understand both hardware and software<https://www.udemy.com/course/cuda-parallel-programming-on-nvidia-gpus-hw-and-sw>
• [ 1y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/mhn1l2s/)
[leetgpu.com](http://leetgpu.com)
[deleted]
• [ 1y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/ml5uo6r/)
NPTEL has a course I guess but you have to get enrolled when batch starts 
• [ 1y ago ](https://www.reddit.com/r/MachineLearning/comments/w52iev/comment/mmwv566/)
Learn, write, practice CUDA programming on LeetGPU.com, an online CUDA playground for anyone to write and execute CUDA code without needing a GPU and for free 
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of July 22, 2022 ](https://www.reddit.com/posts/2022/july-22-1/global/)
  * [ Reddit  reReddit: Top posts of July 2022 ](https://www.reddit.com/posts/2022/july/global/)
  * [ Reddit  reReddit: Top posts of 2022 ](https://www.reddit.com/posts/2022/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
