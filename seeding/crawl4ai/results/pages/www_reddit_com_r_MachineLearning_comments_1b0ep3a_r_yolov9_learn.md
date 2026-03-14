[r/MachineLearning](https://www.reddit.com/r/MachineLearning/) • 2y ago
[deleted]
#  [R] YOLOv9: Learning What You Want to Learn Using Programmable Gradient Information 
**Paper** : <https://arxiv.org/abs/2402.13616>
**Code** : <https://github.com/WongKinYiu/yolov9>
**Models** : <https://huggingface.co/merve/yolov9>
**Demo** : <https://huggingface.co/spaces/kadirnar/Yolov9>
**Colab** : <https://colab.research.google.com/github/roboflow-ai/notebooks/blob/main/notebooks/train-yolov9-object-detection-on-custom-dataset.ipynb>
**Abstract** : 
> Today's deep learning methods focus on how to design the most appropriate objective functions so that the prediction results of the model can be closest to the ground truth. Meanwhile, an appropriate architecture that can facilitate acquisition of enough information for prediction has to be designed. Existing methods ignore a fact that when input data undergoes layer-by-layer feature extraction and spatial transformation, large amount of information will be lost. This paper will delve into the important issues of data loss when data is transmitted through deep networks, namely information bottleneck and reversible functions. We proposed the concept of **programmable gradient information** (**PGI**) to cope with the various changes required by deep networks to achieve multiple objectives. PGI can provide complete input information for the target task to calculate objective function, so that reliable gradient information can be obtained to update network weights. In addition, a new lightweight network architecture -- **Generalized Efficient Layer Aggregation Network** (**GELAN**), based on gradient path planning is designed. GELAN's architecture confirms that PGI has gained superior results on lightweight models. We verified the proposed GELAN and PGI on MS COCO dataset based object detection. The results show that GELAN only uses conventional convolution operators to achieve better parameter utilization than the state-of-the-art methods developed based on depth-wise convolution. PGI can be used for variety of models from lightweight to large. It can be used to obtain complete information, so that train-from-scratch models can achieve better results than state-of-the-art models pre-trained using large datasets, the comparison results are shown in Figure 1. The source codes are at: [this https URL](https://github.com/WongKinYiu/yolov9). 
Read more 
Share 
• [ Promoted ](https://www.reddit.com/user/Vodafone_UK/)
At Vodafone, get the new Samsung Galaxy S26 Ultra and save a huge £724.
Samsung Galaxy S26 Ultra 
vodafone.co.uk 
Learn More
[ Zealousideal_Low1287 ](https://www.reddit.com/user/Zealousideal_Low1287/)
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks79y73/)
Ridiculous to call it YOLO when they’re not the authors of YOLO 
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks7o6fj/)
As far as I know, true YOLO models, with any authors continuity, have stopped at YOLOv3. 
YOLOv4 didn't even have a conference or journal publication, there is only an ArXiv preprint. Other papers, e.g. [this one (Scaled-YOLOv4)](https://openaccess.thecvf.com/content/CVPR2021/html/Wang_Scaled-YOLOv4_Scaling_Cross_Stage_Partial_Network_CVPR_2021_paper.html), from the same authors as ArXiv paper, are only citing the preprint. But at least it was written by academics. 
YOLOv5 doesn't have any publication at all, just [this Github page](https://github.com/ultralytics/yolov5). 
YOLOv6 only has [this ArXiv preprint](https://arxiv.org/abs/2209.02976), written by a huge list of [Meituan](https://en.wikipedia.org/wiki/Meituan) (Chinese corporation) emploees. No scientists in sight, no conference/journal publication. [It has been submitted to ICLR 2024](https://openreview.net/forum?id=7c3ZOKGQ6s), and was rejected by a landslide (all very confident rejects). 
YOLOv7 also [only has an ArXiv preprint](https://arxiv.org/abs/2207.02696). But it has the same first and last authors as YOLOv4 and Scaled-YOLOv4, so it has academics as authors. 
YOLOv8, like YOLOv5, doesn't have any publication at all, just [this Github page](https://github.com/ultralytics/yolov5). It is also made by the same company. 
YOLOv9, from OP's post, also [only has ArXiv preprint](https://arxiv.org/abs/2402.13616). First and last authors are the same as in YOLOv7. 
And, of course, we have the [Skynet-level YOLOv10](https://github.com/FrancescoSaverioZuppichini/yolov10). 
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks8oqsr/)
Joseph Redmon the original author, stopped development after yolov3. At that time he endorsed github user AlexeyAB and his repository to continue the darknet yolo line of models. At the time, ultralytics was a popular pytorch port of YOLOv3 and made many original contributions to the model (like mosaic augmentation) that improved performance. 
AlexeyAB published Yolov4, and within a week or two ultralytics published yolov5, but the two models were largely identical and yolov4 actually outperformed yolov5. 
During this time, user WongKinYiu significantly contributed to Yolov4 after which he would be the primary developer for the AlexeyAB line of models. 
Yolov6 authors are out of left field, though. 
Yolov4 - AlexeyAB / WongkinYiu 
Yolov5 - ultralytics 
Yolov6 - who knows 
Yolov7 - WongkinYiu / AlexeyAB 
Yolov8 - ultralytics 
Yolov9 - WongkinYiu 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks8oqsr/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks7xwg9/)
Ok, that YOLOv10 paper was hilarious. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks7xwg9/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks8rxp4/)
YoloV5 is basically YoloV3 with minor adjustments, same like how v8 is to v7. 
Personally I find it ridiculous to publish a model without a paper to justify performance metrics. 
The only reason people use ultralytics's models is because it's neatly wrapped for off-the-shelf purposes. I wouldn't let either v5 or v8 (if a paper was ever published) to pass peer review because of the lack of novelty. 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks7o6fj/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks7abf8/)
Everybody and their dog has been making YOLOs for quite awhile now, pjreddie hasn’t been involved for ages 
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks7l185/)
But at least he was involved when it transitioned to Alexey afaik. 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks7abf8/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks7lp4k/)
Waiting for Apple making YOLO X. 
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks7np0f/)
YoloX already exist x x 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks7lp4k/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks79y73/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks7s697/)
That abstract is a mess. 
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ksabnop/)
Has anyone here actually understood what GELAN and PGI is? For me it seems like PGI is some sort of auxiliary dummy path that somehow preserves full gradient info, and GELAN is some kind of network block abstraction modification, but what do they actually mean in practice and how do they work? 
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/kscn1q5/)
Yeah they reinvented ResNets. 
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/kv4az46/)
I find it funny that Yolo Architectures didn't really use ResNets up until this point. The performance gain is kinda obvious considering they have less problems with vanishing gradients. 
[ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/kscn1q5/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ksabnop/?force-legacy-sct=1)
[ Tight-Lettuce7980 ](https://www.reddit.com/user/Tight-Lettuce7980/)
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks975lj/)
Has anyone actually been able to run the first few models? I looked at the github a while back and people said there were errors and it would be better to just use the newest model. 
• [ Promoted ](https://www.reddit.com/user/Snapdragon_UK/)
For creatives who actually get out and do stuff: PCs powered by Snapdragon. Your desk is now optional.
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks7v8sb/)
Do you think this we'll see a tune to do face recognition, and if it's even any better than yolo3 (or subsequent versions). 
[deleted]
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks9lz30/)
The question is whether YOLOv9 achieves a higher mAP due to the changes mentioned in the paper or due to the other changes in the code. For example, YOLOv9 does not use simOTA anymore (like YOLOv7) but Task Alignment Learning (TAL). 
• [ 2y ago ](https://www.reddit.com/r/MachineLearning/comments/1b0ep3a/comment/ks8emhr/)
Could anyone elaborate on how Figure 2 was made? I get that they randomly initialized models and did forward passes with an image. But what exactly are they plotting? 
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of February 26, 2024 ](https://www.reddit.com/posts/2024/february-26-1/global/)
  * [ Reddit  reReddit: Top posts of February 2024 ](https://www.reddit.com/posts/2024/february/global/)
  * [ Reddit  reReddit: Top posts of 2024 ](https://www.reddit.com/posts/2024/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
