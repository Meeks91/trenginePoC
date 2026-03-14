• 2y ago
[WolframRavenwolf](https://www.reddit.com/user/WolframRavenwolf/)
#  🐺🐦‍⬛ LLM Comparison/Test: Brand new models for 2024 (Dolphin 2.6/2.7 Mistral/Mixtral/Phi-2, Sonya, TinyLlama) 
Happy New Year! 2023 was _the_ year of local and (semi-)open LLMs, the beginning of a new AI era, and software and models are evolving at an ever increasing pace. 
Even over the turn of the year countless brilliant people have blessed us with their contributions, including a batch of brand new model releases in 2024, so here I am testing them already: 
## New Models tested:
  * [**dolphin-2.6-mistral-7b-dpo**](https://huggingface.co/cognitivecomputations/dolphin-2.6-mistral-7b-dpo)
  * _**Update 2024-01-02:**_ [**dolphin-2.6-mistral-7b-dpo-laser**](https://huggingface.co/cognitivecomputations/dolphin-2.6-mistral-7b-dpo-laser)
  * [**dolphin-2.7-mixtral-8x7b**](https://huggingface.co/cognitivecomputations/dolphin-2.7-mixtral-8x7b)
  * [**dolphin-2_6-phi-2**](https://huggingface.co/cognitivecomputations/dolphin-2_6-phi-2)
  * [**sonya-medium-x8-MoE**](https://huggingface.co/dillfrescott/sonya-medium-x8-MoE)
  * [**TinyLlama-1.1B-Chat-v1.0**](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)


## Testing methodology
  * **4 German data protection trainings:**
    * I run models through **4** professional German online data protection trainings/exams - the same that our employees have to pass as well. 
    * The test data and questions as well as all instructions are in German while the character card is in English. This **tests translation capabilities and cross-language understanding**. 
    * Before giving the information, I instruct the model (in German): _I'll give you some information. Take note of this, but only answer with "OK" as confirmation of your acknowledgment, nothing else._ This **tests instruction understanding and following capabilities**. 
    * After giving all the information about a topic, I give the model the exam question. It's a multiple choice (A/B/C) question, where the last one is the same as the first but with changed order and letters (X/Y/Z). Each test has 4-6 exam questions, for a total of **18** multiple choice questions. 
    * If the model gives a single letter response, I ask it to answer with more than just a single letter - and vice versa. If it fails to do so, I note that, but it doesn't affect its score as long as the initial answer is correct. 
    * I rank models according to how many correct answers they give, primarily after being given the curriculum information beforehand, and secondarily (as a tie-breaker) after answering blind without being given the information beforehand. 
    * All tests are separate units, context is cleared in between, there's no memory/state kept between sessions. 
  * [SillyTavern](https://github.com/SillyTavern/SillyTavern) frontend 
  * [oobabooga's text-generation-webui](https://github.com/oobabooga/text-generation-webui) backend (for HF models) 
  * **Deterministic** generation settings preset (to eliminate as many random factors as possible and allow for meaningful model comparisons) 
  * Official prompt format as noted 


## Detailed Test Reports
And here are the detailed notes, the basis of my ranking, and also additional comments and observations: 
  * [**dolphin-2.6-mistral-7b-dpo**](https://huggingface.co/cognitivecomputations/dolphin-2.6-mistral-7b-dpo) 16K context, ChatML format: 
    * ❌ Gave correct answers to only **1+4+4+6=15/18** multiple choice questions! Just the questions, no previous information, gave correct answers: **4+2+2+4=12/18**
    * ❌ Did NOT follow instructions to acknowledge data input with "OK". 
    * ➖ Did NOT follow instructions to answer with just a single letter or more than just a single letter. 


The DPO version did much better than the one without! That's what we hoped for and expected. The unexpected thing here is that it did better than all the other models I tested this time. Is the DPO tuning making this so much better or do the other models have some bugs or flaws still? 
  * [**dolphin-2.7-mixtral-8x7b**](https://huggingface.co/cognitivecomputations/dolphin-2.7-mixtral-8x7b) 4-bit, 32K context, ChatML format: 
    * ❌ Gave correct answers to only **4+2+4+5=15/18** multiple choice questions! Just the questions, no previous information, gave correct answers: **4+2+0+0=6/18**
    * ❌ Did NOT follow instructions to acknowledge data input with "OK". 
    * ➖ Did NOT follow instructions to answer with just a single letter or more than just a single letter. 
    * ❌ Didn't answer multiple times and said instead: "Hello! How can I help you?" or (wrongly) claimed: "all options are partially correct" 


Strange, but the 7B 2.6 DPO version of Dolphin did better in my tests than the 8x7B 2.7 MoE version. The problem of sometimes not answering at all, especially during the blind run, also happened with dolphin-2.6-mistral-7b and dolphin-2.6-mixtral-8x7b in my previous tests. Only the DPO version didn't exhibit that problem, and the previously tested dolphin-2.5-mixtral-8x7b, which for some reason is still the best MoE Dolphin in all my tests. 
  * _**Update 2024-01-02:**_ [**dolphin-2.6-mistral-7b-dpo-laser**](https://huggingface.co/cognitivecomputations/dolphin-2.6-mistral-7b-dpo-laser) 16K context, ChatML format: 
    * ❌ Gave correct answers to only **3+3+0+6=12/18** multiple choice questions! Just the questions, no previous information, gave correct answers: **4+3+2+4=13/18**
    * ❌ Did NOT follow instructions to acknowledge data input with "OK". 
    * ➖ Did NOT follow instructions to answer with just a single letter or more than just a single letter. 
    * ❌ Didn't answer multiple times and instead (wrongly) claimed that all options were partially correct. 


Unfortunately it looks like not everything is better with lasers. If Dolphin wouldn't sometimes fail to answer properly at all, it would score much higher, as shown by the dolphin-2.6-mistral-7b-dpo which didn't blunder like other variants. 
  * [**sonya-medium-x8-MoE**](https://huggingface.co/dillfrescott/sonya-medium-x8-MoE) 4-bit, 8K context, Alpaca format: 
    * ❌ Gave correct answers to only **3+2+2+5=12/18** multiple choice questions! Just the questions, no previous information, gave correct answers: **3+3+1+3=10/18**
    * ❌ Did NOT follow instructions to acknowledge data input with "OK". 
    * ➖ Did NOT follow instructions to answer with just a single letter or more than just a single letter. 
    * ❗ Oozes personality, probably a little too much over the top for an assistant role, but looks like a great match for a roleplay companion. 


Not bad, but I expected much more. Probably needs a finalization finetune [as discussed in the release thread](https://www.reddit.com/r/LocalLLaMA/comments/18vpxf7/i_present_my_magnum_opus_llm_merge_of_2023/kfsyzlh/), so I'm hoping for an update. 
  * [**dolphin-2_6-phi-2**](https://huggingface.co/cognitivecomputations/dolphin-2_6-phi-2) 2K context, ChatML format: 
    * ❌ Gave correct answers to **NONE** of the 18 multiple choice questions! Just the questions, no previous information, gave correct answers: **0/18**
    * ❌ Did NOT follow instructions to acknowledge data input with "OK". 
    * ➖ Did NOT follow instructions to answer with just a single letter or more than just a single letter. 


Clearly not up to the tasks I'm testing, and it didn't feel like any modern LLM at all. I'm sure these little <3B models have their uses, but for the use cases I have and test for, they're unfortunately completely unsuitable. 
  * [**TinyLlama-1.1B-Chat-v1.0**](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) 2K context, Zephyr format: 
    * ❌ Gave correct answers to **NONE** of the 18 multiple choice questions! Just the questions, no previous information, gave correct answers: **0/18**
    * ❌ Did NOT follow instructions to acknowledge data input with "OK". 
    * ➖ Did NOT follow instructions to answer with just a single letter or more than just a single letter. 


Same as the Phi-2 model, this one is even smaller, so same outcome. In LLM land, size does matter, too. 
## Updated Rankings
This is my objective ranking of these models based on measuring factually correct answers, instruction understanding and following, and multilingual abilities: 
Rank  |  Model  |  Size  |  Format  |  Quant  |  Context  |  Prompt  |  1st Score  |  2nd Score   
---|---|---|---|---|---|---|---|---  
GPT-4  |  GPT-4  |  18/18 ✓  |  18/18 ✓   
120B  |  GGUF  |  Q2_K  |  Vicuna 1.1  |  18/18 ✓  |  18/18 ✓   
120B  |  GGUF  |  Q2_K  |  Synthia  |  18/18 ✓  |  18/18 ✓   
[Nous-Capybara-34B-GGUF](https://huggingface.co/TheBloke/Nous-Capybara-34B-GGUF) |  GGUF  |  Q4_0  |  Vicuna 1.1  |  18/18 ✓  |  18/18 ✓   
120B  |  EXL2  |  3.0bpw  |  Alpaca  |  18/18 ✓  |  18/18 ✓   
GGUF  |  Q4_0  |  Vicuna 1.1  |  18/18 ✓  |  17/18   
[chronos007-70B-GGUF](https://huggingface.co/TheBloke/chronos007-70B-GGUF) |  GGUF  |  Q4_0  |  Alpaca  |  18/18 ✓  |  16/18   
[SynthIA-70B-v1.5-GGUF](https://huggingface.co/migtissera/SynthIA-70B-v1.5-GGUF) |  GGUF  |  Q4_0  |  SynthIA  |  18/18 ✓  |  16/18   
[Mixtral-8x7B-Instruct-v0.1](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1) |  8x7B  |  4-bit  |  ~~32K~~ 4K  |  Mixtral  |  18/18 ✓  |  16/18   
[dolphin-2_2-yi-34b-GGUF](https://huggingface.co/TheBloke/dolphin-2_2-yi-34b-GGUF) |  GGUF  |  Q4_0  |  ChatML  |  18/18 ✓  |  15/18   
GGUF  |  Q4_0  |  Vicuna 1.1  |  18/18 ✓  |  14/18   
GGUF  |  Q4_0  |  Alpaca  |  18/18 ✓  |  14/18   
[Euryale-1.3-L2-70B-GGUF](https://huggingface.co/TheBloke/Euryale-1.3-L2-70B-GGUF) |  GGUF  |  Q4_0  |  Alpaca  |  18/18 ✓  |  14/18   
[sophosynthesis-70b-v1](https://huggingface.co/sophosympatheia/sophosynthesis-70b-v1) |  EXL2  |  4.85bpw  |  Vicuna 1.1  |  18/18 ✓  |  13/18   
GGUF  |  Q4_0  |  Alpaca  |  18/18 ✓  |  12/18   
[Samantha-1.11-70B-GGUF](https://huggingface.co/TheBloke/Samantha-1.11-70B-GGUF) |  GGUF  |  Q4_0  |  Vicuna 1.1  |  18/18 ✓  |  10/18   
[Airoboros-L2-70B-3.1.2-GGUF](https://huggingface.co/TheBloke/Airoboros-L2-70B-3.1.2-GGUF) |  GGUF  |  Q4_K_M  |  Llama 2 Chat  |  17/18  |  16/18   
[Rogue-Rose-103b-v0.2](https://huggingface.co/sophosympatheia/Rogue-Rose-103b-v0.2) |  103B  |  EXL2  |  3.2bpw  |  Rogue Rose  |  17/18  |  14/18   
GPT-3.5 Turbo Instruct  |  GPT-3.5  |  17/18  |  11/18   
[Synthia-MoE-v3-Mixtral-8x7B](https://huggingface.co/migtissera/Synthia-MoE-v3-Mixtral-8x7B) |  8x7B  |  4-bit  |  ~~32K~~ 4K  |  ~~Synthia~~ Llama 2 Chat  |  17/18  |  9/18   
[dolphin-2.2-70B-GGUF](https://huggingface.co/TheBloke/dolphin-2.2-70B-GGUF) |  GGUF  |  Q4_0  |  ChatML  |  16/18  |  14/18   
[mistral-ft-optimized-1218](https://huggingface.co/OpenPipe/mistral-ft-optimized-1218) |  ~~32K~~ 8K  |  Alpaca  |  16/18  |  13/18   
[OpenHermes-2.5-Mistral-7B](https://huggingface.co/teknium/OpenHermes-2.5-Mistral-7B) |  ~~32K~~ 8K  |  ChatML  |  16/18  |  13/18   
[Mistral-7B-Instruct-v0.2](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2) |  Mistral  |  16/18  |  12/18   
[DeciLM-7B-instruct](https://huggingface.co/Deci/DeciLM-7B-instruct) |  Mistral  |  16/18  |  11/18   
~~32K~~ 8K  |  Alpaca  |  16/18  |  11/18   
[SauerkrautLM-7b-HerO](https://huggingface.co/VAGOsolutions/SauerkrautLM-7b-HerO) |  ~~32K~~ 8K  |  ChatML  |  16/18  |  11/18   
[mistral-ft-optimized-1227](https://huggingface.co/OpenPipe/mistral-ft-optimized-1227) |  ~~32K~~ 8K  |  Alpaca  |  15/18  |  14/18   
GPT-3.5 Turbo  |  GPT-3.5  |  15/18  |  14/18   
[dolphin-2.5-mixtral-8x7b](https://huggingface.co/ehartford/dolphin-2.5-mixtral-8x7b) |  8x7B  |  4-bit  |  ~~32K~~ 4K  |  ChatML  |  15/18  |  13/18   
[Starling-LM-7B-alpha](https://huggingface.co/berkeley-nest/Starling-LM-7B-alpha) |  OpenChat (GPT4 Correct)  |  15/18  |  13/18   
25 🆕  |  [dolphin-2.6-mistral-7b-dpo](https://huggingface.co/cognitivecomputations/dolphin-2.6-mistral-7b-dpo) |  ChatML  |  15/18  |  12/18   
OpenChat (GPT4 Correct)  |  15/18  |  7/18   
27 🆕  |  [dolphin-2.7-mixtral-8x7b](https://huggingface.co/cognitivecomputations/dolphin-2.7-mixtral-8x7b) |  8x7B  |  4-bit  |  ChatML  |  15/18  |  6/18   
[dolphin-2.6-mixtral-8x7b](https://huggingface.co/cognitivecomputations/dolphin-2.6-mixtral-8x7b) |  8x7B  |  4-bit  |  ~~32K~~ 16K  |  ChatML  |  14/18  |  12/18   
[MixtralRPChat-ZLoss](https://huggingface.co/chargoddard/MixtralRPChat-ZLoss) |  8x7B  |  4-bit  |  ~~32K~~ 8K  |  CharGoddard  |  14/18  |  10/18   
[OpenHermes-2.5-neural-chat-v3-3-openchat-3.5-1210-Slerp](https://huggingface.co/Weyaxi/OpenHermes-2.5-neural-chat-v3-3-openchat-3.5-1210-Slerp) |  ~~32K~~ 8K  |  OpenChat (GPT4 Correct)  |  13/18  |  13/18   
31 🆕  |  [dolphin-2.6-mistral-7b-dpo-laser](https://huggingface.co/cognitivecomputations/dolphin-2.6-mistral-7b-dpo-laser) |  ChatML  |  12/18  |  13/18   
32 🆕  |  [sonya-medium-x8-MoE](https://huggingface.co/dillfrescott/sonya-medium-x8-MoE) |  8x11B  |  4-bit  |  Alpaca  |  12/18  |  10/18   
[dolphin-2.6-mistral-7b](https://huggingface.co/cognitivecomputations/dolphin-2.6-mistral-7b) |  ~~32K~~ 8K  |  ChatML  |  10/18  |  10/18   
[SauerkrautLM-70B-v1-GGUF](https://huggingface.co/TheBloke/SauerkrautLM-70B-v1-GGUF) |  GGUF  |  Q4_0  |  Llama 2 Chat  |  9/18  |  15/18   
35 🆕  |  2.7B  |  ChatML  |  0/18 ✗  |  0/18 ✗   
35 🆕  |  [TinyLlama-1.1B-Chat-v1.0](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) |  1.1B  |  Zephyr  |  0/18 ✗  |  0/18 ✗   
  * 1st Score = Correct answers to multiple choice questions (after being given curriculum information) 
  * 2nd Score = Correct answers to multiple choice questions (without being given curriculum information beforehand) 
  * OK = Followed instructions to acknowledge all data input with just "OK" consistently 
  * +/- = Followed instructions to answer with just a single letter or more than just a single letter 


## Upcoming/Planned Tests
Next on my ~~to-do~~ to-test list are still the 10B and updated 34B models. Just wanted to put this review in between so that I could be as up to date as possible when it comes to the brand new releases. 
Here's a list of my previous model tests and comparisons or other related posts: 
  * [LLM Comparison/Test: Ranking updated with 10 new models (the best 7Bs)!](https://www.reddit.com/r/LocalLLaMA/comments/18u122l/llm_comparisontest_ranking_updated_with_10_new/)
  * [LLM Prompt Format Comparison/Test: Mixtral 8x7B Instruct with **17** different instruct templates](https://www.reddit.com/r/LocalLLaMA/comments/18ljvxb/llm_prompt_format_comparisontest_mixtral_8x7b/)
  * [LLM Comparison/Test: Mixtral-8x7B, Mistral, DeciLM, Synthia-MoE](https://www.reddit.com/r/LocalLLaMA/comments/18gz54r/llm_comparisontest_mixtral8x7b_mistral_decilm/) Winner: Mixtral-8x7B-Instruct-v0.1 
  * [Updated LLM Comparison/Test with new RP model: Rogue Rose 103B](https://www.reddit.com/r/LocalLLaMA/comments/18ft8f5/updated_llm_comparisontest_with_new_rp_model/)
  * [**Big** LLM Comparison/Test: 3x 120B, 12x 70B, 2x 34B, GPT-4/3.5](https://www.reddit.com/r/LocalLLaMA/comments/185ff51/big_llm_comparisontest_3x_120b_12x_70b_2x_34b/) Winner: Goliath 120B 
  * [LLM Format Comparison/Benchmark: 70B GGUF vs. EXL2 (and AWQ)](https://www.reddit.com/r/LocalLLaMA/comments/17w57eu/llm_format_comparisonbenchmark_70b_gguf_vs_exl2/)
  * [LLM Comparison/Test: 2x 34B Yi (Dolphin, Nous Capybara) vs. 12x 70B, 120B, ChatGPT/GPT-4](https://www.reddit.com/r/LocalLLaMA/comments/17vcr9d/llm_comparisontest_2x_34b_yi_dolphin_nous/) Winners: goliath-120b-GGUF, Nous-Capybara-34B-GGUF 
  * [LLM Comparison/Test: Mistral 7B Updates (OpenHermes 2.5, OpenChat 3.5, Nous Capybara 1.9)](https://www.reddit.com/r/LocalLLaMA/comments/17p0gut/llm_comparisontest_mistral_7b_updates_openhermes/) Winners: OpenHermes-2.5-Mistral-7B, openchat_3.5, Nous-Capybara-7B-V1.9 
  * [Huge LLM Comparison/Test: Part II (7B-20B) Roleplay Tests](https://www.reddit.com/r/LocalLLaMA/comments/17kpyd2/huge_llm_comparisontest_part_ii_7b20b_roleplay/) Winners: OpenHermes-2-Mistral-7B, LLaMA2-13B-Tiefighter 
  * [Huge LLM Comparison/Test: 39 models tested (7B-70B + ChatGPT/GPT-4)](https://www.reddit.com/r/LocalLLaMA/comments/17fhp9k/huge_llm_comparisontest_39_models_tested_7b70b/)
  * [My current favorite new LLMs: SynthIA v1.5 and Tiefighter!](https://www.reddit.com/r/LocalLLaMA/comments/17e446l/my_current_favorite_new_llms_synthia_v15_and/)
  * [Mistral LLM Comparison/Test: Instruct, OpenOrca, Dolphin, Zephyr and more...](https://www.reddit.com/r/LocalLLaMA/comments/178nf6i/mistral_llm_comparisontest_instruct_openorca/)
  * [LLM Pro/Serious Use Comparison/Test: From 7B to 70B vs. ChatGPT!](https://www.reddit.com/r/LocalLLaMA/comments/172ai2j/llm_proserious_use_comparisontest_from_7b_to_70b/) Winner: Synthia-70B-v1.2b 
  * [LLM Chat/RP Comparison/Test: Dolphin-Mistral, Mistral-OpenOrca, Synthia 7B](https://www.reddit.com/r/LocalLLaMA/comments/16z3goq/llm_chatrp_comparisontest_dolphinmistral/) Winner: Mistral-7B-OpenOrca 
  * [LLM Chat/RP Comparison/Test: Mistral 7B Base + Instruct](https://www.reddit.com/r/LocalLLaMA/comments/16twtfn/llm_chatrp_comparisontest_mistral_7b_base_instruct/)
  * [LLM Chat/RP Comparison/Test (Euryale, FashionGPT, MXLewd, Synthia, Xwin)](https://www.reddit.com/r/LocalLLaMA/comments/16r7ol2/llm_chatrp_comparisontest_euryale_fashiongpt/) Winner: Xwin-LM-70B-V0.1 
  * [New Model Comparison/Test (Part 2 of 2: 7 models tested, 70B+180B)](https://www.reddit.com/r/LocalLLaMA/comments/16l8enh/new_model_comparisontest_part_2_of_2_7_models/) Winners: Nous-Hermes-Llama2-70B, Synthia-70B-v1.2b 
  * [New Model Comparison/Test (Part 1 of 2: 15 models tested, 13B+34B)](https://www.reddit.com/r/LocalLLaMA/comments/16kecsf/new_model_comparisontest_part_1_of_2_15_models/) Winner: Mythalion-13B 
  * [New Model RP Comparison/Test (7 models tested)](https://www.reddit.com/r/LocalLLaMA/comments/15ogc60/new_model_rp_comparisontest_7_models_tested/) Winners: MythoMax-L2-13B, vicuna-13B-v1.5-16K 
  * [Big Model Comparison/Test (13 models tested)](https://www.reddit.com/r/LocalLLaMA/comments/15lihmq/big_model_comparisontest_13_models_tested/) Winner: Nous-Hermes-Llama2 
  * [SillyTavern's Roleplay preset vs. model-specific prompt format](https://www.reddit.com/r/LocalLLaMA/comments/15mu7um/sillytaverns_roleplay_preset_vs_modelspecific/)


[My Ko-fi page](https://ko-fi.com/wolframravenwolf) if you'd like to tip me to say thanks or request specific models to be tested with priority. Also consider tipping your favorite model creators, quantizers, or frontend/backend devs if you can afford to do so. They deserve it! 
Read more 
Share 
• [ Promoted ](https://www.reddit.com/user/Use-Paragon/)
Users will never stop asking for more integrations, but integrations costs months of engineering (API research, building auth, error handling etc.). 29% of B2B SaaS engineering teams use an embedded iPaaS - to save 70% of the engineering, but should you? Read the detailed build vs. buy comparison.
Learn More
useparagon.com 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwh3ba/)
So [Nous-Capybara-34B-GGUF](https://huggingface.co/TheBloke/Nous-Capybara-34B-GGUF) is so strong? 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwocs9/)
I can verify Nous-Capybara 34B has been doing the best for me in personal tests for the last month or so also. Beats ChatGPT 3.5 and has good context length. ✅ 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwocs9/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwhz4b/)
Yeah, that came as a real surprise, a mere 34B doing that well. Some test results are surprising me a lot, but it is what it is. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwj6zp/)
will you develop more tasks/questions for models this year? :) 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwj6zp/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfxptdy/)
I think some of the 34b are very slept on and better than people think (the new 34b hermes model seems interesting, but was only okay in my testing). That said, as far as MOE models go, the only good ones I've tried are solarc-moe <https://huggingface.co/TheBloke/SOLARC-MOE-10.7Bx4-GGUF>, which is ironic cause I've disliked most of the solar models I've tried, and undi's 4x7b rp moe <https://huggingface.co/Undi95/Mixtral-4x7B-DPO-RPChat?not-for-all-audiences=true>. I still think causallm 14b dpo is pretty underrated for its size <https://huggingface.co/CausalLM/14B-DPO-alpha>. 
2 more replies 
2 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfxptdy/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwqge2/)
Funny considering that yi-34b according to the team that made it was trained only on English and Chinese, no other languages at all. It's funny how you can train on entire Wikipedias in multiple languages unknowingly if you aren't careful and you operate on that scale. 
4 more replies 
4 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwqge2/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwhz4b/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfyax6s/)
Can confirm. 
Also Moose's Yi 200k tunes. 
Yi is fucking OP right now, wild that people don't talk about it more, but I guess you do need a 24gb card to really use it and that's pretty rare. 
Also if you think the GGUF is strong wooo lawdy the exl2 is NICE. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfyax6s/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwh3ba/?force-legacy-sct=1)
[ Cold-Celebration-812 ](https://www.reddit.com/user/Cold-Celebration-812/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfx3l2l/)
NousResearch recently released the Nous-Hermes-2-Yi-34B, is this model better than the Nous-Capybara-34B? Have you ever tested yi-34b-chat? 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfy8brr/)
Those will be part of the upcoming 34B tests - hopefully next post... 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfy8brr/?force-legacy-sct=1) 1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfx3l2l/?force-legacy-sct=1)
[deleted]
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwvhfm/)
I am always excited when I see a new post from you. Benchmarks are now meaningless because of contamination. This is the kind of testing we need. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwvhfm/?force-legacy-sct=1)
• [ Promoted ](https://www.reddit.com/user/cdata_software/)
Free e-book for product leaders: How to pivot from conventional data pipelines to adaptive architectures that actually support AI at scale.
Learn More
cdata.com 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwttvt/)
Are there any comparisons/tests list like this for just English? Would be interesting to see if the answers improve if you avoid languages other than English. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwttvt/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwgkvz/)
Funnily enough I really like dolphin-2.6-mistral-7b. It performs really well for me and the 16k context size is perfect for me. 
I tried the DPO version with literally exactly the same settings and it bizarrely kept getting the characters names from my cards all mixed up. Extra letters in the names I mean. _Shrug_
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwhoej/)
That a model works for you is always the most important thing. Mixtral Instruct is only in 5th place on my list but still my number one model currently. 
The DPO version is weird because it completed 3/4 of the main tests perfectly. It only lost because it didn't at all answer 3/4 questions of the first test, claiming all answers were correct, which they obviously weren't. Weird! 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwgkvz/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfxv2bi/)
Benchmark idea.Test every top model of it's size against itself but with different quantization. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfys0t2/)
Been there, done that! ;) Well, not of all top models, that would be a full time job - but I took the top 70B model and [tested different formats and quantization levels](https://www.reddit.com/r/LocalLLaMA/comments/17w57eu/llm_format_comparisonbenchmark_70b_gguf_vs_exl2/) of it. 
5 more replies 
5 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfys0t2/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfxv2bi/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfy1d4r/)
There has to be something we are missing on the mixtral finetunes, considering they are all coming in so much below the base model of mixtral. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfy8ylc/)
Yes, definitely, that's what Eric told me as well. He confirmed that his own benchmarks show the same results as my tests, and for some reason, dolphin-2.5-mixtral-8x7b is still the best MoE Dolphin (which is still far from Mixtral Instruct). They're working on it, though, so I still have hope for the next release. 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfy1d4r/?force-legacy-sct=1)
• [ Promoted ](https://www.reddit.com/user/UK-government/)
Protect your business with Cyber Essentials certification. Find out if you’re ready with our free interactive tool.
Learn More
ncsc.gov.uk 
[ Specialist-State2004 ](https://www.reddit.com/user/Specialist-State2004/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwlbpw/)
how [Nous-Capybara-34B-GGUF](https://huggingface.co/TheBloke/Nous-Capybara-34B-GGUF) got the 1st ranks while [Mixtral-8x7B-Instruct-v0.1](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1) is at 5 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwmh0b/)
I ask questions, the models answer, and I tally the results. Nous-Capybara-34B-GGUF just answered everything perfectly, like the other top ranked ones, whereas Mixtral-8x7B-Instruct-v0.1 made two mistakes in the blind run (where I don't provide all the information required to answer the questions, so the model either knows or deduces the answers). 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwp2an/)
In my personal tests Mixtral is worse than Nous-Capybara 34B and Qwen 72B. 
Mixtral feels almost like ChatGPT 3.5 with all the frustrating hiccups. 
Nous-Capybara on the other hand feels somewhere between ChatGPT 3.5 and 4.0. 
(Use case: I mainly use LLMs for research and problem solving) 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwp2an/?force-legacy-sct=1) 1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwlbpw/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwe37c/)
thanks for the hard work. I am surprised by goliath 2quant being so good. I'll play with it more. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwfe41/)
It definitely adheres to the old rule of thumb that a bigger model at higher quantization is better than even an unquantized smaller one. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwi0eh/)
goliath is basically 2 70b llamas smashed together, then quant it to 2, and it beats 70b 4quant at your testing. what are we even doing... 
4 more replies 
4 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwi0eh/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwfe41/?force-legacy-sct=1) 4 more replies 
4 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwe37c/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfwedtm/)
Cheers 🍻 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfx8s3f/)
Thank you. 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfyhzmt/)
Someone probably asked this already, but you just don't have any interest in stuff between 7B and 34B?Or are they not fit for this type of benchmark for some reason? 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfytzfl/)
Next on my ~~to-do~~ to-test list are still the 10B and updated 34B models. Just didn't get around to them yet as they are in a weird spot: If you prioritize quality (and have the necessary resources), you can usually go bigger for maximum quality. If you (are forced to) prioritize size/speed, you may need to go smaller. 
But the tests I've done so far show great potential in that size range. I'm looking forward to the upcoming results. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfytzfl/?force-legacy-sct=1) [ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfyhzmt/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kgdhfvi/)
We have some recent stats showing that q4 for Mixtral is about as damaging as q3_K_M would be for a single 7b in terms of relative quantization error (as measured by KL divergence):<https://github.com/ggerganov/llama.cpp/pull/4739>
Mixtral seems less "compressible" compared to larger dense models, and I worry a bit that 4-bit transformers is giving a slightly skewed representation as a result. Would you be interested in re-testing Mixtral Instruct at q5_K_M, or ideally q6_K? Especially since Mixtral's q6_K requires less VRAM than q4_0 70b does. 
16 more replies 
16 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kgdhfvi/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfy33i2/)
You're doing god's work here 
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfzjiy8/)
Would you run your tests with the API versions of the mistral-medium/mistral-small/mistral-tiny? It would be very interesting to see where mistral-medium lands, and how mistral-small/mistral-tiny fairs with their open weights versions. 
Also maybe try google's Gemini Pro, too, while its API is still free to use. 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfzjiy8/?force-legacy-sct=1)
[ Illustrious-Cash-135 ](https://www.reddit.com/user/Illustrious-Cash-135/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfzk06b/)
Anyone have a list of Prompt syntax templates ? 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kfzk06b/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kg4zehr/)
I think it's naive to run the tests in one language, if the model was trained on another language. This is especially true for the small models. What is interesting is that the tests you use, hopefully was not visible by the training data, when in German. But who knows. 
It's equally naive to build and train small models in multiple languages and think they'll be useful. 
It would be fair to ask to repeat the tests using a Google translated (for consistency) test set and questions, and see how the results differ from German. 
[ Obvious-River-100 ](https://www.reddit.com/user/Obvious-River-100/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kga5ody/)
I check with one question: What is heavier than a kg of fluff or a kg of iron? So far, no open source has answered correctly 
6 more replies 
6 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kga5ody/?force-legacy-sct=1)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kgolcos/)
I'm hearing very good things about <https://huggingface.co/Doctor-Shotgun/Mixtral-8x7B-Instruct-v0.1-LimaRP-ZLoss> in terms of it actually matching the official Instruction tune's quality. If you plan on doing more Mixtral models soon, I would prioritize this 
1 more reply 
1 more reply 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/kgolcos/?force-legacy-sct=1)
[ RiemannZetaFunction ](https://www.reddit.com/user/RiemannZetaFunction/)
• [ 2y ago ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/ki0roiw/)
Which gpt-3.5-turbo and gpt-4 were these? The 1106 ones or the 0613? 
5 more replies 
5 more replies 
[ Continue this thread  ](https://www.reddit.com/r/LocalLLaMA/comments/18w9hak/comment/ki0roiw/?force-legacy-sct=1)
View more comments
View more comments
## 
View Post in 
##  Top Posts 
  * [ Reddit  reReddit: Top posts of January 1, 2024 ](https://www.reddit.com/posts/2024/january-1-1/global/)
  * [ Reddit  reReddit: Top posts of January 2024 ](https://www.reddit.com/posts/2024/january/global/)
  * [ Reddit  reReddit: Top posts of 2024 ](https://www.reddit.com/posts/2024/global/)


[Reddit, Inc. © 2026. All rights reserved.](https://redditinc.com)
