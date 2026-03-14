Erik Knobl
[Twitter](https://readmedium.com/#twitter)[Facebook](https://readmedium.com/#facebook)[LinkedIn](https://readmedium.com/#linkedin)[WeChat](https://readmedium.com/#wechat)[Qzone](https://readmedium.com/#qzone)
Summary
The author, a designer, has leveraged Generative AI tools like ChatGPT, Claude AI, Midjourney, Runway Gen-3, and others to create a YouTube series set in a cyberpunk universe, detailing the creative process and challenges faced, particularly in character consistency and animation.
Abstract
The website content outlines the author's innovative approach to storytelling by using AI-driven tools to produce a video series. The author details the process starting from conceptualizing the script with AI, generating consistent aesthetic images with Midjourney, and animating these images to create a cohesive narrative. The article emphasizes the experimental nature of the workflow, which includes using AI for scriptwriting, image generation, voice creation, and video editing, while also acknowledging persistent challenges such as character consistency and animation limitations. Despite these hurdles, the author has managed to produce a gritty sci-fi story of a lone hitman in a dystopian, cyberpunk setting. The project serves as a testament to the evolving capabilities of AI in filmmaking, and the author invites feedback and discussion on the process, while also promoting a newsletter focused on creative AI tools.
Opinions
  * The author believes that AI tools like ChatGPT, Claude AI, Midjourney, and Runway Gen-3 have evolved sufficiently to produce decent video stories, emphasizing the importance of hands-on experience in understanding their potential.
  * They note the experimental nature of using AI for video production, suggesting that the workflow will continue to evolve with each unique project.
  * The author recognizes the significance of maintaining a consistent aesthetic and narrative throughout the video, achieved by using a specific sref parameter in Midjourney for image generation.
  * A major challenge identified is character consistency, which the author addresses by using a workaround with a celebrity reference for the main character and suggests not to stress over this issue given the current lack of a perfect solution.
  * The author shares a personal revelation regarding the blending of srefs for varied clothing styles, indicating a learning curve and adaptability in the use of AI tools.
  * They also express satisfaction with the results achieved, despite some limitations, and encourages the use of AI-generated voices and sounds to enhance the storytelling experience.
  * The author is optimistic about the potential of AI in filmmaking and eager to share knowledge and insights through their newsletter, "Creative AI."


[Use the OpenAI o1 models for free at OpenAI01.net (10 times a day for free)!](https://OpenAI01.net "PS2 Filter AI")
# I created a YouTube series using Midjourney and Runway Gen-3: Here’s what I learned
## Exploring new workflows for Video with Generative AI
Lately, I’ve been diving into the world of storytelling with AI. I believe these tools have evolved enough to produce decent video stories, and the only way to truly find out is by doing it myself.
# Tools Used:
  * **Concept and Script:** ChatGPT and Claude AI
  * **Base Images, Casting, and Concept Design:** Midjourney and Freepik
  * **Video Generation:** Runway Gen-3, LumaLabs, Kling
  * **Voices and Sound Effects:** ElevenLabs, Hedra Labs, and Capcut
  * **Editing:** Capcut
  * **Graphic Design:** Figma


Since these tools are still relatively new, the workflow is experimental, and I expect it will evolve with each unique project.
Here’s a look at the process I followed for this one.
# Concept and Script
As a designer, I often draw inspiration from single images. While working on [_The Big Book of Midjourney Reference Styles (sref codes)_](https://erikknobl.gumroad.com/l/thebigbookofmidjourneyreferencestyles), I became captivated by sref 3456119169:
I wanted to create a gritty story of a lone sci-fi headhunter, using that reference as the mood. With those elements in mind, I turned to ChatGPT and Claude AI to brainstorm ideas with the following prompt:
> Futuristic setting in a human colony in another planet. A hitman goes to a bar to collect some payments. He ends up with a task to hunt somebody. Suggest 5 possible ideas for a short video story in a grim, cyberpunk setting
After reviewing the responses, I extracted the ideas I liked and refined the story further with this prompt:
> Make a script of the following plot: The hitman enters the bar to collect his payment, only to find out that the person who owes him has been killed by a notorious droid criminal who has been hiding within the colony’s slums, and and also taken the payment. The hitman decides to hunt this criminal.
Now, with a basic draft of the script, I used it as a guide for generating images with Midjourney and Freepik.
# Generating Images
To maintain a consistent aesthetic throughout the video, I used the sref parameter in Midjourney, specifically sref 3456119169. This provided an orange, misty mood across all the images. Here are some examples of the generated images:
> Cinematic Still, aerial view of futuristic city with skyscrapers, remove person, dystopian, cyberpunk — ar 16:9 — sref 3456119169 — p — stylize 1000 — v 6
> Cinematic Still, Futuristic vehicle in an alley in a city with skyscrapers, dystopian, cyberpunk — ar 16:9 — sref 3456119169 — v 6 — stylize 1000 — p
> Cinematic Still, Futuristic bar sign in an alley, city with skyscrapers in the background, dystopian, cyberpunk — ar 16:9 — sref 3456119169 — v 6 — stylize 1000 — p
Some of the images generated with this sref were a bit rough, which could be problematic when animating.
Upscaling with Freepik was necessary to improve the quality.
# Animating the Images
The next step involved animating these images using Runway, LumaLabs, and Kling. Adding a brief prompt describing the action required helped bring the scenes to life:
> Prompt: Vehicle flies away
> Prompt: Person walking
LumaLabs’ image-blending feature proved useful, allowing me to experiment with transitioning between scenes. The results added depth to the structure.
The basic structure was taking shape.
But here comes **THE BIG BAD PROBLEM** of AI Films:
DumDumDumDuuuuuum.
Character Consistency.
This remains a significant challenge in AI filmmaking, and it’s far from being fully resolved. For this project, I used a workaround that produced satisfactory results.
# Characters
I had a clear vision for my character’s appearance, based on a celebrity reference. My initial prompt was:
> Cinematic still, frontal shot, portrait Bruce Willis with a futuristic trenchcoat walking in an alley, dystopian, cyberpunk — ar 16:9 — sref 3456119169 — p — stylize 1000 — v 6
Yup. He works.
This worked well enough, so I used this as a base template for all the character scenes, only changing the scene description and adding the -cref parameter with the image URL for reinforcement.
While not perfect, it was good enough for the project.
**Advice:** Don’t stress over this issue. There’s currently no perfect solution.
For supporting actors, another trick is to generate a main portrait of the character and use Midjourney’s editor to change the surroundings. This adds just enough variety for the scene, making the characters different enough once animated.
> **Side Note:** One limitation I encountered with this sref was the inability to change a character’s clothing to a futuristic style. I realized later that blending the sref with another featuring futuristic elements might have solved this issue.
Once animated, they will be different enough.
> Side Note: Here I found a limit of this Midjourney sref. No matter how much I changed the prompt, I could get MJ to dress her with futuristic clothing. (As I was writing this, it ocurred to me I could have blended the sref with another with a futuristic elements. Oh, well)
# Voices and Sounds
There are several options for adding voice and sound to your characters:
  * **ElevenLabs:** Generate voices with Text to Voice.
  * **Runway and Hedra Labs:** Lip-sync features allow you to add voices to images.
  * **Capcut:** Offers voice generation but no lip-sync feature.


Additionally, sound effects elevate your video. Both ElevenLabs and Capcut provide options to generate or add them.
# Uploading to YouTube
YouTube is the best platform to share your creations and build an audience. I recommend creating and sharing your channel.
For thumbnails, I used the free version of Figma. It offers a range of fantastic fonts. Here are a few thumbnails I designed:
Which one do you prefer?
This is the final result. I’d love to hear your feedback or answer any questions about the process!
_Thanks for reading!_
I’m launching my newsletter about AI creative tools like Midjourney, Leonardo AI, Runway, Pika, GPT, and others. If you would like to be in touch, please subscribe: [Creative AI](https://creativeai.beehiiv.com/)
## [Creative AI News and Tips for Midjourney, Runway and other creative tools for AI Art creativeai.beehiiv.com ](https://creativeai.beehiiv.com/)
> Hi👋 I’m [Erik](https://twitter.com/Erik_Knobl). If you liked this story, clap and follow me here on Medium. I‘m sharing my learnings in my newsletter [Creative AI.](https://creativeai.beehiiv.com/) It would be amazing if you could join me on this journey.
Midjourney
Runway
Generative Ai Tools
Ai Video
YouTube
Recommended from ReadMedium
Andrew Best
[New KILLER ChatGPT Prompt — The “Playoff Method”Super powerful prompt for ChatGPT — 01 Preview](https://readmedium.com/new-killer-chatgpt-prompt-the-playoff-method-0ee759bd917c)
5 min read
Afghan Bitani
[How to Make ChatGPT Write Like a Human: (7-Step Prompt) to Make Your Content Come Alive!I tried a total of 58 different prompts in my experiments, Out of these, 7 truly stand out.](https://readmedium.com/how-to-make-chatgpt-write-like-a-human-7-step-prompt-to-make-your-content-come-alive-98e0cd51894f)
7 min read
Erik Knobl
[Steal this process to mine SREF codes in MidjourneySharing my fun-filled process to get SREF Codes](https://readmedium.com/steal-this-process-to-mine-sref-codes-in-midjourney-9b386095daec)
3 min read
Vivek Naskar
[How FLUX.1 Is Disrupting The Billion Dollar AI Image Generator IndustryNow you can generate hyperrealistic industry grade AI images for free.](https://readmedium.com/how-flux-1-is-disrupting-the-billion-dollar-ai-image-generator-industry-a710abddbeb6)
9 min read
Awais
[I Sold AI Art for 30 Days And Here’s My ProfitAnd Results Were Unexpected](https://readmedium.com/i-tried-to-sell-ai-art-for-30-days-and-this-happened-6ef9002d12be)
5 min read
Vrilya Jarac
[I Created an Impressive AI Fashion Music Video With Runway Gen-3New AI Video Tools Deliver Amazing Realism](https://readmedium.com/i-created-an-impressive-ai-fashion-music-video-with-runway-gen-3-2e158eeaf235)
3 min read
Copy link
✓
Thanks for sharing!
