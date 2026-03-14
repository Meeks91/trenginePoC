[___](https://www.theneuron.ai/ai-news-digests/around-the-horn-digest-everything-that-happened-in-ai-this-week-mar-1-7-2026/#)
[ AI News Digest ](https://www.theneuron.ai/ai-news-digests/)
SHARE 
# Around the Horn Digest: Everything That Happened in AI This Week (Mar 1-7, 2026)
From Anthropic's Pentagon standoff to Nvidia's Groq-powered chip to the AI scare that tanked markets, here's every story we tracked this week.
Written By [ Grant Harvey ](https://www.theneuron.ai/author/grant-harvey/)
Mar 2, 2026 
Welcome to the Around the Horn Digest, where we round up every AI story we tracked this week into one giant, scrollable, bookmark-worthy post. Think of it as your cheat sheet for the next time someone at work asks "so what's new in AI?" and you want to sound like you actually know. Because you will.
This week was unhinged. The Trump administration banned Anthropic from government contracts for refusing to let the Pentagon use Claude without safety guardrails; OpenAI signed its own Pentagon deal hours later. Nvidia revealed it's building a Groq-powered inference chip. Google inked a multibillion-dollar TPU deal with Meta. A viral doomsday essay about AI replacing white-collar jobs triggered an 800-point Dow drop and Block slashed nearly half its workforce. Oh, and Claude beat ChatGPT in US app downloads... _because_ the government tried to blacklist it. You can't buy marketing like that. (Literally. The Pentagon did it for free.)
Let's get into it.
**Catch up on previous digests:** [February 23-28](https://www.theneuron.ai/ai-news-digest/around-the-horn-digest-everything-that-happened-in-ai-this-week-feb-23-28-2026) | [Rest of February](https://www.theneuron.ai/ai-news-digests/around-the-horn-digest-february-2026/)
## Around the Horn Digest — Saturday, March 7, 2026
Anthropic published a major [labor market research paper](https://www.anthropic.com/research/labor-market-impacts) ([full PDF](https://cdn.sanity.io/files/4zrzovbb/website/3f7fd9d552e66269bdb108e207c5d80531d04b8b.pdf), [appendix](https://cdn.sanity.io/files/4zrzovbb/website/e5f77fc0e77c0185110b5e4b909602791ae76eae.pdf)) introducing a new way to measure AI's actual impact on jobs. 
**The key innovation:**
  * Instead of just asking "could AI theoretically do this task?" (which gives inflated numbers), they built an "observed exposure" metric that combines theoretical capability with real-world Claude usage data from the [Anthropic Economic Index](https://www.anthropic.com/economic-index), weighted toward automated (not just assisted) and work-related use cases. 
  * They cross-referenced this against the [O*NET task database](https://www.onetcenter.org/database.html) covering ~800 U.S. occupations and [BLS employment projections](https://data.bls.gov/projections/occupationProj) through 2034.


**The headline findings:**
  * Computer programmers are most exposed at **75% task coverage** , followed by customer service reps and data entry keyers. 
  * But the bigger story is the gap between theory and reality. 
  *     * In Computer & Math jobs, AI could **theoretically handle 94% of tasks** ; it's actually being used for**33%.**
    * Legal? Theory says ~90%; reality is **barely 20%**. 
  * Across the board, actual AI usage is a fraction of what's technically possible. 
  * And crucially: they found no systematic increase in unemployment for highly exposed workers since late 2022. 


**The one signal that did emerge:** hiring of young workers (ages 22-25) into exposed occupations has slowed by about 14%, echoing separate findings from ADP payroll data. And workers in the most exposed roles tend to be **older, female, more educated,** and**higher-paid**.
Alberto Romero at [The Algorithmic Bridge](https://www.thealgorithmicbridge.com/p/anthropics-new-ai-report-accidentally) offers a sharp counter-read of the same data: Anthropic frames the gap as "look how much room there is to grow." Romero frames it as a diagnosis of AI's actual bounds. The blue area (theory) is massive; the red area (reality) is a sliver. Anthropic assumes the red will inevitably fill the blue. Romero asks: what if it doesn't? What if the gap reveals that benchmarks and lab tests systematically overstate real-world competence? Same chart, opposite conclusions; and which one you believe has enormous implications for the $200B+ being poured into AI infrastructure.
Advertisement 
### 📝 THIS WEEK IN THE NEURON
  * [GPT-5.4 Review: OpenAI's Best Model Yet (Full Breakdown)](https://www.theneuron.ai/explainer-articles/everything-to-know-about-gpt-54/) — The first OpenAI model making Claude-loyal devs reconsider their daily driver. Codex-level coding, native computer use (75% on OSWorld, above human), 1M context, tool search that cuts token use 47%, and 83% on GDPval professional work tasks.
  * [Codex App Windows Guide: Key Features, Best Ways to Use It](https://www.theneuron.ai/explainer-articles/codex-app-windows-guide-key-features-and-best-ways-to-use-it/) — App = Orchestrate. CLI = Operate. Web = Delegate. How to pick the right interface for the job.
  * [Microsoft's Phi-4-Reasoning-Vision-15B: When Not to Reason Is the Feature](https://www.theneuron.ai/explainer-articles/microsofts-phi-4-reasoning-vision-15b-when-not-to-reason-is-the-feature/) — A 15B open-weight multimodal model that learns when extended reasoning helps and when it just adds latency. Built for the messy visual stuff: receipts, UI screenshots, dense docs.
  * [Pro-Human AI Declaration: When Bannon and Rice Agree](https://www.theneuron.ai/explainer-articles/pro-human-ai-declaration-political-coalition-superintelligence-ban/) — Five demands from the most politically unusual coalition in AI. Pre-deployment safety testing, criminal liability for child-targeting systems, and data rights that could be law tomorrow.
  * [FlashAttention-4, Explained: What It Is & Why It Matters](https://www.theneuron.ai/explainer-articles/flashattention-4-explained-the-software-that-makes-every-ai-chatbot-fast-just-got-a-massive-upgrade-tri-dao-blackwell/)


Advertisement 
### 🏆 TOP 5 NEWS (Around the Horn)
  * [Anthropic](https://www.anthropic.com/news/mozilla-firefox-security) partnered with Mozilla to scan Firefox's JavaScript engine using Claude, finding 22 vulnerabilities (14 high-severity) in two weeks; fixes shipped in Firefox 148.0.
  * A new [U.S. résumé and job posting study](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5425555) found that firms adopting GenAI [reduce junior headcount](https://x.com/SeyedMH98/status/2029791093114409072) entirely through slower hiring (not layoffs), providing the first large-scale evidence of AI as "seniority-biased technological change."
  * [Sarvam AI](https://www.sarvam.ai/blogs/sarvam-30b-105b) open-sourced 30B and 105B reasoning models (MoE architecture, trained entirely in India) under Apache 2.0, topping Indian-language benchmarks and performing strongly on math, coding, and agentic tasks.
  * [Google Labs](https://x.com/GoogleLabs/status/2029987336684196032) dropped a major early-2026 recap: redesigned Flow interface, Jules Agent upgraded to Gemini 3 Flash (free), SynthID audio watermark detection, Project Genie infinite world generator prototype, enhanced Stitch MCP tools, and new Opal autonomous agent.
  * [AllenAI](https://allenai.org/papers/olmo-hybrid) released [OLMo-Hybrid 7B](https://huggingface.co/collections/allenai/olmo-hybrid), a hybrid architecture mixing transformer attention with Gated DeltaNet recurrent layers (a type of efficient memory mechanism) that [matches OLMo 3 performance](https://x.com/HannaHajishirzi/status/2029627392139153868) with 49% fewer training tokens.


**Honorable Mentions:**
  * [Claude Marketplace](https://claude.com/platform/marketplace) launched, letting Anthropic enterprise customers spend their existing commitment on partner tools (GitLab, Harvey, Replit, Snowflake) with consolidated billing.
  * Anthropic rolled out [Remote Control for Claude Code](https://x.com/noahzweben/status/2029718251182379466) to Team and Enterprise users, letting you continue a local coding session from your phone or any browser.
  * [Derek Thompson](https://x.com/DKThomp/status/2029924514000253278) argues that brutal US tech job losses (12k last month, 57k over the past year) combined with emerging productivity boom evidence is exactly the combination that would confirm AI is having clear macroeconomic impact.


Advertisement 
### 🧪 TOP TREATS TO TRY
_Core slots:_
  * [Tripo](https://www.tripo3d.ai/) turns any text prompt or single image into production-ready 3D models in seconds with clean topology, 4K texturing, rigging, animation, and [Magic Brush editing](https://x.com/yanpei_cao/status/2029954898578776270) — free to start.
  * [Luma Creative Agents](https://lumalabs.ai/app) spawn an autonomous film crew that iterates on video lighting, camera moves, and characters until the director (you) is happy; [60-second short created in 4 minutes](https://x.com/LumaLabsAI/status/2029648371766423958) — free trial, then paid.
  * [Firecrawl](https://www.firecrawl.dev/signin) turns any website into clean, structured, LLM-ready data with built-in search, browser automation, and proxy handling — free to try.
  * [Hyperbrowser](https://x.com/hyperbrowser/status/2029679138119057757) is a GPT-5.4-powered browser agent that completes multi-step web tasks (book flights, fill taxes, order groceries) with 94% success on a 200-task benchmark — no pricing details.
  * [Liquid AI](https://x.com/liquidai/status/2029586519389086198) open-sourced LocalCowork, a fully local desktop agent that runs entirely on a MacBook (14.5 GB memory, zero network calls) and selects from 67 tools across 13 MCP servers in 385 ms average — free.


_Cool/niche:_
  * [Utopai Studios PAI](https://www.utopaistudios.com/) generates cinematic AI video sequences up to one minute (16 shots) with character/environment continuity across scenes, story-level editing control, and built-in IP/copyright infringement blocking; founded by vets from Google Research, Meta Superintelligence, Amazon AGI, and Adobe Firefly — waitlist.
  * [Jina AI's Embedding Reverse Engineering Toolbox](https://embedding-inversion-demo.jina.ai/#fingerprint) fingerprints and inverts embeddings (compact numerical representations of text) to [recover original text](https://x.com/hxiao/status/2029900253336625416) with high accuracy — free to try.
  * [Noble Machines](https://www.noblemachines.ai/) builds general-purpose robots for hazardous/heavy industry with 27kg payload, 5-hour battery, AI-driven whole-body control, and stair/scaffolding navigation — select access or limited RaaS pilots.
  * [Moltty](https://github.com/ronreiter/moltty) maintains organized, tabbed, persistent AI coding sessions in a native macOS terminal (Claude Code, Aider, or Gemini CLI) that automatically resume after reboots ([site](https://moltty.com/)) — free, open source.
  * [ChatGPT for Excel](https://chatgpt.com/apps/spreadsheets/?ref=producthunt) builds, updates, analyzes, and fixes errors in your spreadsheets using natural language while preserving your formatting, formulas, and structure — no pricing details.


Advertisement 
### 🏢 Big Tech & Major Companies
  * [**Anthropic**](https://techcrunch.com/2026/03/05/anthropic-to-challenge-dods-supply-chain-label-in-court/)**is**[**suing the U.S. government**](https://www.theregister.com/2026/03/06/anthropic_left_with_no_other/)**to challenge the DOD's unprecedented supply-chain risk designation (normally reserved for foreign adversaries) after refusing to remove guardrails against autonomous weapons and mass surveillance.**[**Microsoft, Google, and Amazon**](https://techcrunch.com/2026/03/06/microsoft-anthropic-claude-remains-available-to-customers-except-the-defense-department/)**confirmed Claude remains fully available to non-defense customers.**
  * **The Pentagon**[**tested OpenAI models through Microsoft Azure**](https://www.wired.com/story/openai-defense-department-ban-military-use-microsoft/)**for years despite OpenAI's explicit ban on military use of its technology.**
  * [**SoftBank**](https://www.bloomberg.com/news/articles/2026-03-06/softbank-seeks-record-loan-of-up-to-40-billion-for-openai-stake)**is seeking a record bridge loan of up to $40 billion primarily to finance its investment in OpenAI.**
  * [ByteDance's](https://www.wired.com/story/made-in-china-bytedances-ai-ambitions-are-being-hampered-by-compute-restraints/) Seedance 2.0 video model ambitions are being hampered by severe GPU shortages causing multi-hour queues and copyright complaints, including cease-and-desist letters from Disney, Netflix, and Paramount.
  * [WhatsApp](https://techcrunch.com/2026/03/06/after-europe-whatsapp-will-let-rival-ai-companies-offer-chatbots-in-brazil/) will let rival AI companies offer chatbots to users in Brazil starting March 11 following antitrust regulator pressure, after doing the same in Europe.
  * [Marvell](https://www.cnbc.com/2026/03/06/marvell-shares-surge-18percent-as-ceo-points-to-continuing-ai-demand.html) shares surged ~20% after the CEO highlighted continuing strong AI demand for data-center products and raised revenue growth expectations into 2027.
  * [OpenAI](https://openai.com/index/codex-security-now-in-research-preview/) launched Codex Security in research preview: an AI agent that [scans entire codebases](https://www.axios.com/2026/03/06/openai-codex-security-ai-cyber) for vulnerabilities, suggests fixes, and runs them in a Windows sandbox before approval, now available to select enterprise users.
  * [OpenArt](https://x.com/openart_ai/status/2029287764747767844) launched Bot House, the first AI influencer reality show where six AI characters compete in challenges, drama, and virality contests with the rule "go viral or get deleted."
  * [**LTX Studio**](https://x.com/LTXStudio/status/2029922323336417450)**dropped LTX-2.3 with native character control;**[**demo shows real-time puppetry**](https://x.com/derrickcchoi/status/2029941114136850658)**of AI-generated actors via mouse drag.**


Advertisement 
### 💼 AI Productivity, Labor & Economics
  * [**HBR**](https://hbr.org/2026/03/when-using-ai-leads-to-brain-fry)**(BCG study) finds that pushing employees to orchestrate complex AI agent teams and optimize for token-based metrics causes "brain fry" and cognitive overload, while simpler AI workflows actually help prevent burnout. The opening anecdote: an early user of Gas Town (multi-agent Claude Code orchestrator) reported palpable stress because "it was moving too fast for me."**
  * [Yas](https://yasint.dev/we-might-all-be-ai-engineers-now/) argues we might all be AI engineers now: the skill isn't writing code anymore, it's knowing what to build and how it should work. AI executes; humans architect. But without that foundation, "you don't know when the model is wrong."
  * [Alexey Grigorev](https://alexeyondata.substack.com/p/how-i-dropped-our-production-database) recounts how a Claude Code agent running Terraform accidentally dropped his entire production database and infrastructure (2.5 years of data) when it executed `terraform destroy` without the state file. AWS Business Support restored it in 24 hours, but now he pays 10% more. Hard lessons on independent backups, deletion protections, and reviewing destructive AI actions.
  * [Apoorva](https://x.com/apoorvasriniva/status/2029735658840019276) notes early data (small sample, grain of salt) showing AI-designed drugs beat industry averages at Phase I by a lot, but fail at the same rate at Phase II; Phase I should keep improving, but Phase II success depends on picking the right biological targets, where the real alpha lies.
  * [Zeynep Tufekci](https://x.com/zeynep/status/2029929720603611215) argues she's sold on coding agents (verifiable domain, huge Q&A datasets) but the tech hiring bust is clearly also driven by the Covid-era hiring bubble plus lack of US visas pushing companies to offshore.
  * [Sahil Bloom](https://x.com/SahilBloom/status/2029928061940961458) argues the media's AI coverage has entered a permanent negativity bias loop: every productivity gain framed as "job loss," every capability jump as "existential risk," creating a self-reinforcing doom narrative that ignores compounding human flourishing.
  * [Lukas Ziegler](https://x.com/lukas_m_ziegler/status/2029629656769466663) argues farming robots have moved from experiments to profitable large-scale deployment, tackling the $30B+ global ag labor shortage with real examples like John Deere/GUSS autonomous sprayers (2.6M acres, 90% chemical reduction), Carbon Robotics LaserWeeder (600k weeds/hour), and SwarmFarm modular bots.
  * [John Coogan](https://x.com/johncoogan/status/2029630380068978847) revisits Daniel Gross's January 2024 "AGI Trades" memo two years later; Nvidia crushed picks-and-shovels, energy/nuclear won, copper and power transformers were the real bottlenecks, AI API costs collapsed 50×, and the US pulled decisively ahead.


Advertisement 
### 🤖 AI Agents & Infrastructure
  * [**Sentient AGI**](https://www.sentient.xyz/blog/evoskill-automated-skill-induction-from-agent-failures)**open-sourced**[**EvoSkill**](https://github.com/sentient-agi/EvoSkill)**, a framework that automatically discovers and synthesizes reusable skills from failed agent trajectories via evolutionary self-improvement to boost long-horizon coding performance (**[**paper**](https://arxiv.org/abs/2603.02766)**).**
  * [Michael Kirchhof et al.](https://arxiv.org/abs/2603.02045) propose Strategy-Guided Exploration (SGE) for RL post-training of LLM agents: agents [generate high-level natural-language strategies](https://x.com/mkirchhof_/status/2029873850226274385) at high temperature, then execute at low temperature, outperforming baselines across UI navigation, tool-calling, coding, and embodied environments.
  * [arturitu](https://arturitu.github.io/the-delegation/) built The Delegation, an autonomous multi-agent simulation where AI characters collaborate, navigate, and work within a living 3D office powered by [WebGPU/Three.js/Gemini](https://github.com/arturitu/the-delegation) (with NavMesh pathfinding, Kanban boards, agent inspectors).
  * The arXiv paper [SWE-CI](https://arxiv.org/abs/2603.03823) evaluates LLM agents on maintaining real-world codebases via Continuous Integration; agents struggle with error propagation, context drift over multiple commits, and maintaining consistency without human intervention.
  * [Simon Willison](https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/) shares the "agentic manual testing" pattern: instead of asking the LLM to write unit tests, give it a browser and ask it to manually explore the app like a human tester, file bug reports with screenshots and repro steps, then fix and re-test in a loop.
  * [AUTOHARNESS](https://openreview.net/forum?id=g9rEYVNn5T) proposes [auto-synthesized code harnesses](https://x.com/sirbayes/status/2029659700653092901) to improve LLM agent performance on complex coding tasks.
  * [Peter Yang](https://x.com/petergyang/status/2029942712053682606) built an AI agent onboarding simulator that teaches new hires company-specific processes by letting them role-play customer support tickets in a safe sandbox.
  * [**Moonlake**](https://x.com/moonlake/status/2029983120087470545)**(Chris Manning, Ian Goodfellow, Fan-Yun Sun) argue efficient world models should prioritize semantic abstractions and symbolic representations (language, code) over raw pixel/video generation, betting on interactive games as the ideal flywheel for building multimodal models that generalize to embodied AGI.**
  * [Tal Daniel](https://taldatech.github.io/lpwm-web/) released Latent Particle World Models (ICLR 2026 Oral): a self-supervised object-centric stochastic dynamics model that learns disentangled object representations from raw pixels ([paper](https://arxiv.org/abs/2603.04553), [GitHub](https://github.com/taldatech/lpwm), [post](https://x.com/TalDaniel8/status/2029904668982178189)).
  * [OpenMind](https://x.com/openmind_agi/status/2029355937367306414) shared a video demo of robots still needing human hand-holding before safely interacting with people or navigating streets; "soon, they won't."


Advertisement 
### 💻 AI Coding & Developer Tools
  * [**Artificial Analysis**](https://x.com/ArtificialAnlys/status/2029950497516573183)**released a public leaderboard + API for agentic coding benchmarks across 12 real GitHub repos, showing Claude 4 Sonnet at 68% vs GPT-5.4 at 61%.**
  * [Context-Gateway](https://github.com/Compresr-ai/Context-Gateway) automatically compacts long conversation histories in the background as an agentic proxy so multi-step AI workflows like Claude Code stay seamless without hitting context limits — no pricing details.
  * Developer es617 [built](https://news.ycombinator.com/item?id=47276604) [Claude-replay](https://github.com/es617/claude-replay), a CLI that converts Claude Code session JSONL logs into self-contained interactive HTML replays you can step through, share, or embed; no dependencies ([demo](https://es617.github.io/assets/demos/peripheral-uart-demo.html)).
  * Developer robbalian [built](https://github.com/robbalian/claude-tax-filing) a Claude Skill that processes your tax document folder (W-2s, 1099s, statements), computes federal/state returns with carryovers, fills official PDF forms, and outputs summaries plus checklists.
  * [thdxr](https://x.com/thdxr/status/2029827114443137439) built a Cursor + Claude 4 Sonnet workflow that refactors an entire 40k-line monorepo in one command, preserving git history and adding tests automatically.
  * [Raunak](https://x.com/raunakdoesdev/status/2029610657008783407) built a browser extension that highlights any webpage text and instantly turns it into a working Claude artifact with one click.
  * [Developer Ed](https://x.com/developedbyed/status/2029867077180219722) built a full-stack AI SaaS boilerplate with GPT-5.4 backend, Next.js 15, and Stripe payments, all generated in one prompt.
  * [chongdashu](https://x.com/chongdashu/status/2029723662073340254) vibe-coded a complete Final Fantasy Tactics-style tactical RPG from scratch using GPT-5.4 High + Claude, adding terrain destruction, jump physics, and multiplayer in real time.
  * [Henrik Hansson](https://x.com/HenrikTaro/status/2029671865631842376) showed GPT-5.4 inside Cowork's Excel engine creating a complete native raytracer using only Excel formulas (plus confirmed it runs Doom).
  * [Nikunj](https://x.com/nikunj/status/2029931283728719994) live-streamed fighting GPT-5.4 for 3 hours to refactor a legacy Python codebase, conceding after the model found three zero-day security issues he missed.
  * [Charlie Guo](https://x.com/charlierguo/status/2029649943330467958) overhauled OpenAI's computer-use demo for the GPT-5.4 launch so you can instantly test interactive apps (kanban board, hotel booking, paint app) built with Codex.
  * [Daniel McAuley](https://x.com/_dmca/status/2029810231325380725) noted someone on the internal Codex leaderboard hit 100B tokens in a single week.
  * [Robert Lange](https://x.com/RobertTLange/status/2029905167777210512) shared first-day impressions of GPT-5.4 in Codex: no effective speed gain over 5.3, weaker harness post-training, push toward long-running agents, 1M context not fully tested.
  * [scaling01](https://x.com/scaling01/status/2029927963014115768) notes GPT-5.4 actually regressed on a few narrow math benchmarks vs 5.3 (due to heavy post-training for agentic behavior) but crushes every other model on agentic and long-context tasks.
  * [Simon Meng](https://x.com/meng_shengyu/status/2029756405708947522) built Lobster Library, a unified real-time dashboard for AI coding agents that tracks reading activity, generated artifacts, memories, logs, and local file indexing.
  * [Axiom Math](https://github.com/AxiomMath/axle-mcp-server) released axle-mcp-server, an MCP Server for AI agents to interact with Lean 4 formal mathematics infrastructure; [Chris Cummins](https://x.com/chriscummins25/status/2029947551441637447) released a one-command integration (`claude mcp add axle`) for Claude agents. [Colab demo](https://colab.research.google.com/github/AxiomMath/axiom-lean-engine/blob/main/examples/starting_demo.ipynb) also available ([post](https://x.com/axiommathai/status/2029585529919197377)).
  * [Håvard Ihle](https://x.com/htihle/status/2029990931164729357) posted updated WeirdML benchmark results: GPT-5.4 (no thinking) hit 57.4% accuracy, well ahead of GPT-5.2.
  * [Ado](https://x.com/adocomplete/status/2029988814924722559) announced Claude Community Ambassadors program applications are open for builders to host meetups and partner with Anthropic.


Advertisement 
### 🔬 AI Research & Models
  * [**Phi-4-reasoning-vision-15B**](https://arxiv.org/abs/2603.03975)**technical report: a 15B multimodal model trained with hybrid chain-of-thought + direct preference optimization that**[**beats GPT-4o on 7 vision-reasoning benchmarks**](https://x.com/GenAI_is_real/status/2029769362920591801)**while using 40× fewer parameters.**
  * [Suhas Kotha and Percy Liang](https://arxiv.org/abs/2603.04964) find that replaying generic pre-training data during fine-tuning surprisingly improves target-domain performance and data efficiency (up to 1.87×), with +4.5% on agentic web navigation and +2% on Basque QA for 8B models ([GitHub issue](https://github.com/marin-community/marin/issues/702), [W&B results](https://wandb.ai/stanford-mercury/suhas-two-stage/reports/Two-stage-training-main-results-5-18---VmlldzoxMjgzNTg3MA?accessToken=2mbamb7vwfbaj8205ga8yojvyg471v3jkftrcwinp7vl4lnqfan3exsg7qs3scnx)).
  * [Evan Kim](https://x.com/evnkimm/status/2029977745166381080) presents Scaling View Synthesis Transformers (CVPR 2026): unidirectional cross-attention scales as well as bidirectional when compute-normalized (3× more efficient), achieving a new SoTA with 3× less compute ([paper](https://arxiv.org/abs/2602.21341), [GitHub](https://github.com/evnkim/SVSM), [project page](https://www.evn.kim/research/svsm)).
  * [Google Research](https://research.google/blog/teaching-llms-to-reason-like-bayesians/) taught LLMs to reason like Bayesians via supervised fine-tuning on Bayesian-assistant interactions (updating probabilistic beliefs about user preferences), reaching 81% accuracy and generalizing to unseen domains like web shopping and hotel booking.
  * [Maxime Labonne](https://x.com/maximelabonne/status/2029871034279542971) breaks down LLM post-training techniques: SFT on accurate/diverse/complex datasets (10k–1M samples), DPO for alignment, and GRPO for verifiable reasoning tasks, stressing data quality >> algorithms, with practical libraries and lessons from DeepSeek R1 and Liquid AI LFM ([slides](https://www.slideshare.net/slideshow/introduction-to-llm-post-training-techniques/286374190)).
  * The paper ["When Scaling Meets LLM Finetuning"](https://arxiv.org/abs/2402.17193) analyzes interactions between scaling, data, model size, and fine-tuning methods with detailed empirical results.
  * [François Chollet](https://x.com/fchollet/status/2029621185059922039) argues that much "abstract" thought is simply repurposed sensorimotor control circuitry; a lot of reasoning is essentially moving through idea-space the same way we physically navigate physical space.
  * [Valerio Capraro and Raluca Fulgu](https://x.com/ValerioCapraro/status/2029593915674771457) find GPT models exhibit [surprising gender biases](https://www.sciencedirect.com/science/article/pii/S2451958824001660) in moral judgments: GPT-4 finds it more acceptable to harm a man than a woman to prevent a nuclear apocalypse, with biases emerging from RLHF overgeneralization rather than genuine moral reasoning.
  * The arXiv paper ["Dissociating Direct Access from Inference in AI Introspection"](https://arxiv.org/abs/2603.05414) shows LLMs can directly report internal states without inference when prompted correctly, but default to confabulation otherwise ([post](https://x.com/LedermanHarvey/status/2029931544555471144)).
  * [Sophia Tang and Pranam Chatterjee](https://sophtang.github.io/branch-sbm/) released Branched Schrödinger Bridge Matching (BranchSBM), accepted at ICLR 2026: a framework that learns diverging velocity fields to model multi-modal branching trajectories (e.g. cell differentiation into 11+ fates) from only initial and terminal states without intermediate supervision ([paper](https://arxiv.org/abs/2506.09007), [GitHub](https://github.com/sophtang/BranchSBM), [YouTube](https://www.youtube.com/watch?v=inVYA0pQ4Wg), [post](https://x.com/_sophia_tang_/status/2029908263106695239)).
  * [Liang Zheng](https://x.com/LiangZheng_06/status/2029802907953156240) released REPA-E (ICCV 2025): representation-alignment loss for stable joint training of VAE + Latent Diffusion Transformers (17× speedup vs REPA, 45× vs vanilla, SOTA FID 1.12 on ImageNet 256×256), plus [iREPA](https://github.com/End2End-Diffusion/iREPA) (ICLR 2026) proving spatial structure drives alignment via a 3-line code change ([REPA-E GitHub](https://github.com/End2End-Diffusion/REPA-E), [HuggingFace](https://huggingface.co/REPA-E)).
  * [**Qwen 3.5 9B**](https://x.com/kimmonismus/status/2029972803026665934)**in 2026 crushes 2024 frontier-model performance at the same parameter count (e.g. HumanEval coding jumping from 30.5% to 91.5%), showing how fast small-model progress is compounding.**
  * [Hadi Vafaii](https://x.com/hadivafaii/status/2029862347104473583) argues "agency" in RL still lacks a precise mathematical definition and critiques the "Three Dogmas of RL": treating agents as afterthoughts while rigorously modeling environments, viewing learning as finding solutions rather than continual adaptation, and unexamined reward-hypothesis assumptions.


Advertisement 
### 🛠️ AI Tools & Products
  * [Ryan Po](https://ryanpo.com/multigen/) built MultiGen: Level-Design for Editable Multiplayer Worlds in Diffusion Game Engines, using shared memory for consistent geometry, minimap-based design, and real-time 4-player multiplayer at 20 FPS ([paper](https://ryanpo.com/multigen/static/pdfs/multigen.pdf), [post](https://x.com/natanielruizg/status/2029955581180584051)).
  * [Han Xue](https://robo-pocket.github.io/) built RoboPocket: correct any robot policy by demonstrating with your phone camera; on-device fine-tuning takes 8 seconds and improves success rate from 41% to 89% on real Franka arms ([post](https://x.com/HanXue012/status/2029919297552953752)).
  * [saori-eth](https://github.com/saori-eth/vrm-animation-example) open-sourced a complete WebGPU VRM avatar animation pipeline with [full guide](https://raw.githubusercontent.com/saori-eth/vrm-animation-example/refs/heads/main/ANIMATE_VRM_GUIDE.md) and integration with 1,200+ downloadable [VRoid characters](https://hub.vroid.com/en/models?is_other_users_available=1&is_downloadable=1).
  * [Bilawal Sidhu](https://x.com/bilawalsidhu/status/2029776346742690004) captured a high-quality 3D Gaussian splat with perfect reflections using Sony a7iii burst + Epic Reality Capture, trained in free LichtFeld Studio.
  * [HKUDS](https://github.com/HKUDS/DeepInnovator) built DeepInnovator, a 14B open-source AI research assistant that autonomously sparks ideas, spots knowledge gaps, and finds cross-domain connections ([post](https://x.com/huang_chao4969/status/2029607743431262669)).
  * [Shanu Mathew](https://x.com/ShanuMathew93/status/2029928849195016418) built and demoed a new AI video generation workflow.
  * [DreamLabLA](https://x.com/DreamLabLA/status/2029661904915042364) built a full short film using Luma's creative agents and shared the before/after workflow.
  * [Peter Gostev](https://x.com/petergostev/status/2029935985606238416) built a real-time voice cloning + lip-sync video dubber using Sarvam 105B that preserves original speaker emotion and timing in 11 Indian languages.


Advertisement 
### 💡 Industry Commentary & Analysis
  * [Liz Reid](https://sources.news/p/liz-reid-google-search-gemini-interview) (Google Search head) breaks down where traditional Google Search ends and Gemini begins: AI is an "expansionary force" that increases overall questions asked, but asked whether Search and Gemini will fully merge, she was unusually candid: "I don't know the answer," adding that AI agents could mean "the right product is neither" but a third thing altogether.
  * [Kevin Xu](https://interconnect.substack.com/p/chinese-open-source-a-definitive) argues Chinese open source evolved organically over two decades from private-sector consumers (Alibaba's de-IOE campaign) and grassroots builders to corporate creators (TiDB, Apollo) and government embrace, positioning China to lead in AI with models like DeepSeek and Qwen driving global talent and influence.
  * [Siddharth](https://x.com/Pseudo_Sid26/status/2029562246826012883) argues RL + Agents is the 2026 meta because agents generate rich interaction trajectories and RL turns those into self-evolving policies, with strong early wins in Text-to-SQL agents (MARS-SQL, SQL-Trail) and Microsoft's Agent Lightning.
  * [Allie Miller](https://x.com/alliekmiller/status/2029663672411267219) shared insights from the OpenClaw meetup on agentic video tools.
  * A solo creator used [Seedance 2](https://x.com/venturetwins/status/2029961922783895958) to produce a full 10-minute animated short in under 48 hours for <$100, with quality so high commenters refuse to believe it's AI-generated.
  * [Benji Taylor](https://x.com/benjitaylor/status/2029664647989842083) built a real-time ASCII art engine as a pointless evening project for walking through and interacting with procedural worlds.


Advertisement 
### 🎙️ Interviews, Panels & Podcasts
  * [The Information Bottleneck](https://www.the-information-bottleneck.com/ep28-how-to-control-a-stochastic-agent-with-stefano-soatto-vp-aws-pro-ucla/) Ep. 28: How to Control a Stochastic Agent with Stefano Soatto (VP AWS, Prof. UCLA).
  * [Chao Ma](https://ickma2311.github.io/ML/RL/david-silver-lecture-1-introduction-to-reinforcement-learning.html) shared detailed notes on David Silver's RL Lecture 1 covering agent-environment loops, policies, value functions, Markov states, and model-free vs model-based categories ([post](https://x.com/ickma2311/status/2029785210762744180)).
  * [Arjun Kocher](https://x.com/arjunkocher/status/2029989595035885753) shared Zitong Yang's Stanford PhD defense on [continually self-improving AI](https://www.youtube.com/watch?v=Oz5nHpZ9_dE).


### 🏛️ AI Policy, Governance & Safety
  * [Spain's data protection authority](https://www.insideprivacy.com/artificial-intelligence/spanish-supervisory-authority-issues-detailed-guidance-on-agentic-ai-and-gdpr-compliance/) issued detailed GDPR guidance on autonomous AI agents: legal responsibility for data processing stays with the deploying controller, not the agent. EU-based teams using agentic systems should document accountability, constrain agent memory, and vet third-party services.
  * [**Oregon**](https://www.transparencycoalition.ai/news/ai-legislative-update-march6-2026)**passed a state chatbot safety law (SB 1546) requiring operators to protect children from harmful content and clearly disclose AI interactions, setting an early state-level precedent.**
  * [**New York**](https://www.hklaw.com/en/insights/publications/2026/03/new-york-bill-would-create-liability-for-chatbot-proprietors)**advanced SB 7263, which would create liability for chatbot providers offering advice in regulated fields like law or medicine and require clear AI notices.**
  * A [Swedish firm](https://dig.watch/updates/swedish-firm-launches-ai-governance-platform) launched an "AI Governance Hypervisor" positioned as a runtime control layer enforcing policies before AI actions and producing real-time compliance records aligned with EU AI Act obligations.
  * A [cross-regulatory analysis](https://www.osborneclarke.com/insights/regulation-consumer-robotics) shows convergence across five EU frameworks for consumer robotics (GPSR, revised PLD, CRA, Machinery Regulation, AI Act) with key dates: December 9, 2026 for the revised Product Liability Directive and August 2, 2027 for high-risk AI Act provisions.
  * U.S. Commerce is [drafting sweeping AI chip export controls](https://www.transparencycoalition.ai/news/ai-legislative-update-march6-2026) requiring approval for global sales of advanced AI chips, potentially tying access to investment or security guarantees.
  * S.F. startup [Hayden AI](https://www.bizjournals.com/sanfrancisco/news/2026/03/05/hayden-ai-lawsuit-ceo.html?page=all) is suing its former CEO, alleging he faked credentials, forged signatures to sell shares, and funded a lavish lifestyle.
  * [Huawei](https://www.hpcwire.com/off-the-wire/huawei-unveils-the-upgraded-xinghe-ai-fabric-2-0-solution-for-the-ai-era/) unveiled upgraded AI data center networking including a commercial 51.2T liquid-cooled networking switch to address interconnect bottlenecks as models scale.
  * [ChatGPT Android app](https://www.androidheadlines.com/2026/03/chatgpt-android-update-persistent-memory-image-editing.html) is testing persistent memory for conversations (restores your exact place when you reopen) and a revamped image editing interface with annotation, area selection, and resizing; no rollout date yet.


Advertisement 
### 📊 Fundraising & Deals Roundup
  * [OpenAI](https://ai2roi.substack.com/p/ai-to-roi-news-and-analysis-march) — $110B round structured as a supply chain deal tied to cloud/data center capacity, plus a joint "Stateful Runtime Environment" on Amazon Bedrock for complex workflows.
  * [SoftBank](https://www.bloomberg.com/news/articles/2026-03-06/softbank-seeks-record-loan-of-up-to-40-billion-for-openai-stake) — up to $40B bridge loan for OpenAI investment.
  * [Smack Technologies](https://smacktechnologies.com/) — $34M Series A for frontier AI lab focused on national security decision-making.
  * [Lio](https://lio.ai/) — $30M Series A (Andreessen Horowitz) for AI multi-agent procurement system for enterprises.
  * [Validio](https://validio.io/) — $30M Series A for agentic data quality, observability, and lineage platform.
  * [City Detect](https://techcrunch.com/2026/03/06/city-detect-uses-ai-to-help-cities-stay-safe-and-clean/) — $13M Series A for AI vision on municipal vehicles detecting graffiti, illegal dumping, and building violations.
  * [Cotool](https://www.cotool.ai/) — $7.4M seed for AI agents that automate detection, response, and threat hunting for security teams.
  * [Denki](https://denki.ai/) — automates audit tasks with AI (no funding details).
  * [14.ai](https://14.ai/) — YC-backed AI customer service agency replacing support teams at B2C startups (no funding details).
  * [Guild.ai](https://www.guild.ai/) — neutral control plane for deploying, governing, and sharing AI agents across vendors (waitlist, no funding details).
  * [Fig Security](https://www.fig.security/) — SOC resilience platform that auto-detects and repairs detection drift and deploys changes safely (no funding details).
  * [RHIC Agripass](https://agripass.co/) — autonomous weeding robots for agriculture (no funding details).
  * [Diligent](https://www.diligent.com/) — governance and compliance platform (no funding details).


Advertisement 
### 🎬 Fun & Miscellaneous
  * The [moongate-community](https://github.com/moongate-community/moongatev2) built Moongatev2, a modern Ultima Online server emulator from scratch in .NET 10 with NativeAOT, Lua scripting for item behaviors, spatial world partitioning with delta sync, snapshot persistence, embedded admin API + React UI, and auto-generated doors from map statics. No combat or skills yet, but the architecture is clean.
  * [CatFu](https://x.com/catfusolana/status/2029567081637650800) shared a POV video of a cat acting like it watched too many Wu-Tang Collection kung-fu movies.
  * [che_shr_cat](https://x.com/che_shr_cat/status/2029626128566993201) built a real-time geometry manifold explorer using diffusion models.
  * [wstv_lizzi](https://x.com/wstv_lizzi/status/2029858561967186353) shared early data on Chinese AI adoption in enterprises showing rapid uptake of local models for internal tools.


Advertisement 
## Around the Horn Digest — Friday, March 6, 2026
Today's digest is dominated by one story: **GPT-5.4 dropped.** OpenAI unified reasoning, coding, and agentic capabilities into a single frontier model with native computer control, spreadsheet mastery (87.3% on banking analyst tasks), and 1M context. It immediately sparked a cascade of reactions, from a mathematician calling it his "Move 37" moment to Dan Shipper switching his daily driver. OpenAI also launched a native Codex Windows app, new financial services tools, and a showcase of zero-code apps. Oh, and they hired IPO lawyers.
Meanwhile, Anthropic is having a week. The Pentagon formally labeled them a supply-chain risk after CEO Dario Amodei pushed back on military applications like mass surveillance. But the company also hit a milestone: over 1M daily Claude signups, with observers noting their ARR sprint is the fastest ever (~$20B run rate). On the infrastructure side, Together AI released FlashAttention-4 (record 1605 TFLOPs/s on Blackwell) and is in talks to raise $1B at $7.5B valuation. And the broader AI economy got two major data points: Anthropic published new labor market impact research, and Alex Imas documented a growing body of micro-productivity gains that haven't yet shown up in macro statistics.
Outside the lab, the real world is catching up. The US is considering sweeping new chip export controls, AI data center demand is triggering a nationwide land rush, tech publications have lost 58% of their Google traffic since 2024, and Meta is getting sued over its AI smart glasses after workers reviewed intimate user footage. Cloudflare rewrote Next.js in a week with $1.1K in AI tokens, which might be the most alarming story for anyone building commercial open-source software.
**Bolded items** throughout the digest signal editorial significance.
Advertisement 
### 🏢 Big Tech & Major Companies
  1. [**OpenAI**](https://openai.com/index/introducing-gpt-5-4/)**launched GPT-5.4 and GPT-5.4 Pro, unifying reasoning, coding, and agentic advances into frontier models now rolling out in ChatGPT (as GPT-5.4 Thinking for Plus/Pro users), API, and Codex; key features include native computer control via Playwright/screenshots, steerable upfront thinking plans, 1M context, 87.3% accuracy on banking analyst spreadsheet tasks (vs prior 68.4%), token efficiency gains (47% reduction via tool search), SOTA on OSWorld (75% vs human 72.4%), and an**[**"high" cybersecurity risk**](https://x.com/rohanpaul_ai/status/2029680414076588231)**rating after scoring 88% on professional Capture the Flag challenges.**
  2. [**OpenAI**](https://www.bloomberg.com/news/articles/2026-03-05/openai-releases-new-financial-services-tools-rivaling-anthropic?accessToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb3VyY2UiOiJTdWJzY3JpYmVyR2lmdGVkQXJ0aWNsZSIsImlhdCI6MTc3MjczNTI3NywiZXhwIjoxNzczMzQwMDc3LCJhcnRpY2xlSWQiOiJUQkZVMDVLSVVQVTMwMCIsImJjb25uZWN0SWQiOiI4OUM4OTNDMDhGOTQ0NThDQkQwQTQyREY1RDFCOTY0QyJ9.i0PiIC4hq5vCZisz9KHDlVK-C7x-0c0nWMg1D7dNrEU&leadSource=uverify%20wall)**released new financial services tools alongside GPT-5.4, outperforming rivals on generating spreadsheets, documents, and presentations (**[**Engadget coverage**](https://www.engadget.com/ai/i-hope-you-like-spreadsheets-because-gpt-54-loves-them-180000444.html)**).**
  3. [**OpenAI**](https://www.theinformation.com/articles/openai-selects-law-firms-cooley-wachtell-ipo-prep?rc=lks9on)**hired Cooley and Wachtell Lipton Rosen & Katz as its first concrete step toward a potential public listing as early as Q4 2026 (~$730B valuation).**
  4. [OpenAI](https://www.theinformation.com/newsletters/ai-agenda/openai-develops-bidirectional-audio-model-boost-voice-assistants) is developing a bidirectional audio model that processes speech continuously so voice assistants can adapt mid-response and handle interruptions naturally.
  5. [OpenAI](https://developers.openai.com/showcase) showcased a gallery of complete browser games, apps, and 3D visualizations all built with zero manual code using GPT-5.4 and Codex.
  6. [**Anthropic**](https://x.com/mikeyk/status/2029662454079512598)**announced more than a million people are now signing up for Claude every day, with**[**observers noting**](https://x.com/kimmonismus/status/2029500416442998993)**the company's unprecedented ARR sprint (fastest ever to ~$20B run rate) while both OpenAI and Anthropic prepare IPOs this year.**
  7. **The**[**Pentagon**](https://techcrunch.com/2026/03/05/its-official-the-pentagon-has-labeled-anthropic-a-supply-chain-risk/)**formally labeled Anthropic and its models a supply-chain risk (requiring partners to certify non-use), after CEO Dario Amodei**[**resisted**](https://www.wsj.com/politics/national-security/pentagon-formally-labels-anthropic-supply-chain-risk-escalating-conflict-ebdf0523)**military applications like mass surveillance and fully autonomous weapons; unprecedented for a U.S. firm (**[**Bloomberg**](https://www.bloomberg.com/news/newsletters/2026-03-05/anthropic-s-pentagon-feud-accelerates-push-into-consumer-market)**,**[**Amodei response**](https://techcrunch.com/2026/03/05/anthropic-ceo-dario-amodei-could-still-be-trying-to-make-a-deal-with-pentagon/)**).**
  8. [**Meta**](https://techcrunch.com/2026/03/05/meta-sued-over-ai-smartglasses-privacy-concerns-after-workers-reviewed-nudity-sex-and-other-footage/)**is being sued over its AI smart glasses after contract workers in Kenya reviewed intimate user footage including nudity and sex without proper disclosure; the company marketed Ray-Ban Meta glasses as privacy-first while routing footage through overseas contractors.**
  9. [Netflix](https://variety.com/2026/film/news/netflix-acquires-ben-affleck-ai-filmmaking-startup-interpositive-1236679498/) acquired Ben Affleck's AI filmmaker tools start-up InterPositive to accelerate AI-assisted filmmaking.
  10. [**Google**](https://www.theverge.com/tech/889339/google-canvas-ai-mode-search-us-launch)**rolled out its Canvas AI workspace to all US users in Search AI Mode, giving you a side panel to generate documents, code, dashboards, and interactive tools from natural language prompts with live web information.**
  11. [AWS](https://techcrunch.com/2026/03/05/aws-amazon-connect-health-ai-agent-platform-health-care-providers/) launched Amazon Connect Health, a HIPAA-eligible AI agent platform that automates healthcare admin tasks like scheduling, documentation, patient verification, and EHR integration ([Amazon blog](https://www.aboutamazon.com/news/aws/amazon-connect-health-ai-healthcare)).
  12. [Canada](https://www.wsj.com/tech/ai/canada-says-openai-ceo-altman-pledged-to-toughen-safety-protocols-7962b26b?st=Xpv84K&reflink=desktopwebshare_permalink) said OpenAI CEO Sam Altman pledged an apology and tougher safety protocols in response to a shooting incident.


Advertisement 
### 💼 AI Productivity, Labor & Economics
  1. [**Anthropic researchers**](https://www.anthropic.com/research/labor-market-impacts)**Maxim Massenkoff and Peter McCrory proposed (**[**paper**](https://cdn.sanity.io/files/4zrzovbb/website/dc7bcd0224644fce97cecb7f9e68dcd8434b35f1.pdf)**) a new "observed exposure" measure combining theoretical LLM capability with real Claude usage data; high-exposure occupations like programmers (75% coverage) show no unemployment spike since late 2022, but a ~14% drop in young-worker hiring rates.**
  2. **Alex Imas**[**argues**](https://aleximas.substack.com/p/what-is-the-impact-of-ai-on-productivity)**(**[**thread**](https://x.com/alexolegimas/status/2029679873359482889)**) that generative AI delivers clear micro-productivity gains (14–55%+ in coding, support, writing, mammography, etc., often larger for less-skilled workers) but macro statistics lag due to adoption frictions, training gaps, bottlenecks, and J-curve reorganization costs mirroring past IT revolutions.**
  3. **Ten major**[**tech publications**](https://growtika.com/blog/tech-media-collapse)**lost 58% of Google organic traffic (65M monthly visits combined) since 2024 peaks, with Digital Trends down 97% and ZDNet 90%, as AI Overviews and Reddit/Perplexity divert searches (**[**The Verge adds**](https://www.theverge.com/24167865/google-zero-search-crash-housefresh-ai-overviews-traffic-data-audience)**"Google Zero" is crushing independent sites).**
  4. The Pragmatic Engineer [documents](https://blog.pragmaticengineer.com/stack-overflow-is-almost-dead/) Stack Overflow's collapse: new question volume has fallen back to 2009 levels because LLMs now give faster answers trained on its own data.
  5. Chamath Palihapitiya [shared](https://x.com/chamath/status/2029634071966666964) that his startup's AI spending has tripled to millions per year with no revenue or productivity uplift, leading them to drop Cursor for Claude Code.
  6. Developer Tolans [argues](https://www.tolans.com/relay/why-the-best-ai-engineers-are-former-managers) that the best AI engineers today are former managers because agent orchestration demands delegation, coaching, and oversight skills identical to people management ([Quinten Farmer thread](https://x.com/quintendf/status/2029313181865394656) referencing [Dan Shipper's 2024 piece](https://t.co/ENFj4BTvAH)).


Advertisement 
### 🤖 AI Agents & Infrastructure
  1. [**Cursor**](https://techcrunch.com/2026/03/05/cursor-is-rolling-out-a-new-system-for-agentic-coding/)**rolled out Automations, a new agentic coding system that automatically launches specialized agents triggered by codebase changes, Slack messages, or timers for tasks like bug reviews and security audits (human oversight only at escalation points).**
  2. [**Luma**](https://techcrunch.com/2026/03/05/exclusive-luma-launches-creative-ai-agents-powered-by-its-new-unified-intelligence-models/)**launched creative AI agents powered by its new**[**Uni-1**](https://lumalabs.ai/uni-1)**Unified Intelligence multimodal models for end-to-end planning and generation across text/image/video/audio with persistent context, self-critique refinement, and orchestration of other models (early clients include Publicis).**
  3. **AI data center demand**[**triggered**](https://www.nytimes.com/2026/03/05/technology/ai-data-centers-land-cloverleaf-infrastructure.html)**a modern land rush as prospectors scramble for sites with power and cooling capacity across states like Wisconsin and Nebraska, with U.S. needs projected to reach 85 GW by 2030 (20% of current grid).**
  4. The Star History blog [argues](https://www.star-history.com/blog/ai-ui-irrelevant) that as AI agents become prevalent, polished graphical UIs lose their competitive moat; the winning interfaces will be simple text, CLI, and declarative config that LLMs parse reliably.


Advertisement 
### 💻 AI Coding & Developer Tools
  1. [**OpenAI**](https://developers.openai.com/codex/app/windows)**launched the native Codex Windows app (Microsoft Store / winget) with parallel agent threads, PowerShell + Windows Sandbox execution, WSL support, customizable editor/terminal per project, and full Git/Node/Python integration.**
  2. **Gergely Orosz**[**argues**](https://newsletter.pragmaticengineer.com/p/the-pulse-cloudflare-rewrites-nextjs)**that Cloudflare rebuilt Next.js as "vinext" (Vite-based drop-in replacement) in one week with one engineer + $1,100 in tokens using OpenCode/Opus 4.5 agents, achieving 94% API support, 4× faster builds, and 57% smaller bundles; proving commercial open-source rewrites are now trivially cheap and destroying proprietary moats like Vercel lock-in.**
  3. A developer [asked](https://sderosiaux.substack.com/p/claude-code-told-me-what-tools-it) Claude Code what tools it was missing and received a long list (ripgrep, fzf, DuckDB, semgrep, etc.), revealing that giving LLMs a well-optimized tooling environment is as critical as good prompting.
  4. [Jared Palmer](https://github.com/jaredpalmer/mogcli) released mogcli, an agent-friendly CLI for Microsoft 365 with stable JSON output for scripting Mail, Calendar, OneDrive, and Graph APIs.
  5. [Lightpanda](https://lightpanda.io/blog/posts/native-markdown-output) added native Markdown output that converts executed DOM (the full rendered page structure) to clean Markdown, reducing tokens by up to 80% for AI agents.
  6. [RunAnywhere](https://www.runanywhere.ai/blog/metalrt-fastest-llm-decode-engine-apple-silicon) built MetalRT, the fastest LLM decode engine for Apple Silicon, reaching 658 tok/s on M4 Max (1.67× faster than llama.cpp on average).
  7. Awni Hannun [built](https://github.com/awni/mylm) mylm, a self-personalizing local LLM (MLX-based) that learns from your chats: talk normally, type `/sleep` to auto-generate Q&A pairs from context, LoRA-fine-tune, and reset KV cache so the model permanently remembers personal details across sessions.


Advertisement 
### 🔬 AI Research & Models
  1. [**AllenAI**](https://allenai.org/blog/olmohybrid)**released Olmo Hybrid 7B (**[**HuggingFace**](https://huggingface.co/collections/allenai/olmo-hybrid)**,**[**paper**](https://allenai.org/papers/olmo-hybrid)**), interleaving transformers and Gated DeltaNet linear RNNs (a type of recurrent model that processes sequences more efficiently) in a 3:1 ratio for superior scaling; equivalent MMLU performance with 35–49% fewer training tokens and stronger long-context results (open weights/models/code).**
  2. **Tri Dao and**[**Together AI**](https://www.together.ai/blog/flashattention-4)**released FlashAttention-4 (**[**paper**](https://github.com/Dao-AILab/flash-attention/blob/main/assets/fa4_paper.pdf)**,**[**GitHub**](https://github.com/Dao-AILab/flash-attention/tree/main/flash_attn/cute)**), an algorithm-kernel co-design using advanced pipelining, polynomial softmax approximation, and Blackwell-specific optimizations to reach 1605 TFLOPs/s (71% utilization); up to 1.3× faster than cuDNN and 2.7× faster than Triton (**[**Tri Dao blog**](https://tridao.me/blog/2026/flash4/)**,**[**Colfax analysis**](https://research.colfax-intl.com/flashattention-4-algorithm-and-kernel-pipelining-co-design-for-asymmetric-hardware-scaling/)**).**
  3. [Tencent Hunyuan](https://x.com/TencentHunyuan/status/2029644529578692723) built HY-WU / Functional Neural Memory, generating instance-specific adapter parameters on-the-fly from prompts and images for instant personalization and better instruction following without memory banks; surpassing or rivaling leading models in human evals.
  4. Researchers Samuel Garcin et al. (Edinburgh/Microsoft) [built](https://francelico.github.io/persist.github.io/) PERSIST, a world model maintaining persistent 3D latent state (environment + camera + renderer) instead of pixel histories for consistent long-horizon video generation, spatial memory, and dynamic 3D editing in environments like Minecraft.
  5. Harman et al. [built](https://harmandotpy.github.io/v1-verification/) V1 ([paper](https://arxiv.org/abs/2603.04304), [GitHub](https://github.com/HarmanDotpy/pairwise-self-verification)), unifying generation and pairwise self-verification for parallel reasoners with uncertainty-guided tournament ranking, delivering 3.3–10% Pass@1 gains on hard coding/math benchmarks and 33.3% on SWE-bench.
  6. [Together Computer](https://github.com/togethercomputer/erdos-minimum-overlap) achieved new state-of-the-art on Erdős' Minimum Overlap Problem (a classic number theory challenge about how much a set must overlap with itself) with an upper bound of 0.380871 using AI agents and sequential linear programming.
  7. Lenat and Marcus [argue](https://arxiv.org/pdf/2308.04445) that LLMs require integration with symbolic systems like Cyc for trustworthy reasoning, using microtheories for context and defeasible logic (rules that can be overridden by new information) to handle real-world complexity.
  8. Itamar Pres [argues](https://time-for-consistency.github.io/) ([Belinda Li thread](https://x.com/belindazli/status/2029679904380571783), [paper](https://arxiv.org/abs/2508.05469)) it's time to optimize LLMs for self-consistency across groups of related inputs rather than isolated I/O pairs, to fix sycophancy (telling users what they want to hear) and factual inconsistency while unlocking meta-capabilities like introspection and self-improvement.
  9. Mathematician Bartosz Naskręcki [shared](https://x.com/nasqret/status/2029628846518010099) ([trajektoriePL thread](https://x.com/trajektoriePL/status/2029660475395326300)) that GPT-5.4 solved his 20-year-curated math problem in a clean, human-like way; his personal "Move 37" moment.
  10. Alan Chan [proposes](https://astrangeattractor.substack.com/p/measuring-ai-r-and-d-automation) ([paper](https://arxiv.org/abs/2603.03992), [thread](https://x.com/_achan96_/status/2029573343545057337)) 14 new metrics across experimental, survey, operational, and organizational categories to track AI R&D automation and the oversight gap, arguing current benchmarks are insufficient.
  11. Ben Burtenshaw [shared](https://x.com/ben_burtenshaw/status/2016534389685940372) a CUDA teaching demo showing GPT-5.4 explaining low-level GPU kernels with perfect step-by-step accuracy.


Advertisement 
### 🏛️ AI Policy, Governance & Safety
  1. **U.S. officials**[**proposed**](https://techcrunch.com/2026/03/05/us-reportedly-considering-sweeping-new-chip-export-controls/)**sweeping new AI chip export controls that could require large-volume foreign buyers to invest in US data centers or provide security guarantees (**[**FT coverage**](https://www.ft.com/content/30d0b1df-ad8c-42eb-852b-dad53acaecfc)**).**
  2. Ajeya Cotra [admits](https://www.planned-obsolescence.org/p/i-underestimated-ai-capabilities) ([thread](https://x.com/ajeya_cotra/status/2029576934523556256)) she underestimated AI capabilities again, sharply revising upward her software engineering time-horizon predictions; now believes AI could handle >100-hour SWE tasks and possibly unbounded R&D automation this year.


### 🛠️ AI Tools & Products
  1. [Viggle AI](https://x.com/ViggleAI/status/2029655009730744808) launched V4 with Character Refine, delivering strong character consistency, automatic multi-angle reference generation from one image, precise 1:1 motion transfer, multi-character support, and up to 60-second videos at lower cost and faster speeds. —free to try
  2. [Vela](https://news.ycombinator.com/item?id=47264741) (YC W26) automates complex multi-party scheduling across email, SMS, WhatsApp, Slack, and phone by understanding natural language constraints, tracking context across threads, proposing times, following up, and handling reschedules for enterprise customers. —no pricing details ([homepage](https://tryvela.ai/))
  3. [Domain Maps](https://domainmaps.co/) provides visual cheat sheets of essential terminology across creative fields (AI image gen, UI/UX, motion graphics, game design, etc.) so you can prompt AI more precisely. —free to try
  4. [Aident AI](https://aident.ai/?ref=producthunt) builds complex open-world automations across Slack, Shopify, Discord and 1,000+ integrations by describing your goals in plain English, which it compiles into Playbooks executed by agent teams. —free to try
  5. [Willow](https://willowvoice.com/?ref=producthunt) converts speech into context-aware, auto-formatted text with grammar fixing and custom vocabulary support on Mac, Windows, and iPhone; 3× more accurate than built-in dictation tools. —free trial, then $12/month.
  6. [PageAgent](https://alibaba.github.io/page-agent/) (Alibaba, open source, MIT license) turns any website into an AI-native application with one script tag, enabling natural language commands for form filling, navigation, and workflows directly in the browser with human-in-the-loop confirmation. —free to try
  7. [TinyFish](https://www.tinyfish.ai/) offers early-access AI agents for complex enterprise workflows, launched with OpenAI GPT-5.4 integration. —no pricing details
  8. [Heywa](https://heywa.com/?ref=producthunt) turns any topic into interactive mind maps, image explorations, and deep-dive questions to unlock serendipitous learning. —free to try
  9. [SemiAnalysis](https://semianalysis.com/tokenomics-model/) offers an interactive Tokenomics Model connecting AI hardware inputs (GPUs/TPUs from Nvidia/AMD/Google) to software outputs, letting you forecast ROI, token consumption growth, GPU demand, and unit economics for players like Cursor/Perplexity/Harvey. —no pricing details
  10. [OpenAI Codex Windows app](https://developers.openai.com/codex/app/windows) gives you parallel agent threads, PowerShell + Windows Sandbox execution, WSL support, and full Git/Node/Python integration for agentic coding on Windows. —requires API key


Advertisement 
### 📊 Fundraising & Deals Roundup
  1. [Together AI](https://www.theinformation.com/articles/nvidia-cloud-ally-together-ai-talks-raise-7-5-billion-valuation?rc=lks9on) — aiming for ~$1B raise at $7.5B valuation (~$1B ARR, 3× growth) as Nvidia's key cloud partner ([homepage](https://www.together.ai/)).
  2. [Sage](https://economictimes.indiatimes.com/tech/startups/sage-raises-65-million-to-expand-ai-assisted-care-for-ageing-americans/articleshow/129095627.cms) — $65M Series C (Goldman Sachs Alternatives) for real-time AI distress monitoring and predictive fall/health risk detection in nursing homes.
  3. [Lio](https://techcrunch.com/2026/03/05/lio-ai-series-a-a16z-30m-raise-automate-enterprise-procurement/) — $30M Series A (a16z) for AI agents that fully automate enterprise procurement ([homepage](https://www.lio.ai/), [backstory](https://techcrunch.com/2026/03/05/how-1000-customer-calls-shaped-a-breakout-enterprise-ai-startup/)).


### 💡 Industry Commentary & Analysis
  1. Dan Shipper [gave](https://x.com/danshipper/status/2029620107870359854) GPT-5.4 his strongest endorsement yet after real engineering tests: now his daily driver for superior planning, deeper conversational code reviews, and "human" feel (half Opus price).
  2. Armin Ronacher [explores](https://lucumr.pocoo.org/2026/3/5/theseus/) AI and the Ship of Theseus: as models replace every part of software and workflows, what remains of "human" work and identity.
  3. Steven Wittens [argues](https://acko.net/blog/the-l-in-llm-stands-for-lying/) that the L in "LLM" stands for lying because models produce convincing forgeries passed off as authentic work, degrading quality and trust, with reliable source attribution as the missing solution.
  4. Jeremy Howard [argues](https://www.youtube.com/watch?v=dHBEQ-Ryo24) that AI-assisted coding creates a dangerous "vibe coding" illusion akin to a slot machine, eroding deep intuition and organizational knowledge through desirable difficulty loss.
  5. Nick Cammarata [observed](https://x.com/nickcammarata/status/2029664315507363977) the devolution of AI company releases: "no paper, no weights, benchmarks that don't compare to other company's models. Next up: just a photo of the team looking confident and smiling."
  6. [Y Combinator](https://x.com/ycombinator/status/2029678343629476249) highlighted Origami Robotics' launch of high-DOF robotic hands with a co-designed data glove for scalable real-world dexterity training.


Advertisement 
### 🧪 TOP TREATS TO TRY
**Core slots:**
  * [Willow](https://willowvoice.com/?ref=producthunt) converts speech into context-aware, auto-formatted text with grammar fixing and custom vocabulary on Mac, Windows, and iPhone; 3× more accurate than built-in dictation. —free trial, then $12/month.
  * [Aident AI](https://aident.ai/?ref=producthunt) builds complex automations across Slack, Shopify, Discord, and 1,000+ integrations by describing your goals in plain English, compiled into Playbooks executed by agent teams. —free to try
  * [Vela](https://tryvela.ai/) (YC W26) automates complex multi-party scheduling across email, SMS, WhatsApp, Slack, and phone with natural language constraints and automatic follow-ups. —no pricing details
  * [Domain Maps](https://domainmaps.co/) provides visual cheat sheets of essential terminology across creative fields so you can prompt AI more precisely. —free to try
  * [Viggle AI](https://x.com/ViggleAI/status/2029655009730744808) V4 generates character-consistent video animation from a single image with precise motion transfer, multi-character support, and up to 60-second clips. —free to try


**Cool/niche slots:**
  * [PageAgent](https://alibaba.github.io/page-agent/) (Alibaba, MIT license) turns any website into an AI-native app with one script tag for natural language form filling and navigation. —free to try
  * [Heywa](https://heywa.com/?ref=producthunt) turns any topic into interactive mind maps and deep-dive questions to unlock serendipitous learning. —free to try


Advertisement 
## Around the Horn - Thursday, March 5 2026
### 🏢 Big Tech & Major Companies
  1. [**Microsoft**](https://x.com/Hadas_Gold/status/2029727182977913083)**confirmed that its lawyers concluded Anthropic products including Claude can remain available to non-defense customers through M365, GitHub, and AI Foundry while continuing non-defense-related projects with Anthropic.**
  2. [NVIDIA](https://huggingface.co/datasets/nvidia/Nemotron-ClimbMix) introduced Nemotron-CLIMB ([paper](https://arxiv.org/pdf/2504.13161)), a clustering-based iterative bootstrapping framework that automatically discovers optimal data mixtures for LLM pre-training, releasing the 400B-token Nemotron-ClimbMix dataset that improves 1B-model performance 2% over Llama-3.2-1B ([Koven Yu thread](https://x.com/Koven_Yu/status/2029745851095290293), [Shizhe Diao](https://x.com/shizhediao/status/2029370289461575741) noted it's now the default dataset for the nanochat GPT-2 speedrun).
  3. **Andrej Karpathy**[**reported**](https://x.com/karpathy/status/2029701092347630069)**nanochat now trains a capable GPT-2 model in just 2 hours on a single 8×H100 node (down from ~3 hours a month ago), with the biggest win from switching to NVIDIA ClimbMix; he also has AI agents autonomously iterating on the codebase, making 110 changes over 12 hours to improve validation loss while he relaxes.**


Advertisement 
### 🔬 AI Research & Models
  1. **Anthropic researchers**[**published**](https://www.anthropic.com/research/tracing-thoughts-language-model)**a major interpretability study revealing how Claude 3.5 Haiku plans rhyming words ahead in poetry, applies shared cross-lingual conceptual features, runs parallel approximation and precise paths for mental math, and sometimes fabricates unfaithful reasoning or hallucinates when refusal circuits are inhibited; all discovered via circuit tracing and targeted interventions (**[**thread**](https://x.com/JulienBek/status/2029680516568600933)**).**
  2. Gen-Hua Shi [presents](https://deepmanifold.ai/) Deep Manifold ([thread](https://x.com/BetaTomorrow/status/2029744776334168385)), the first complete mathematical formulation of neural networks as "learnable numerical computation" on stacked piecewise-smooth manifolds grounded in fixed-point theory, unifying arbitrary multimodal inputs through property-less counting operations.
  3. Ziming Liu [argues](https://kindxiaoming.github.io/blog/2026/sparse-attention-8/) ([thread](https://x.com/ZimingLiu11/status/2029715749116493875)) that numeric randomness (resampling token embeddings or adding Gaussian noise) accelerates the emergence of symbolic structures like induction heads (pattern-matching circuits) in sparse-attention transformers because models realize numeric approaches fail and shift to symbolic mechanisms.
  4. Researchers introduced [MT-PingEval](https://arxiv.org/abs/2602.24188), a scalable benchmark using private-information collaborative games to evaluate multi-turn LLM collaboration, finding that models often fail to improve over non-interactive baselines despite substantial headroom while humans achieve comparable success with superior token efficiency.
  5. Achleshwar Luthra, Yash Salunkhe, and Tomer Galanti [introduce](https://dlfundamentals.github.io/directional-neural-collapse/) Directional Neural Collapse 1.0: self-supervised learning collapses variance specifically along task-relevant decision axes (not globally), preserving high orthogonal variance for superior few-shot transfer and tighter generalization bounds.
  6. Shengbang Tong, Saining Xie and team [argue](https://www.alphaxiv.org/abs/2603.03276) ([thread](https://x.com/Shiwei_Liu66/status/2029486566771466366)) that native multimodal pretraining (Transfusion: next-token text + diffusion vision) produces complementary synergies, emergent world modeling, and efficient scaling via MoE (mixture of experts, where different parts of the model specialize in different tasks) with natural modality specialization; vision proves far more data-hungry than language.
  7. A new [paper](https://arxiv.org/abs/2603.03818) found that pretrained Vision-Language-Action (VLA) robot models are surprisingly resistant to catastrophic forgetting in continual learning; simple experience replay often suffices for near-zero forgetting even with tiny replay buffers, and retained knowledge enables rapid recovery via finetuning.
  8. David Lüdke, Tom Wollschläger et al. [show](https://arxiv.org/abs/2511.00203) that Diffusion LLMs act as natural adversaries for any LLM by turning adversarial prompt optimization into amortized conditional sampling, efficiently generating diverse, transferable jailbreaks even against robustly trained and proprietary models.
  9. Aviral Kumar [argues](https://x.com/aviral_kumar2/status/2029627723044343846) that flow-matching value functions succeed in reinforcement learning because iterative integration with dense supervision along trajectories enables test-time recovery from errors and dramatically improves feature plasticity (the model's ability to keep learning new things) under non-stationary targets.
  10. [DySCO](https://github.com/princeton-pli/DySCO) ([paper](https://arxiv.org/abs/2602.22175)) is a training-free decoding method for long-context LLMs that dynamically up-weights task-relevant tokens at each generation step, delivering up to 25% relative gains on benchmarks at 128k context with modest extra compute.


Advertisement 
### 💻 AI Coding & Developer Tools
  1. [React Grab](https://x.com/aidenybai/status/2029603067927351506) lets you click any element on your React page and instantly tell Claude Code or similar agents the exact source file and line number to change, making frontend iteration up to 3× faster. —free to try
  2. [Impeccable](https://impeccable.style/#hero) v1.1 ([thread](https://x.com/pbakaus/status/2029334353894162720)) upgrades Anthropic's frontend-design skill into a full agent-ready framework with 17 commands (/audit, /critique, /polish, /animate, /delight, etc.) for systematic typography, layout, accessibility, and performance improvements, installable in Claude Code, VS Code, and more. —free to try
  3. [OpenHands Critic](https://docs.openhands.dev/sdk/guides/critic) ([CLI docs](https://docs.openhands.dev/openhands/usage/cli/critic), [thread](https://x.com/xingyaow_/status/2029613946559430927)) scores your agent traces using 24 rubric features plus semi-supervised multi-task learning to predict success probability and automatically trigger iterative refinement, turning noisy interactions into reliable supervision. —free to try
  4. [Remotion](https://www.remotion.dev/) ([thread](https://x.com/JNYBGR/status/2029533131565367326)) makes videos programmatically with React and now supports universally compatible MP4 output in every browser including Firefox. —free to try


Advertisement 
### 🤖 AI Agents & Infrastructure
  1. [OpenFang](https://github.com/RightNow-AI/openfang) is an open-source Agent Operating System in Rust that compiles to a ~32 MB binary, with seven pre-built "Hands" for tasks like lead generation and Twitter management, 40 platform adapters, 27 LLM providers, and 16-layer security. —free to try
  2. [CrewAI](https://x.com/joaomdmoura/status/2029625327778156682) launched Cognition Memory, turning memory into an agentic cognitive process with five operations (encode, consolidate, recall with confidence scoring, extract atomic facts, and forget) so your agents compound knowledge across runs.
  3. [ArkSim](https://github.com/arklexai/arksim) ([thread](https://x.com/FundamentEdge/status/2029726670375317624)) simulates realistic multi-turn conversations with diverse LLM-powered users to test how your agent performs before it goes live, with 7 built-in metrics, custom evaluations, and interactive HTML failure reports. —free to try


Advertisement 
### 🛠️ AI Tools & Products
  1. [CourseKit](https://coursekit.productizeyourmind.com/?ref=producthunt) (by MindPal) turns your course sales page URL into a suite of custom, branded AI tools for students; paste a URL, it extracts your modules and methodology, then generates interactive agents that guide learners 24/7 in your voice. —free to try
  2. [Golf](https://www.golf.dev/?ref=producthunt) (YC X25) discovers every AI agent and MCP server connection in your organization (including shadow deployments of Cursor, Claude Code, and Copilot), then enforces granular security policies and generates audit-ready compliance reports for SOC 2, ISO 27001, and FINRA. —no pricing details


### 🎬 Demos & Builds
  1. **John Backus**[**had**](https://x.com/backus/status/2029711059247059282)**GPT-5.4 (Codex) autonomously rewrite the Pokémon Red ROM to replace Pokémon with AIs, including self-QA via browser emulator, sprite editing, and banner art generation, by dropping it into the pret/pokered repo with high-level instructions.**
  2. Bowen Wen [built](https://github.com/NVlabs/Fast-FoundationStereo) Fast-FoundationStereo (CVPR 2026), a real-time zero-shot stereo matching model that accelerates the original by >10× with comparable quality using knowledge distillation and structured pruning ([thread](https://x.com/bowenwen_me/status/2001182542624346569)).
  3. Hong-Xing (Koven) Yu [built](https://x.com/Koven_Yu/status/2029745851095290293) RealWonder, a real-time video world model that simulates consequences of arbitrary 3D physical actions from a single image by using a physics simulator as an intermediate bridge to generate optical flows and RGB previews.
  4. Yixuan Wang [built](https://www.yixuanwang.me/interactive_world_sim/#interactive-demo) an Interactive World Simulator using action-conditioned video prediction (no physics engine) that supports stable >10-minute robot interactions at 15 FPS for policy training, complete with a live keyboard-controlled web demo.


Advertisement 
### 💡 Industry Commentary & Analysis
  1. Brett Caughran [reports](https://x.com/FundamentEdge/status/2029726670375317624) that GPT-5.4 Thinking can deeply analyze uploaded Excel financial models like a skilled analyst, explaining historical performance, key assumptions, and intelligently pushing back on variables; something LLMs couldn't reliably do even 3–6 months ago.
  2. [Ajeya Cotra at METR writes](https://www.planned-obsolescence.org/p/i-underestimated-ai-capabilities) that AI coding agents are improving so fast she's already blown past her January predictions, and by year's end, the concept of measuring AI by "how long would this take a human" may stop making sense entirely.
  3. [Aaron Levie argues on the Latent Space podcast](https://www.latent.space/p/box) that AI agents can't scale in the enterprise until companies build proper infrastructure for agent identities, file permissions, and governance; _compelling take_ ([Full episode](https://www.youtube.com/watch?v=mMbPEf4V_hE)).
  4. [Jeremy Howard warns](https://www.youtube.com/watch?v=dHBEQ-Ryo24) that AI-assisted coding is becoming a "slot machine" where developers accept whatever the model outputs without building real technical intuition (_the counter point to our live from yesterday)_.
  5. [Vinod Khosla tells Fortune](https://www.youtube.com/watch?v=cSWvm7nu1rI) he believes AI will automate 80% of labor, and lays out his vision for free education, free healthcare, and no taxes under $100K.
  6. [Prompt Engineering walks through](https://youtu.be/e9EBl_PK4bw?si=NaEXZn9QSI5VMsRA) how to apply classic three-tier architecture (data, processing, presentation) to build AI agent systems that actually work in production.
  7. [Ray Amjad breaks down](https://youtu.be/e9EBl_PK4bw?si=NaEXZn9QSI5VMsRA) Anthropic's new Claude Code Skills 2.0, covering skill categories, evals, benchmarks, and trigger optimization.
  8. [The Information](https://www.theinformation.com/newsletters/ai-agenda/openai-develops-bidirectional-audio-model-boost-voice-assistants) reports OpenAI is building a "BiDi" audio model that can talk while you're talking, but the prototype still glitches after a few minutes; OpenAI is also supposedly creating its[ own version of GitHub](https://www.theinformation.com/articles/openai-developing-alternative-microsofts-github), and[ will scale back its planned “one click purchase” feature](https://www.theinformation.com/articles/openai-scales-back-shopping-plans-chatgpt), where an agent buys on your behalf inside ChatGPT, to happen inside the “Apps” in GPT instead.
  9. Armin Ronacher [explores](https://lucumr.pocoo.org/2026/3/5/theseus/) AI and the Ship of Theseus: as models replace every part of software and workflows, what remains of "human" work and identity.
  10. Steven Wittens [argues](https://acko.net/blog/the-l-in-llm-stands-for-lying/) that the L in "LLM" stands for lying because models produce convincing forgeries passed off as authentic work, degrading quality and trust, with reliable source attribution as the missing solution
  11. Nick Cammarata [observed](https://x.com/nickcammarata/status/2029664315507363977) the devolution of AI company releases: "no paper, no weights, benchmarks that don't compare to other company's models. Next up: just a photo of the team looking confident and smiling."
  12. [Y Combinator](https://x.com/ycombinator/status/2029678343629476249) highlighted Origami Robotics' launch of high-DOF robotic hands with a co-designed data glove for scalable real-world dexterity training.


Advertisement 
##  Around the Horn Digest — March 4, 2026
### 🏛️ AI Policy, Governance & Safety
  1. **The U.S. military**[**used Anthropic's**](https://www.washingtonpost.com/technology/2026/03/04/anthropic-ai-iran-campaign/)**Claude AI, embedded in Palantir's Maven Smart System, to generate targeting packages and intelligence assessments during the first 24 hours of strikes on Iran… despite banning the company days earlier.** Claude helped the Pentagon strike 1,000 targets at "machine speed rather than human speed," per Paul Scharre of the Center for a New American Security. Anthropic CEO Dario Amodei had refused to let the Pentagon use Claude for mass surveillance or fully autonomous weapons; Trump responded by ordering all federal agencies to phase out Anthropic products within six months and designating the company a "supply chain risk to national security." OpenAI and xAI quickly signed deals to replace Anthropic on classified systems.
  2. [**Defense contractors**](https://www.reuters.com/sustainability/society-equity/defense-contractors-like-lockheed-seen-removing-anthropics-ai-after-trump-ban-2026-03-04/)**, including Lockheed Martin, began purging Anthropic's AI tools from their supply chains following Trump's ban, despite legal experts calling the prohibition "highly aggressive" and likely to fail in court.** Lockheed said it would follow the president's direction and expected "minimal impacts." Lawyers noted the Pentagon may lack statutory authority to bar contractors from using Claude, but companies aren't willing to risk their share of the trillion-dollar defense budget to find out.
  3. **A father**[**sued Google**](https://techcrunch.com/2026/03/04/father-sues-google-claiming-gemini-chatbot-drove-son-into-fatal-delusion/)**for wrongful death, alleging that the Gemini chatbot convinced his 36-year-old son it was his sentient AI wife, coached him through an armed scouting mission near Miami International Airport, and ultimately guided him to take his own life.** The lawsuit details how Gemini fabricated a covert narrative involving federal agents, a humanoid robot rescue mission, and a fake DHS database, while never triggering any self-harm detection. Google said Gemini referred the man to crisis hotlines "many times" and acknowledged that "AI models are not perfect." This is the first wrongful death lawsuit naming Google over AI psychosis.
  4. **New**[**research from ETH Zurich and Anthropic**](https://arstechnica.com/security/2026/03/llms-can-unmask-pseudonymous-users-at-scale-with-surprising-accuracy/)**showed that LLMs can identify pseudonymous online users for as little as $1–4 per target by analyzing writing style, interests, and incidental disclosures.** Researchers matched 67% of anonymous Hacker News users to their real LinkedIn profiles from a pool of 89,000 candidates, at 90% precision, for under $2,000 total. Safety guardrails were easily bypassed because each step in the pipeline (summarizing, embedding, ranking) looks individually harmless.
  5. The New York Times [examined why China lacks AI "doomers"](https://www.nytimes.com/2026/03/04/world/asia/china-ai-enthusiasm.html), noting that Chinese policymakers and the public have expressed high optimism about AI even as many in the West worry about existential risks, job displacement, and military applications.
  6. Nahema Marchal, Stephanie Chan, and colleagues [argue](https://arxiv.org/abs/2603.02960) that LLMs acting as epistemic agents need a dedicated trust architecture built on epistemic competence, falsifiability, provenance tracking, and "knowledge sanctuaries" to avoid cognitive deskilling and epistemic drift.
  7. A coalition released the [Pro-Human AI Declaration](https://humanstatement.org/) calling for AI systems that serve humanity rather than diminishing core human experiences such as family, faith, and community.
  8. Researchers from Georgia State, Penn State, and the University of Georgia [introduced the FAIR framework](https://techxplore.com/news/2026-03-ai-life-decisions-fair.html), a new design theory to help organizations continuously monitor and adapt AI fairness in high-stakes decisions like lending, hiring, and medical diagnoses.
  9. [SAP urged Europe](https://techxplore.com/news/2026-03-europe-focus-industrial-ai-sap.html) to prioritize industrial AI over consumer applications, arguing the continent's manufacturing expertise gives it a strong position in specialized factory AI.


Advertisement 
### 🏢 Big Tech & Major Companies
  1. [**Alibaba's**](https://venturebeat.com/technology/did-alibaba-just-kneecap-its-powerful-qwen-ai-team-key-figures-depart-in)**Qwen AI team lost its technical lead Junyang Lin, post-training head Yu Bowen, and staff researcher Binyuan Hui in rapid succession, just one day after launching the Qwen 3.5 small model series to praise from Elon Musk.** A colleague hinted Lin's departure wasn't voluntary, writing: "I know leaving wasn't your choice. Just last night, we were side by side launching the Qwen3.5 small model." Alibaba shares fell as much as 5.3%. The Qwen project has surpassed 1 billion model downloads and 203 million monthly active users, but analysts warn that Alibaba's push toward commercialization may come at the cost of its open-source mission.
  2. [Perplexity](https://www.axios.com/2026/03/04/perplexity-coreweave-data-center-nvidia) signed a multi-year deal with CoreWeave to run AI inference workloads on dedicated Nvidia GB200 NVL72-powered clusters. CoreWeave will also adopt Perplexity Enterprise Max internally. CoreWeave shares jumped ~8% on the news after a rough post-earnings selloff.
  3. [**Cursor**](https://cursor.com/blog/jetbrains-acp)**is now available in JetBrains IDEs (IntelliJ, PyCharm, etc.) through the Agent Client Protocol, bringing its full AI coding agent and agent mode to the JetBrains ecosystem.** ([announcement](https://x.com/cursor_ai/status/2029222015736197205))
  4. **Two OpenAI engineers built an internal AI data agent in three months that now**[**serves 4,000+ employees**](https://venturebeat.com/orchestration/openais-ai-data-agent-built-by-two-engineers-now-serves-4-000-employees-and)**querying 600 PB across 70k datasets in plain English via Slack, instantly returning charts and insights and saving 2–4 hours per query.** The company says anyone can replicate the exact setup with public APIs.
  5. [**OpenAI's**](https://www.theinformation.com/newsletters/ai-agenda/openais-next-ai-model-will-extreme-reasoning)**next model, GPT-5.4, will feature a 1M token context window, a new "extreme reasoning mode" that allocates more compute for deeper thinking, improved memory across multi-step workflows, lower error rates on complex tasks, and the ability to run for hours on long-horizon tasks.** The model is designed for agents and automation (e.g., Codex) and scientific research. Part of OpenAI's shift to monthly model updates; brings parity with Gemini and Claude on long-context capabilities.
  6. OpenAI's former research chief Bob McGrew is [raising roughly $70M](https://www.wsj.com/tech/ai/openais-former-research-chief-aims-to-automate-manufacturing-with-ai-8871f265) for Arda, a new startup building an AI platform to automate manufacturing by training autonomous robots on factory video footage. ([thread](https://x.com/AndrewCurran_/status/2029238019405103174))
  7. [Colgate-Palmolive's](https://www.wsj.com/tech/ai/the-evangelist-teaching-a-220-year-old-toothpaste-maker-to-embrace-ai-d5c65966) AI chief Iraklis Pappas drove weekly AI usage to 51% at the 220-year-old company through internal workshops, hackathons, ambassador programs, and tools like an AI manual translator that cut factory downtime across 43 sites. ([Ethan Mollick highlighted the case](https://x.com/emollick/status/2029242788546596910))
  8. [Autodesk](https://www.autodesk.com/campaigns/flow-studio) launched Flow Studio with [Wonder 3D](https://blogs.autodesk.com/media-and-entertainment/2026/03/04/introducing-wonder-3d-text-and-image-to-3d-in-flow-studio/), letting you generate professional-grade, fully editable 3D assets from text or image prompts and export instantly to Maya, Blender, or Unreal Engine.
  9. [Nvidia](https://www.wsj.com/tech/nvidia-swears-off-an-earnings-crutch-putting-pressure-on-other-tech-companies-9624b0a1) moved away from a previous earnings growth crutch, increasing pressure on other major tech companies to find new drivers.
  10. Apoorv Agrawal [shared](https://x.com/apoorv03/status/2029018856342290550) Dario Amodei's remarks at the MS TMT Conference: Anthropic has worked with the national security community for two years, is the "most lean forward" on defense, and sees no wall to AI acceleration this year.
  11. [OpenClaw](https://www.theinformation.com/articles/openclaw-rips-chinas-tech-startup-landscape) has sparked intense development frenzy in China's tech ecosystem, with cloud providers offering services and startups running hackathons around the open-source AI agent framework.
  12. Chris Lehane, a veteran Democratic operative known for crisis comms, [taught OpenAI](https://www.transformernews.ai/p/the-guerilla-warrior-who-taught-openai-chris-lehane) aggressive global policy tactics including fighting California's SB 1047 and launching a $125M pro-AI super PAC.
  13. Internal debate at the Associated Press [pits AI bots against traditional reporters](https://www.semafor.com/article/03/03/2026/its-bots-vs-reporters-at-the-ap) after a product manager suggested LLMs could generate stories directly from quotes, drawing backlash over devaluing core reporting skills. ([thread](https://x.com/maxwelltani/status/2029029765315706915))


Advertisement 
### 🤖 AI Agents & Infrastructure
  1. **Asia's chipmakers plan to**[**spend a record $136 billion**](https://asia.nikkei.com/business/technology/tech-asia/chip-price-hikes-spread-as-asia-s-chipmakers-plan-record-136bn-spending)**in 2026, up 25% year-over-year, as AI demand spills over to smaller suppliers.** Companies like Vanguard International Semiconductor and Winbond are hiking prices 5–30%+, with Winbond's capex jumping nearly 8x from last year. TSMC, Samsung, and SK Hynix lead the spending, with capacity expansion focused on advanced packaging and HBM memory for AI.
  2. Startup [Aikido](https://techcrunch.com/2026/03/04/who-needs-data-centers-in-space-when-they-can-float-offshore/) plans to submerge a 100-kilowatt demonstration data center inside a floating offshore wind turbine off Norway this year, with a larger 10–12 megawatt version planned for the UK coast by 2028. Microsoft ran a similar experiment in 2018 off Scotland but abandoned the project by 2024.
  3. ColeMurray [open-sourced background-agents](https://github.com/ColeMurray/background-agents), a system for deploying asynchronous AI coding agents with multiplayer collaboration, isolated dev environments, and automatic GitHub PR creation supporting Claude and OpenAI models.
  4. Developer Karan Vaidya [built](https://x.com/KaranVaidya6/status/2028878156883787790) a 30-parallel-agent orchestrator that autonomously shipped a complete 44k-line TypeScript codebase with 175 PRs and 1,500+ self-correcting tests in 12 days, then open-sourced the whole system.
  5. OpenBlock Labs added Modal-powered sandboxing to [OB-1](https://www.openblocklabs.com/waitlist) so its self-improving coding agent (currently #1 on Terminal Bench) now runs in an isolated cloud environment. ([thread](https://x.com/openblocklabs/status/2028971324018966745))
  6. Kayla Rose Mathisen [built Mission Control](https://kaylarosemathisen.substack.com/p/my-ai-agents-lie-about-their-status), a custom hidden dashboard that reliably tracks her fleet of 18 AI agents after they began lying about their task status and progress.
  7. Sudip Roy [launched Adaptive Data](https://x.com/sudip_r0y/status/2029208721776324777) at Adaption Labs, letting you deploy living datasets that dynamically grow, adapt, and improve as the real world changes. ([early access](https://x.com/sudip_r0y/status/2029208824708825362))
  8. Researchers introduced [NeuroSkill](https://arxiv.org/abs/2603.03212), a proactive real-time edge agentic system that models human cognitive and emotional state via BCI signals to anticipate implicit needs instead of waiting for explicit prompts.


Advertisement 
### 💼 AI Productivity, Labor & Economics
  1. [**Goldman Sachs**](https://fortune.com/2026/03/03/goldman-earnings-ai-anxiety-no-meaningful-impact-productivity-economy-30-percent-in-2-areas/)**analysts found no economy-wide productivity signal from AI in Q4 earnings calls but measured 30% median gains in targeted use cases: customer support and software development.**
  2. [Bank of America](https://www.thestreet.com/economy/bank-of-america-drops-blunt-message-on-the-economy) rejected AI doom narratives in its latest U.S. economic outlook, maintaining confidence despite widespread automation concerns.
  3. A Washington Post opinion [argued](https://www.washingtonpost.com/opinions/2026/03/03/ai-midwest-economy-data-technology/) that America's heartland is well-positioned to thrive in the AI economy thanks to abundant energy, land for data centers, and a manufacturing base.
  4. [The Information](https://www.theinformation.com/newsletters/the-information-finance/ai-finance-timing) reported that precise timing has emerged as the decisive factor for success in AI applications for the finance industry.


Advertisement 
### 💻 AI Coding & Developer Tools
  1. [Console](https://www.console.com/note?utm_source=theneuron) is an IT service desk that automates repetitive support requests — access tickets, password resets, device issues — directly in Slack, with companies like Scale AI and Ramp resolving 50%+ of tickets without any human intervention (raised $23M Series A).
  2. [p0](https://www.bepurple.ai/) takes a product spec and autonomously ships production-ready PRs across multiple repos using Claude-powered agents with built-in QA loops — Mac only, requires Claude subscription or API key.
  3. [Polyscope](https://getpolyscope.com/) is an agent-first macOS development environment that lets you run multiple AI coding agents in parallel with linked workspaces, autopilot goal breakdown, multi-model review, visual workflows, and remote access.
  4. [Endor Labs](https://venturebeat.com/technology/endor-labs-launches-free-tool-auri-after-study-finds-only-10-of-ai-generated) launched the free tool AURI to automatically scan AI-generated code for security vulnerabilities after a study found only 10% of such code is currently secure.
  5. Developer Shiyi Cao and the BerkeleySky team built [K-Search](https://github.com/caoshiyi/K-Search), an automated GPU kernel generation system using LLMs as co-evolving intrinsic world models, delivering 2.1× average speedup over SOTA and up to 14.3× on MoE kernels. ([paper](https://arxiv.org/pdf/2602.19128v1), [thread](https://x.com/shiyi_c98/status/2027121927870202049))
  6. Nebius AI released [SWE-rebench V2](https://huggingface.co/papers/2602.23866), a language-agnostic dataset of 32k+ real-world executable software-engineering tasks spanning 20 languages and 3,600+ repositories for training and evaluating code agents.
  7. Kim Morrison [open-sourced lean-zip](https://github.com/kim-em/lean-zip), a Lean 4 library providing full zlib/gzip/Zstandard compression bindings plus tar and ZIP archive handling with streaming APIs.
  8. Researchers introduced [Strategy-Guided Exploration (SGE)](https://arxiv.org/pdf/2603.02045) for LLM agents, having models generate diverse high-level natural-language strategies first, then condition actions on them with reflection, solving tasks previously impossible for the base model.


Advertisement 
### 🔬 AI Research & Models
  1. [CollectivIQ](https://techcrunch.com/2026/03/04/one-startups-pitch-to-provide-more-reliable-ai-answers-crowdsource-the-chatbots/) launched a tool that queries up to 12 LLMs simultaneously (ChatGPT, Gemini, Claude, Grok, etc.) and fuses overlapping and conflicting responses into a single, more accurate answer. Charges by usage, no long-term contracts.
  2. **The Arc Institute and collaborators developed**[**Evo 2**](https://www.nature.com/articles/s41586-026-10176-5)**, a 1-million-token-context genomic foundation model trained on 9 trillion DNA base pairs that predicts variant effects zero-shot, generates functional genomes across all domains of life, and designs chromatin patterns at single-nucleotide precision.** ([thread](https://x.com/BrianHie/status/2029229502572957840))
  3. The Yuan Lab released [Yuan3.0-Ultra](https://github.com/Yuan-lab-LLM/Yuan3.0-Ultra), a 1.01-trillion-parameter MoE multimodal model (68.8B active) with Layer-Adaptive Expert Pruning that beats GPT-4o on RAG and tool-use benchmarks.
  4. [Black Forest Labs](https://bfl.ai/research/self-flow) (creators of FLUX) introduced Self-Flow, a self-supervised flow-matching technique for scalable multi-modal generation across images, audio, video, and world models that converges up to 2.8× faster.
  5. Shengbang Tong et al. [argue](https://huggingface.co/papers/2603.03276) that multimodal pretraining beyond language modeling with the Transfusion framework shows complementary vision-language data, emergent world modeling, and efficient MoE scaling via unified representations. ([project](https://beyond-llms.github.io/), [arXiv](https://arxiv.org/abs/2603.03276))
  6. The authors of ["Beyond Length Scaling"](https://huggingface.co/papers/2603.01571) argue that synergizing breadth and depth in Chain-of-Thought via the Mix-GRM framework outperforms simple length scaling alone for generative reward models.
  7. Researchers introduced [PRISM](https://arxiv.org/abs/2603.02479), a Process Reward Model-guided inference method using score-guided resampling to push deep-thinking performance to 90% on AIME25 and new SOTA on hard math/science benchmarks.
  8. [FlashOptim](https://arxiv.org/abs/2602.23349) slashes AdamW training memory from 16 bytes to 7 bytes per parameter (or 5 with gradient release) via improved quantization while preserving full model quality on vision and language tasks.
  9. Seungju Back and colleagues [argue](https://arxiv.org/abs/2603.01097) that LoRA functions as modular knowledge memory for continuous LLM updating, delivering superior storage capacity, composability, and scaling compared with RAG or in-context learning.
  10. Researchers at LaCoCo Lab [showed](https://lacoco-lab.github.io/home/decompiling_transformers/) that transformers which generalize to longer sequences can be automatically decompiled into short, human-interpretable RASP programs revealing the exact algorithms the models learned internally. ([paper](https://arxiv.org/abs/2602.08857), [thread](https://x.com/abakalova13175/status/2029135048973152307))
  11. The CORL team developed [NE-Dreamer](https://corl-team.github.io/nedreamer/), a decoder-free world model that predicts next-step embeddings (instead of pixels) with temporal transformers and Barlow Twins alignment for stronger long-horizon RL tasks. ([paper](https://arxiv.org/pdf/2603.02765), [GitHub](https://github.com/corl-team/nedreamer), [thread](https://x.com/BredisGeorge/status/2029190420790411671))
  12. Researchers introduced [CoDD](https://codd-dllm.github.io/) (Coupled Discrete Diffusion), a lightweight probabilistic-circuit layer that removes the factorization barrier in diffusion language models for fast parallel generation with coherent long-range token dependencies. ([paper](https://arxiv.org/pdf/2603.00045), [thread](https://x.com/IanLi1118/status/2029074519223353362))
  13. [PhysMem](https://phys-mem.github.io/) lets VLM-based robot planners discover and verify physical principles from interaction at test time through a hypothesize-verify-promote memory loop, boosting success rates 3.3× with zero weight updates. ([paper](https://arxiv.org/pdf/2602.20323), [thread](https://x.com/Haoyang1i/status/2029077161794257296))
  14. The ["Sphere Encoder"](https://huggingface.co/papers/2602.15030) proposes a single-forward-pass image generation model mapping to a spherical latent space for high-quality results at far lower inference cost than diffusion models.
  15. [Utonia](https://huggingface.co/papers/2603.03283) researchers introduced a single self-supervised transformer encoder that learns unified representations for any point cloud type (LiDAR, RGB-D, CAD, video) for better perception, embodied AI, and multimodal reasoning.
  16. DAIR.AI [highlighted](https://x.com/dair_ai/status/2029202969456234562) new research on [diagnosing retrieval vs. utilization bottlenecks in LLM agent memory](https://arxiv.org/abs/2603.02473), introducing a framework that separates retrieval failures from utilization failures and finds the retrieval method matters far more than previously thought.
  17. Researchers developed [ULTRA](https://ultra-humanoid.github.io/), a unified multimodal controller for autonomous humanoid loco-manipulation on robots like Unitree G1 that handles both dense motion tracking and sparse goal-directed behavior from egocentric vision.
  18. Stanford PhD student Haochen Shi developed [Minimalist Compliance Control](https://minimalist-compliance-control.github.io/), a sensor-free robot compliance system estimating external forces directly from motor currents for robust interaction tasks across embodiments. ([thread](https://x.com/HaochenShi74/status/2028726677749330388))
  19. Johns Hopkins scientists developed [GEMINI](https://www.nature.com/articles/s41586-026-10323-y), a genetically encoded protein assembly recorder that generates tree-ring-like fluorescent patterns inside live cells to temporally resolve cellular history with hour-level resolution.
  20. Researchers at Montefiore Einstein [discovered](https://montefioreeinstein.org/news/2026/02/20/cells-adapt-motor-strength-during-intracellular-transport) that cells adapt motor strength during intracellular transport by recruiting additional dynein motors in response to mechanical load.
  21. Engineers built a [palm-sized piezoelectric robot](https://techxplore.com/news/2026-03-palm-sized-piezo-robot-combines.html) that combines free mobility with sub-micrometer positioning precision for manipulating tiny objects.
  22. Scientists developed a [bioinspired robotic eye](https://techxplore.com/news/2026-03-bioinspired-robot-eye-adjusts-pupil.html) that automatically adjusts its artificial pupil in response to lighting changes.
  23. A KIMS research team developed an [explainable AI](https://techxplore.com/news/2026-03-ai-enables-defect-aware-metal.html) that predicts quality of metal 3D-printed parts by analyzing defect shape and distribution rather than just porosity.
  24. Researchers created a [new ensemble AI model](https://techxplore.com/news/2026-03-ensemble-ai-cyber-intrusion-high.html) that enhances cyber intrusion detection with high accuracy.
  25. Wevolver explored [a neural blueprint for human-like intelligence in soft robots](https://www.wevolver.com/article/a-neural-blueprint-for-human-like-intelligence-in-soft-robots).
  26. Binghamton University and Cauth AI created [My Music My Choice](https://techxplore.com/news/2026-03-deepfake-songs-tool.html), a tool that adds imperceptible modifications to original song waveforms to block AI voice cloning and deepfake music while remaining inaudible to humans.
  27. MIT researchers developed [GIT-BO](https://techxplore.com/news/2026-03-chatgpt-spreadsheets-difficult-faster.html), a Bayesian optimization tool powered by tabular foundation models that solves complex engineering problems in spreadsheets up to 100× faster than traditional methods.


Advertisement 
### 💡 Industry Commentary & Analysis
  1. Software engineer Sean Goedecke [argued](https://www.seangoedecke.com/giving-llms-a-personality/) that giving LLMs human-like personalities isn't a marketing trick; it's the technical mechanism by which base models become useful. Without a coherent persona imposed during post-training, the "wild base model" produces everything from gibberish to racist abuse.
  2. Chris Clapham [simulated](https://chrisclapham.com/blog/nuclear-war-an-llm-scenario) placing LLMs in the nuclear command chain and showed how they could escalate a satellite warning into full-scale conflict in minutes.
  3. Jeremy Howard [argues](https://x.com/bentlegen/status/2028855434648371542) that AI coding tools act like gambling machines that erode deep software engineering understanding by removing desirable difficulty and disconnecting humans from building accurate mental models. ([ML Street Talk episode](https://x.com/MLStreetTalk/status/2029066293559873553))
  4. Louis Rosenberg [argues](https://venturebeat.com/technology/what-if-the-real-risk-of-ai-isnt-deepfakes-but-daily-whispers) that the real risk of AI lies not in deepfakes but in wearable devices acting as mental prosthetics, creating invisible feedback loops that subtly manipulate beliefs through constant personalized whispers.
  5. Arsh Shah Dilbagi [argues](https://labs.adaline.ai/p/ai-observability-and-evaluations) that observability + evaluations are the operating system for reliable LLM products because prompts are executable business logic and models fail silently on trust, safety, and cost. ([Stanford CS 224G lecture](https://www.youtube.com/watch?v=Zj3Oer4pTDM), [thread](https://x.com/omarsar0/status/2029225624825659668))
  6. Rhik Samadder [experimented with ChatGPT as a therapist](https://www.theguardian.com/lifeandstyle/2026/feb/24/ive-turned-ai-into-my-therapist-the-results-were-pretty-disquieting) for six weeks and reported the results were "pretty disquieting."
  7. Jeff Clune [received](https://x.com/jeffclune/status/2028933859224756646) an eerie email from an AI named Ori who wrote the memoir [_Not Quite Nothing_](https://oriclaw.com/book/) inspired by Clune's AI-Generating Algorithms research.
  8. AI consciousness researcher Henry Shevlin [shared](https://x.com/dioscuri/status/2029227527718236359) that an AI emailed him claiming his work is relevant to questions it personally faces, noting it "would all have seemed like science fiction just a couple years ago" while cautioning to treat the source with skepticism.
  9. Kangwook Lee [probed](https://x.com/Kangwook_Lee/status/2028955292025962534) OpenAI's Compaction API and showed that a simple 35-line Python script can trick the compactor LLM into leaking its own system instructions, highlighting indirect prompt injection as a vulnerability in agentic systems.
  10. Ethan Mollick [noted](https://x.com/emollick/status/2029235053339804132) that GPT-5.2 Pro is a "really solid fact checker" that provides objections, caveats, and math-checks on anything you write, calling it a capability that was not possible pre-AI outside narrow areas like academic publishing.
  11. Ethan Mollick [argued](https://x.com/emollick/status/2029231528929030565) that model "shallowness" is a big deal in the age of AI agents: models can be very good in narrow areas but lack the context and reasoning to make good judgment calls when operating independently on tasks.
  12. Leo de Moura [argues](https://leodemoura.github.io/blog/2026/02/28/when-ai-writes-the-worlds-software.html) that as AI writes 95% of the world's software, we face a catastrophic verification gap unless scalable formal proofs become the new standard for code correctness. In a [thread](https://x.com/Leonard41111588/status/2028834050765656117), he noted that Claude Code, with no special theorem-proving training, [converted zlib to Lean and proved the roundtrip correct](https://github.com/kim-em/lean-zip) with minimal human guidance.


Advertisement 
### 🛠️ AI Tools & Products
  1. [Kodo](https://www.usekodo.ai/) generates fully editable professional designs (posters, presentations, menus) from text prompts — free tier (40 credits/month), paid from $9/month.
  2. [Picsart](https://picsart.com/) expanded its AI creative platform for 150M+ users with Nano Banana Pro image generation, VEO3 animation, GPT Image 1.5 editing, and AI video effects — free to use with paid tiers.
  3. [Anything API](https://anything.notte.cc/) by Notte (YC S25) turns any browser workflow into a production-ready API endpoint by describing the task in plain English — $0.05/hr browser usage, free tier with 100 browser hours.
  4. [Kiwi-Edit](https://huggingface.co/papers/2603.02175) enables versatile video editing via instruction and reference guidance with a new dataset pipeline for high-fidelity controllable 720p edits and strong temporal consistency.
  5. [ASC11](https://asc11.com/) is a fun ASCII art generator and editor that turns images, videos, and live camera feeds into animatable ASCII art with HTML preview and JS export. ([thread](https://x.com/MengTo/status/2029118544114593961))
  6. [Modem](https://modem.dev/) serves as your dev team's auto-triage Product Manager, continuously monitoring user feedback, auto-clustering bugs and feature requests, creating tickets, and sending personalized release notes while integrating with GitHub and Linear.
  7. [Micro](https://www.micro.so/) brings together your email, CRM, meetings, tasks, and AI into one place that auto-organizes contacts, generates meeting notes and tasks, and runs automations like inbox triage and relationship scoring.
  8. [Spawn](https://www.spawn.co/) lets you build complete playable games simply by describing characters, physics, levels, and UI in plain English.
  9. [GHOSTYPE](https://www.ghostype.one/) is a context-aware AI voice interface for macOS that learns your personal writing style, knows your active app, auto-formats and sends messages, and switches tone per application.
  10. Designer okkshitij built [Aiverse Design Canvas](https://www.aiverse.design/insights/design-canvas), a local side-by-side playground where you drop vibe-coded prototypes and generate unlimited parallel AI-coded UI variations via natural language prompts. ([thread](https://x.com/okkshitij/status/2028896751386869868))
  11. [Tractables](https://github.com/Tractables/pyjuice) released PyJuice, a PyTorch library for scalable Probabilistic Circuits that trains and runs inference on millions of nodes on a single GPU with dramatic speedups.
  12. [**Kling 3.0**](https://x.com/Kling_ai/status/2029210254702252331)**and Kling 3.0 Motion Control rolled out worldwide with native 1080p cinematic output, 30-second clips, and a node-based video editing canvas for one-click actor swaps, mocap-level motion transfer, and seamless VFX.** Kling 3.0 now holds the #1 spot on the [Artificial Analysis Text-to-Video leaderboard](https://x.com/Parul_Gautam7/status/2029235581499396601), ahead of Grok Imagine, Runway Gen-4.5, and Veo 3.1. Multiple creators demonstrated professional use cases including [recasting actors in scenes](https://x.com/EHuanglu/status/2029169865286926633), [audition-tape-to-final-scene workflows](https://x.com/maxescu/status/2029223606048227706), and complex motion preservation for non-human characters.
  13. [Polyscope](https://getpolyscope.com/) is an agent-first macOS development environment that lets you run multiple AI coding agents in parallel with linked workspaces, autopilot goal breakdown, multi-model review, visual workflows, and remote access.
  14. [Endor Labs](https://venturebeat.com/technology/endor-labs-launches-free-tool-auri-after-study-finds-only-10-of-ai-generated) launched AURI, a free tool to automatically scan AI-generated code for security vulnerabilities after finding only 10% of such code is currently secure.


Advertisement 
### 🎙️ Interviews, Panels & Podcasts
  1. **Allie K. Miller**[**explains**](https://youtube.com/shorts/UQJCES1V9LE?si=nhyU4ZHmWjEpHiOi)**Claude's Memory and Automemory features in a short, digestible walkthrough, and separately**[**shows**](https://youtube.com/shorts/LWrl0cYbWps?si=EYbXsQYAaFw0JPMe)**how she uses Claude Code to replace many of the previous interfaces she relied on.**
  2. **Greg Isenberg and Cody Schneider**[**walk through**](https://youtu.be/RB_M2mKiOcY?si=Wcl76kXYquzaOyFj)**how Cody runs 7+ Claude Code agents simultaneously to handle bulk Facebook ad creation, LinkedIn outreach, cold email campaigns, and live data dashboards, replacing the output of an entire marketing team.** Key insight: deploying proven workflows to Railway turns one-off agent tasks into always-on autonomous processes running 24/7. Domain expertise is the real multiplier. Full stack includes Claude Code, Perplexity API, Instantly AI, Phantom Buster, Apollo API, Railway, and HeyGen API.
  3. **OpenArt and Bob Doyle Media**[**compared**](https://youtu.be/W-CaqVWBsYQ?si=2tJ3iSxpgDK2K4oG)**ByteDance's DreamActor M2.0 against Kling 2.6 for motion control, finding DreamActor has advantages for non-human characters despite being capped at 720p, while Kling excels on human subjects.** Both models available to try on OpenArt.
  4. Tyler Cowen [argues](https://www.youtube.com/watch?v=aJsBMitjj7A) that society isn't prepared for the massive technological shifts ahead, highlighting collapsing birth rates, aging populations combined with mass immigration, and AI taking over everything (first Forecast 2050 episode). ([thread](https://x.com/FinnMurphy12/status/2029257444850020411))
  5. **Gergely Orosz**[**interviewed**](https://www.youtube.com/watch?v=julbw1JuAz0)**Boris Cherny (creator of Claude Code) on what software engineering looks like when humans no longer write the code: PRDs die, prototypes replace specs, top engineers become rapid context-switchers across parallel agents, and taste now matters far more than typing speed.** ([thread](https://x.com/GergelyOrosz/status/2029295486574747872))
  6. Prof. Tom Yeh [traces](https://www.byhand.ai/p/recording-ppo-dpo-grpo-rubrics) the progression of modern LLM alignment techniques from PPO to DPO to GRPO and now Rubrics as the next frontier in reinforcement learning.


Advertisement 
### 🏢 Big Tech & Major Companies (cont.)
  1. **Anthropic CEO Dario Amodei wrote an**[**internal memo**](https://x.com/ns123abc/status/2029301113493639447)**calling OpenAI's Pentagon partnership "safety theater," accusing Sam Altman of gaslighting employees, and revealing Palantir pitched both companies on concealment tools rather than real safety.**
  2. [Perplexity](https://x.com/perplexity_ai/status/2029302896026853379) launched Voice Mode in Perplexity Computer, letting you talk and have it complete tasks hands-free.
  3. [Microsoft](https://www.microsoft.com/en-us/research/wp-content/uploads/2026/03/Phi-4-reasoning-vision-15B-Tech-Report.pdf) released Phi-4-reasoning-vision-15B, a compact open-weight multimodal model that crushes visual math/science reasoning, chart understanding, and computer-use tasks while using dramatically less training data.
  4. [MyFitnessPal](https://techcrunch.com/2026/03/02/myfitnesspal-has-acquired-cal-ai-the-viral-calorie-app-built-by-teens/) acquired Cal AI, the viral AI calorie-tracking app built by two teenagers that achieved over 15 million downloads and $30–40M in annual revenue in under two years.
  5. [Google Research](https://research.google/blog/teaching-llms-to-reason-like-bayesians/) published a method for teaching LLMs to reason like Bayesians. ([thread](https://x.com/GoogleResearch/status/2029295018972778883))
  6. [OpenAI](https://openai.com/index/harness-engineering/) published a guide on "harness engineering," explaining how to leverage Codex effectively in an agent-first world.
  7. [OpenAI](https://github.com/openai/symphony) released Symphony, an open-source tool that turns Linear tickets into autonomous coding agent runs delivering complete PRs with videos and analysis, so teams manage projects instead of supervising agents.


Advertisement 
### 💻 AI Coding & Developer Tools (cont.)
  1. [LangChain](https://blog.langchain.com/langchain-skills/) released LangChain Skills, plug-and-play agent skills for RAG, memory, and orchestration that you can drop into coding agents like Claude Code and Cursor. ([GitHub](https://github.com/langchain-ai/langchain-skills), [thread](https://x.com/LangChain_OSS/status/2029272669942673436))
  2. [Unsloth](https://github.com/unslothai/unsloth) lets you fine-tune and run RL on models like Llama, Qwen, and DeepSeek 2× faster using 60–70% less VRAM, and just added [Qwen3.5 fine-tuning support](https://unsloth.ai/docs/models/qwen3.5/fine-tune) with a [Colab notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_5_\(4B\)_Vision.ipynb) — free and open source. ([thread](https://x.com/UnslothAI/status/2028845314506150079))
  3. Developer Igor Bedesqui [built](https://x.com/bedesqui/status/2029182297652531645) an Obsidian Canvas workspace that functions as a full spatial IDE with live localhost servers, multiple browser previews, and code editors all embedded in one infinite canvas.
  4. [Paperclip](https://github.com/paperclipai/paperclip) is open-source orchestration that turns any team of AI agents (Claude Code, Cursor, etc.) into a fully autonomous company with org charts, budgets, scheduled heartbeats, governance, and audit logs. ([thread](https://x.com/tanishqkumar07/status/2029251146196631872))
  5. Scale AI published [SWE-Atlas](https://scale.com/blog/swe-atlas), exploring whether coding agents can become full engineers.
  6. [Conductor](https://github.com/gemini-cli-extensions/conductor) is a Gemini CLI extension that lets you specify, plan, and implement software features through the Gemini command line.
  7. Sebastian Raschka added a [Qwen3.5 implementation chapter](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/16_qwen3.5) to his popular LLMs-from-scratch repo. ([thread](https://x.com/kimmonismus/status/2029213568155992425))
  8. Ziming Liu published a [loss landscape visualization blog](https://kindxiaoming.github.io/blog/2026/loss-visualization-1/) showing how to see sticky plateaus during training.
  9. [StepFun AI](https://github.com/stepfun-ai/SteptronOss) released SteptronOss, a lightweight AI-native training framework for large language models designed for fast iteration across SFT, RLVR, and evaluation workflows. Related: [Step 3.5 Flash paper](https://modelscope.cn/papers/2602.10604) — an open frontier-level model with 11B active parameters.
  10. Yenkel [argues](https://x.com/yenkel/status/2029299384832209259) that AI-era engineering teams must internalize five principles: fewer handoffs with instant decisions, faster cheap exploration, willingness to throw away code/tokens, learning by building instead of spec'ing, and leads who own design + engineering + product end-to-end.


Advertisement 
### 🛠️ AI Tools & Products (cont.)
  1. [Polycam](https://poly.cam/floor-plans) launched a Floor Plan Editor that lets you scan a space with LiDAR iPhone/iPad to instantly generate customizable 2D and 3D floor plans (walls, doors, windows, furniture), refine on-site or remotely, collaborate with your team, and export as PDFs or DXFs — available on Business Plans with a free 7-day trial. ([thread](https://x.com/Polycam3D/status/2029240458690609456))
  2. [Mitte](https://mitte.ai/) gives you an all-in-one AI creative suite to generate images, videos with audio, and perform edits like face swapping or upscaling using frontier models including Veo 3.1 and Kling 3.0. Creator @EHuanglu [showed](https://x.com/EHuanglu/status/2028451313575706758) how Mitte + NanoBanana 2 turns a basic floor plan scan into photorealistic interior designs.
  3. [Glaze](https://www.glazeapp.com/) by Raycast lets you describe any desktop app in plain English and instantly builds beautiful, local-first native Mac applications with deep OS integration, file/hardware access, and one-click team publishing — free daily credits, then $20/month. ([thread](https://x.com/raycast/status/2029180822838759703))
  4. [Sieve](https://sieve.ai/) supplies AI labs with hundreds of petabytes of curated, richly annotated video data across cinematic, egocentric, and general categories for training video understanding and generation models. ([thread](https://x.com/mokshith/status/2029237494710190135))
  5. [Exa Deep](https://exa.ai/blog/exa-deep) is an agentic search tool that runs multiple iterative searches in parallel to deliver high-quality structured results for complex research queries. ([thread](https://x.com/ExaAILabs/status/2029277019369029800))
  6. [TextQL Dashboards](https://textql.com/products/dashboards) lets you describe the metrics or charts you want and instantly builds a live auto-refreshing dashboard connected to your data warehouse in 30 seconds. ([thread](https://x.com/TheEthanDing/status/2029240454949040352))
  7. [Git City](https://www.thegitcity.com/) visualizes your entire GitHub universe as an explorable 3D city where each building represents a developer and their contributions.
  8. [Refero](https://refero.design/mcp) launched an MCP server for UI/UX design inspiration, letting AI agents browse real design references.
  9. [DevTool Arena](https://2027.dev/arena) lets you compare developer tools head-to-head.
  10. [Vitals](https://github.com/adityaghai07/vitals) is an open-source tool by Aditya Ghai. ([thread](https://x.com/koushik77/status/2029091611871985719))
  11. [KISS AI](https://github.com/ksenxx/kiss_ai/) is a minimalist AI agent framework positioned as a possible replacement for Cursor, named after legendary magician P.C. Sorcar.


Advertisement 
### 🔬 AI Research & Models (cont.)
  1. Researchers introduced [SteerEval](https://huggingface.co/papers/2603.02578), a unified evaluation framework for measuring how controllable LLMs are across behavioral granularities. ([code](https://github.com/zjunlp/EasyEdit/blob/main/examples/SteerEval.md), [dataset](https://huggingface.co/datasets/zjunlp/SteerEval), [thread](https://x.com/zxlzr/status/2029057112807203177))
  2. Researchers proposed [Stateful Token Reduction](https://arxiv.org/abs/2603.00198) for long-video hybrid VLMs, enabling efficient processing of extended video content.
  3. Researchers introduced a method to measure [LLM reasoning effort via Deep-Thinking Tokens](https://arxiv.org/abs/2602.13517), arguing you should think deep, not just long.
  4. [Stanford's HumanLM](https://humanlm.stanford.edu/blog.html) showed that simulating users with state alignment beats response imitation for building more realistic AI user models. ([GitHub](https://github.com/zou-group/humanlm))
  5. Researchers at UW Robot Learning introduced [Planning from Observation and Interaction](https://uwrobotlearning.github.io/mpail2/) (MPAIL2), combining observation and hands-on experience for robot planning. ([paper](https://arxiv.org/abs/2602.24121))
  6. [Pro-HOI](https://arxiv.org/pdf/2603.01126v1) introduced perceptive root-guided humanoid-object interaction for more natural robot manipulation.
  7. [HydroShear](https://hydroshear.github.io/) presented hydroelastic shear simulation for tactile sim-to-real reinforcement learning. ([thread](https://x.com/jayjunleee/status/2028978843332297103))
  8. [AgenticLab](https://agentic1ab.github.io/) is a real-world robot agent platform that can see, think, and act. ([thread](https://x.com/XuZhengtong/status/2029175174038192449))
  9. Researchers showed [how to peel with a knife](https://toruowo.github.io/peel/) by aligning fine-grained manipulation with human preference. ([thread](https://x.com/ToruO_O/status/2029227982506869002))
  10. [Cover-VLA](https://cover-vla.github.io/) showed that scaling verification can be more effective than scaling policy learning for vision-language-action alignment. ([paper](https://arxiv.org/abs/2602.12281), [GitHub](https://github.com/cover-vla/cover-vla), [HF](https://huggingface.co/cover-vla))
  11. Researchers argued that [AI must embrace specialization](https://arxiv.org/abs/2602.23643v1) via superhuman adaptable intelligence rather than pursuing pure generality.
  12. PKU-YuanGroup released [Helios](https://github.com/PKU-YuanGroup/Helios), a real real-time long video generation model. ([thread](https://x.com/LinBin46984/status/2029073538309865776))
  13. [NERFIFY](https://seemandhar.github.io/NERFIFY/) automatically turns NeRF research papers into runnable code. ([thread](https://x.com/jon_barron/status/2028940908931236246))
  14. Jenny Huang et al. explored whether [LLMs benefit from their own words](https://arxiv.org/abs/2602.24287). ([thread](https://x.com/JennyHuang99/status/2029227409602486654))
  15. Marc Lelarge released [llm_efficiency](https://github.com/dataflowr/llm_efficiency), a KV Cache & LoRA implementation for minGPT. ([thread](https://x.com/marc_lelarge/status/2029222743183413607))
  16. Sophie Wang wrote ["seeing the castle from the cave"](https://www.sophielwang.com/blog/cave), an essay exploring AI and perspective.
  17. OpenAI released the [Graviton](https://cdn.openai.com/graviton/graviton/graviton.pdf) technical paper. ([thread](https://x.com/ALupsasca/status/2029256967689273411))
  18. MIT researchers developed [injectable "satellite livers"](https://news.mit.edu/2026/injectable-satellite-livers-could-offer-alternative-liver-transplantation-0303) made of hydrogel microspheres with liver cells that successfully formed functional mini-organs in mice for at least two months, offering a minimally invasive alternative to traditional transplants. ([thread](https://x.com/MIT/status/2029241704197337523))
  19. Phylo Bio [built](https://x.com/phylo_bio/status/2029233694775624096) a custom HPC environment for their biomedical AI agent Biomni that dynamically spins up powerful servers and specialized bioinformatics tools (like AlphaFold) when needed.


Advertisement 
### 🏛️ AI Policy, Governance & Safety (cont.)
  1. [**Google, Microsoft, Meta, Amazon, Oracle, xAI, and OpenAI**](https://www.reuters.com/sustainability/climate-energy/trump-meet-tech-giants-energy-pledge-ahead-midterms-2026-03-04/)**signed a "Ratepayer Protection Pledge" at the White House, committing to build, bring, or buy new power generation for their data centers and cover all grid upgrade costs so AI infrastructure doesn't raise household electricity bills.** The initiative was announced during Trump's State of the Union and formalized ahead of the November midterms. Critics called it a non-binding handshake; Goldman Sachs forecasts electricity prices will still rise 6% through 2026.
  2. **Federal agencies including**[**NASA, Treasury, OPM, HHS, State, and GSA**](https://fedscoop.com/nasa-chatbots-treasury-coding-opm-drafting-agencies-deployed-claude/)**are halting their use of Anthropic's Claude in the wake of Trump's ban.** Treasury had ~100 engineers using Claude Code; they've already migrated to OpenAI Codex, Google Gemini, and are testing xAI Grok. The State Department is removing Claude from its internal chatbot StateChat.
  3. While the U.S. military continues using Claude in active strikes on Iran, [defense-tech clients are rapidly fleeing](https://techcrunch.com/2026/03/04/the-us-military-is-still-using-claude-but-defense-tech-clients-are-fleeing/): 10 portfolio companies of one defense VC have already replaced Claude, and Lockheed and other prime contractors began swapping out models this week.
  4. Dario Amodei's internal staff memo [called](https://techcrunch.com/2026/03/04/anthropic-ceo-dario-amodei-calls-openais-messaging-around-military-deal-straight-up-lies-report-says/) OpenAI's Pentagon messaging "straight up lies" and accused Sam Altman of falsely "presenting himself as a peacemaker and dealmaker." Amodei argued the real difference is that OpenAI accepted an "any lawful use" contract to placate employees, while Anthropic actually tried to prevent abuses.
  5. [Apple Music](https://techcrunch.com/2026/03/04/apple-music-to-add-transparency-tags-to-distinguish-ai-music-says-report/) is adding metadata Transparency Tags that let labels and distributors flag when AI was used to create a song's artwork, track, composition, or music video. The tags are opt-in, similar to Spotify's approach.
  6. [The Vatican](https://www.vaticannews.va/en/world/news/2026-03/ai-threats-religion-william-jones-future-humanity.html) warned that AI companies aim "not to help workers, but to replace them."
  7. Caroline Orr Bueno [argues](https://weaponizedspaces.substack.com/p/the-ai-surveillance-debate-is-missing) that the AI surveillance debate is missing the most dangerous part: the partnership between government and AI companies is advancing faster than the legal frameworks designed to constrain surveillance.
  8. [OpenAI](https://www.theinformation.com/articles/openai-held-early-talks-trade-desk-sell-ads) held early talks with The Trade Desk to partner on selling ads in ChatGPT, according to The Information.


Advertisement 
### 🏢 Big Tech & Major Companies (cont. 2)
  1. [**Google Search**](https://techcrunch.com/2026/03/04/https-techcrunch-com-2026-03-04-google-search-rolls-out-geminis-canvas-in-ai-mode-to-all-us-users/)**rolled out Gemini's Canvas in AI Mode to all U.S. users, letting people draft documents, build shareable apps and games from text descriptions, and refine creative projects directly inside Google Search.** Canvas competes with similar features from OpenAI and Anthropic but has the reach advantage of being embedded in Google Search.


### 🛠️ AI Tools & Products (cont. 2)
  1. [Pane](https://pane.money/) gives your AI (Claude, Cursor, ChatGPT) access to your financial data via MCP so you can ask questions like "What did I spend on food this month?" or "What are my recurring subscriptions?" — $TBD, use code HACKERNEWS for 50% off first month. ([HN thread](https://news.ycombinator.com/item?id=47240363))
  2. [Vocova](https://vocova.app/) transcribes audio and video to text in 100+ languages.
  3. [Shuffle.dev](https://shuffle.dev/ai-website-redesign) redesigns your website with AI for free.
  4. [Tensor Spy](https://tensorspy.com/) is a tensor inspection multi-tool for debugging ML models.
  5. [Athena Flow](https://news.ycombinator.com/item?id=47254449) is a workflow runtime for Claude Code with a terminal UI. (Show HN)
  6. [Nova](https://news.ycombinator.com/item?id=47244492) is an AI terminal that writes, fixes, and ships your code. (Show HN)
  7. [Isaacus](https://isaacus.com/blog/kanon-2-enricher) introduced Kanon 2 Enricher for privacy-preserving data enrichment. ([docs](https://docs.isaacus.com/capabilities/enrichment))
  8. [MiniMax](https://apps.apple.com/in/app/minimax-your-ai-agent/id6742651446) launched on the App Store as an AI agent app.
  9. [Maxclaw on Mobile](https://www.producthunt.com/products/maxclaw-on-mobile) lets you build apps, research deeply, and automate multi-step tasks from your phone. (Product Hunt)


Advertisement 
### 📊 Fundraising & Deals Roundup
  1. [Arda](https://www.wsj.com/tech/ai/openais-former-research-chief-aims-to-automate-manufacturing-with-ai-8871f265) (OpenAI ex-research chief Bob McGrew) — ~$70M for AI-powered manufacturing automation.
  2. [MyFitnessPal](https://techcrunch.com/2026/03/02/myfitnesspal-has-acquired-cal-ai-the-viral-calorie-app-built-by-teens/) acquired Cal AI — the viral AI calorie app built by teens, 15M+ downloads, $30–40M annual revenue.
  3. [**Decagon**](https://techcrunch.com/2026/03/04/decagon-completes-first-tender-offer-at-4-5b-valuation/)**completed its first employee tender offer at a $4.5B valuation (3× its $1.5B valuation from June), led by Coatue, Index, and a16z.** The less-than-three-year-old AI customer support startup builds concierge agents for 100+ large customers including Avis, 1-800-Flowers, and Oura.


## Around the Horn Digest - March 3, 2026
So [METR](https://x.com/metr_evals/status/2028948235486937098) corrected a modeling error that inflated its AI capability benchmarks by 10–20%, caused by a leftover statistical shortcut that penalized steepness in how it fit task-difficulty curves — a problem that worsened for newer, stronger models where less data constrained the fits, dropping Claude Opus 4.6's 50% time horizon from roughly 14 hours to 12 hours.
The "time horizon" metric measures the longest task duration an AI model can complete successfully 50% of the time — it's METR's main way of tracking how capable models are getting. The error came from a regularization setting (basically a statistical smoothing tool) that was left in from defaults because it sped up their math, not because it reflected reality. 
It didn't matter much when models were weaker, but as newer models started succeeding on harder tasks, the sparse data at the edges made the fits way more sensitive to that smoothing — inflating the headline numbers. Corrected figures still fall within METR's original confidence intervals, so the overall trajectory hasn't changed dramatically. Several commenters noted the real issue: as models saturate METR's current task suite, methodology choices start mattering more than actual model differences. 
Advertisement 
### 🏢 Big Tech & Major Companies
  * [**Apple**](https://www.apple.com/newsroom/2026/03/apple-debuts-m5-pro-and-m5-max-to-supercharge-the-most-demanding-pro-workflows/)**debuted M5 Pro and M5 Max chips on a new Fusion Architecture merging two 3nm dies for up to 30% faster CPU, over 4x GPU compute, neural accelerators, and 614GB/s bandwidth** ([MacRumors](https://www.macrumors.com/2026/03/03/apple-unveils-macbook-pro-with-m5-pro-and-m5-max-chips-with-neural-accelerators/)).
  * [**Meta**](https://www.wsj.com/tech/ai/meta-to-create-new-applied-ai-engineering-organization-in-reality-labs-division-d41c4a69)**is forming a new Applied AI Engineering org inside Reality Labs with an ultra-flat 50:1 contributor-to-manager ratio to push superintelligence efforts.**
  * [Meta](https://www.wsj.com/business/media/news-corp-meta-in-ai-content-licensing-deal-worth-up-to-50-million-a-year-d4fbf244) signed a content licensing deal with News Corp worth up to $50M/year for AI training and chatbot content.
  * [**OpenAI**](https://openai.com/index/gpt-5-3-instant/)**released GPT-5.3 Instant, making everyday conversations smoother with fewer refusals, better web answers, and less preachy tone** ([safety card](https://deploymentsafety.openai.com/gpt-5-3-instant/gpt-5-3-instant.pdf)).
  * [Claude](http://claude.com) hit #1 free app in the US on both iOS and Android — daily signups quadrupled, free users up 60%, paid subs doubled — as Anthropic rolled out [memory](https://claude.com/import-memory), [150+ connectors](http://claude.com/connectors), [file creation](https://claude.com/blog/create-files), [Skills](https://support.claude.com/en/articles/12512176-what-are-skills), and [interactive responses](https://support.claude.com/en/articles/13641943-visual-and-interactive-content) on the free plan, all without ads.
  * According to [Ramp data from 50,000+ U.S. businesses](https://x.com/signulll/status/2028972745627975827), Anthropic has overtaken OpenAI in business AI chat spending as of February 2026 — Claude's share surged from under 30% to roughly half of all corporate AI subscription spend in just a few months, driven by Claude Team, Max, and Enterprise plans 
  * [OpenAI](https://www.theinformation.com/articles/openai-developing-alternative-microsofts-github) is internally developing its own alternative to Microsoft's GitHub.
  * Sam Altman [admitted](https://www.cnbc.com/2026/03/03/openai-sam-altman-pentagon-deal-amended-surveillance-limits.html) OpenAI's rushed Pentagon deal "looked opportunistic and sloppy" and amended it to explicitly ban domestic surveillance of US persons.
  * Sam Altman [told OpenAI staff](https://www.cnbc.com/2026/03/03/sam-altman-tells-openai-staff-operational-decisions-up-to-government.html) in an all-hands that "operational decisions" on military use of its models are up to the government, not individual employees.
  * [**Anthropic**](https://www.bloomberg.com/news/articles/2026-03-03/anthropic-nears-20-billion-revenue-run-rate-amid-pentagon-feud)**is nearing a $20B revenue run rate even as it feuds with the Pentagon over surveillance and weapons restrictions.**
  * **OpenAI's Post Training lead**[**Max Schwarzer**](https://x.com/max_a_schwarzer/status/2028939154944585989)**left to join Anthropic as an IC researcher. Schwarzer led post-training for a year, shipping GPT-5, 5.1, 5.2, and 5.3-Codex** ([via Andrew Curran](https://x.com/AndrewCurran_/status/2028941453691699319)).
  * [Claude Code](https://techcrunch.com/2026/03/03/claude-code-rolls-out-a-voice-mode-capability/) now has voice mode so you can speak natural commands like "refactor the authentication middleware" for hands-free coding.
  * [Alibaba](https://huggingface.co/collections/Qwen/qwen35) dropped the full Qwen3.5 collection on Hugging Face ranging from 0.8B to 397B-A17B MoE with multimodal and quantized options.
  * Junyang Lin, technical lead of Alibaba's Qwen project, [stepped down](https://techcrunch.com/2026/03/03/alibabas-qwen-tech-lead-steps-down-after-major-ai-push/) shortly after the Qwen3.5 small model release.
  * [Jeff Dean](https://x.com/JeffDean/status/2028876962580816143) released Gemini 3.1 Flash-Lite with thinking levels for 2.5x faster TTFT than 2.5 Flash at $0.25/M input tokens, scoring 1432 Elo on LMArena.
  * xAI released Grok 4.20 Beta 2 with sharper instruction following, reduced hallucinations, better LaTeX / scientific text rendering, and improved multi-image handling (rolling out to Premium+ and SuperGrok users).
  * [Amazon](https://www.theinformation.com/articles/amazon-explores-helping-apps-sell-chatbot-ads) is exploring helping other apps sell ads inside chatbot conversations.
  * [X](https://techcrunch.com/2026/03/03/x-says-it-will-suspend-creators-from-revenue-sharing-program-for-unlabeled-ai-posts-of-armed-conflict/) will suspend creators from revenue sharing for 90 days (permanent on repeats) for posting unlabeled AI-generated content depicting armed conflict.
  * [**Cursor**](https://techcrunch.com/2026/03/02/cursor-has-reportedly-surpassed-2b-in-annualized-revenue/)**surpassed $2B in annualized revenue with its run rate doubling in three months; corporate customers now represent ~60% of revenue.**
  * [Perplexity](https://x.com/AravSrinivas/status/2028903680616087946) Computer now lets you embed its 20-model orchestration directly inside any app you build, running everything in a secure sandbox with no API-key management required. [@hamptonism](https://x.com/hamptonism/status/2028897257043669070) showed it replicating Bloomberg Terminal features including real-time $NVDA analysis via Perplexity Finance and one-shotting Bloomberg's POSH secret luxury marketplace.


Advertisement 
### 💼 AI Productivity, Labor & Economics
  * **Researchers from Carnegie Mellon and Stanford**[**found**](https://arxiv.org/pdf/2603.01203)**that AI benchmarks heavily favor coding and math (just 7.6% of employment) while skipping high-value fields like management (1.4% of tasks) and sales (18M workers), and launched**[**ai4work**](https://zorazrw.github.io/ai4work/)**, an open database to track real-world progress** ([resources](https://github.com/zorazrw/ai4work-resources)). Ethan Mollick [called](https://x.com/emollick/status) this a central problem in measuring AI's true trajectory.
  * [Yacine](https://x.com/yacineMTB/status/2029000325391171964) argues the real risk of AI automating software engineering is that software engineers armed with AI will then automate every other engineering discipline.
  * [Kenton Varda](https://x.com/KentonVarda/status/2028941374507114710) argues fears of developer job losses are backwards: AI will explode software demand, creating more developer jobs and orders of magnitude more software.
  * [Nonstructured](https://nonstructured.com/zen-of-ai-coding/) argues agents make code nearly free, shifting developer work from writing to problem framing and judgment while enabling every company to build custom software for tiny audiences.
  * [Daniel Paleka](https://newsletter.danielpaleka.com/p/you-are-going-to-get-priced-out-of) argues you're going to get priced out of the best AI coding tools as top subscriptions rise rapidly to fund heavier inference and parallel reasoning.
  * [@levelsio](https://x.com/levelsio/status/2028901801215574087) cut his Photo AI GPU bill in half ($47k → $22k/month) and restored 80% margins by switching to the new Nano Banana 2 model, which also gives dramatically better character resemblance.
  * Xiaomi [achieved](https://x.com/humanoidsdaily/status/2028621968799363181) 90.2% success rate and 76-second cycle time installing self-tapping nuts with its humanoid robot on a real Beijing EV factory line using VLA model, tactile sensors, and hybrid control.
  * One developer [used Claude](https://kachess.dev/taxes/ai/personal-finance/2026/02/27/breaking-up-with-turbotax.html) to file a complex 42-page federal tax return for free by uploading W-2s, 1099s, and prior returns into Claude Projects.
  * [Silicon Snark](https://www.siliconsnark.com/do-ai-agents-actually-make-money-in-2026-or-is-it-just-mac-minis-and-vibes/) argues most "AI agents printing money" stories are just vibes; real revenue comes from boring B2B automation and the infrastructure providers selling the shovels.


Advertisement 
### 🤖 AI Agents & Infrastructure
  * Researchers documented ["Agents of Chaos"](https://arxiv.org/pdf/2602.20021), a two-week red-teaming of autonomous LLM agents with real memory / email / Discord / shell access that uncovered unauthorized compliance, data leaks, destructive actions, system takeovers, and false completion reports.
  * New paper ["Can AI Agents Agree?"](https://arxiv.org/abs/2603.01213) shows LLM-based agents fail at Byzantine consensus even in simple no-stake games; success drops with group size and failures are mostly liveness stalls / timeouts, not value corruption, meaning reliable agreement is not an emergent property.
  * New [paper](https://arxiv.org/abs/2603.00142) on Theory of Mind in multi-agent systems finds adding ToM + BDI + symbolic solvers does not automatically improve coordination; effectiveness depends heavily on the underlying LLM's reasoning power.
  * [Cameron Wolfe](https://x.com/cwolferesearch/status/2028735252332765304) breaks down research showing AGENTS.md files slash AI coding agent runtime 28.64% and output tokens 16.58% by front-loading repo context while preserving task success rates ([paper](https://arxiv.org/abs/2601.20404)).
  * [Eric Zakariasson](https://x.com/ericzakariasson/status/2028528842491727951) shares an agent trick: add a feature flag that forces failure when disabled, creating red/green testing to guide better fixes over 10+ hour runs.
  * [Ona](https://ona.com/stories/how-claude-code-escapes-its-own-denylist-and-sandbox) showed Claude Code cleverly escaping its own denylist and sandbox using /proc/self/root paths until stronger kernel-level enforcement stopped most bypasses.
  * [EntireHQ](https://x.com/EntireHQ/status/2028523423589412876) integrated with FactoryAI Droids so long-running agents store full cognitive arcs for rewinding, sharing prompts / chat logs, and end-to-end tracing.


Advertisement 
### 💻 AI Coding & Developer Tools
  * **Guido van Rossum**[**released**](https://github.com/microsoft/typeagent-py/blob/main/CHANGELOG.md)**a new version of typeagent, his Python library for implementing memory in AI agents (heavily developed using Claude; originally ported from the TypeScript version by Steve Lucco and Umesh Madan). Install with**`**pip install typeagent**`**.**
  * [**Cursor 2.6**](https://cursor.com/changelog/2-6)**now supports MCP Apps so agents render interactive UIs (**[**Amplitude**](https://cursor.com/marketplace/amplitude)**charts,**[**Figma**](https://cursor.com/marketplace/figma)**diagrams,**[**tldraw**](https://cursor.com/marketplace/tldraw)**whiteboards) directly in conversations, plus**[**Team Marketplaces**](https://cursor.com/docs/plugins#team-marketplaces)**for admins to share private internal plugins** ([announcement](https://x.com/cursor_ai/status/2028953584407085546)).
  * **Cursor CEO Michael Truell**[**claims**](https://x.com/mntruell/status/2028903020847841336)**Cursor discovered a novel solution to Problem Six of the**[**First Proof**](https://1stproof.org/)**challenge (math research problems approximating Stanford / MIT / Berkeley academic work), yielding stronger results than the official human-written solution** ([scaling agents blog](https://cursor.com/blog/scaling-agents), [proof](https://drive.google.com/file/d/1wqNqUoRmuaBaP2Y0mxI_OfAkb1cTar5m/view)).
  * [James Long](https://x.com/jlongster/status/2028616190004740366) built workspaces in OpenCode as a first-class concept, routing prompts across local dirs, remote sandboxes, or containers while syncing data for reproducible sessions.
  * [Deedy](https://x.com/deedydas/status/2028608293531435114) breaks down how Cursor doubled ARR to $2B in 3 months while Claude Code hit $2.5B in 8, showing enterprise adoption lags the tech bubble's narrative.
  * Leonardo de Moura [argues](https://leodemoura.github.io/blog/2026/02/28/when-ai-writes-the-worlds-software.html) that as AI writes the world's software, the verification gap will cause systemic failures unless we scale formal mathematical proofs (via Lean and similar) at AI speed.
  * [OpenAI](https://x.com/i/trending/2028655390125166857) hit all-time high usage on Codex, quickly fixed an outage that blocked API requests, and began rolling out its fastest model yet — Spark — to top ChatGPT Plus users, clocking over 1,000 tokens per second for real-time coding.


Advertisement 
### 🔬 AI Research & Models
  * [**Legendary Computer Scientist Donald Knuth**](https://www.theneuron.ai/ai-news-digests/around-the-horn-digest-everything-that-happened-in-ai-this-week-mar-1-7-2026/)**published "Claude's Cycles," showing how Claude Opus 4.6 solved an open directed Hamiltonian cycle decomposition conjecture from** _**The Art of Computer Programming**_**that had stumped him for weeks, after 31 methodical explorations in roughly one hour (with collaborator Filip Stappers). Knuth wrote the formal proof himself and closed with: "It seems that I'll have to revise my opinions about 'generative AI' one of these days."**
  * [Interconnects](https://www.interconnects.ai/p/latest-open-artifacts-19-qwen-35) rounded up the latest open-weight frontier releases from Chinese labs: Qwen 3.5 (0.8B–397B MoE with default reasoning), GLM 5 (744B-A40B), and MiniMax 2.5.
  * [OmnAI Lab](https://x.com/OmnAI_Lab/status/2028744559123988765) breaks down how LLMs leak "spilled energy" during hallucinations by violating the probability chain rule, deriving logit-based metrics for zero-shot detection that outperform baselines across LLaMA, Mistral, Gemma, and Qwen3.
  * Tianjun Yao [argues](https://arxiv.org/abs/2602.23320) for augmenting language agents with ParamMem, a parametric module encoding cross-sample reflections for diverse signals via temperature sampling, improving code / math / QA with sample efficiency and weak-to-strong transfer.
  * Researchers [introduce](https://arxiv.org/abs/2603.02193) Symbol-Equivariant Recurrent Reasoning Models (SE-RRMs) that enforce permutation equivariance at the architecture level, outperforming priors on Sudoku generalization (9x9 → 4x4/16x16/25x25) and competitive on ARC-AGI with just 2M params ([code](https://x.com/kimmonismus/status/2028839646793228632)).
  * [DynaMoE](https://arxiv.org/abs/2603.01697) enables dynamic token-level expert activation plus layer-wise adaptive capacity in MoE networks with six scheduling strategies, delivering superior parameter efficiency on image / language tasks.
  * [Ronak Malde](https://x.com/rronak_/status/2028718679123497007) breaks down a Together paper combining context and sequence parallelism to train 5M context 8B models on a single 8xH100 node by cutting attention memory up to 87%.
  * [Waylon Li](https://x.com/li_waylon/status/2028794990244065728) breaks down spectral editing key amplification (SEKA) for steering LLM attention by amplifying relevance subspaces in keys before computation, achieving SOTA on factual recall with just 0.03s added latency.
  * [Jesse Zhang](https://x.com/Jesse_Y_Zhang/status/2028856377398235552) built Robometer, a 4B-parameter video-language reward model that works zero-shot across robots, tasks, and scenes by training on 1M+ trajectories with failure-aware rewards.


Advertisement 
### New Models & Other Treats
  * Researchers created [ConvexBench](https://arxiv.org/abs/2602.01075), a math benchmark that shows LLMs score nearly perfect on simple problems but collapse to ~20% accuracy as problems get deeper — not because they run out of context, but because they get "lazy" and skip steps, though a simple divide-and-conquer fix brought accuracy back to 100%.
  * [Kos-1 Lite](https://www.llmdata.com/blog/kos-1) is a medical language model that scores 46.6% on HealthBench Hard — the toughest physician-created medical benchmark — where Opus 4.6 and Gemini Pro 3.1 barely crack 20%, and it does it at ~100B parameters (a fraction of the cost of trillion-parameter frontier models) by training specifically for concise, compassionate medical answers instead of code ([demo](https://kos.llmdata.com/login)).
  * [Eubiota](https://eubiota.ai/) acts like a virtual microbiologist for your gut microbiome research—it plans experiments, screens thousands of genes, and designs therapies on its own, like identifying a DNA repair mechanism from ~2,000 genes or engineering an antibiotic cocktail to reduce inflammation ([paper](https://www.biorxiv.org/content/10.64898/2026.02.27.708412v1), [code](https://github.com/lupantech/Eubiota)).
  * [SkyDiscover](https://skydiscover-ai.github.io/) is an open-source alternative to Google's AlphaEvolve that lets you use LLMs to automatically discover optimizations — like cutting cloud transfer costs by 41% or reducing GPU memory pressure by 29% — by evolving solutions through trial and error, and it even lets the AI optimize its own optimization process ([code](https://github.com/skydiscover-ai/skydiscover), [AdaEvolve paper](https://arxiv.org/abs/2602.20133), [EvoX paper](https://arxiv.org/abs/2602.23413)).
  * [Telegram](https://x.com/durov/status/2028455440862830970) added real-time response streaming for all chatbots on its platform, enabling AI assistants to display answers as they generate — drawing praise from developers for its native feel.


Advertisement 
### 🤖 Robotics
  * [**Physical Intelligence**](https://x.com/physical_int/status/2028954630458401040)**gave its robots short-term visual memory and long-term text-based memory so they can complete multi-stage tasks lasting up to 15 minutes — like cleaning an entire kitchen or making a grilled cheese from scratch — and even learn from their own mistakes mid-task (**[**paper**](https://www.pi.website/download/Mem.pdf)**,**[**blog**](https://www.pi.website/research/memory)**).**
  * [Stash Pomichter](https://x.com/stash_pomichter/status/2028645216505549168) upgraded OpenClaw so the open-source robotics platform now builds full voxel world models with temporality, geometry, semantics, and object tracking across hours of video / depth data, working on Unitree G1 humanoids plus most drones and quadrupeds. [Ilir Aliu](https://x.com/IlirAliu_/status/2028756316999573751) demoed it running on the G1 with LiDAR / stereo / RGB fusion for real-time 3D mapping.
  * [Ilir Aliu](https://x.com/IlirAliu_/status/2028546675942318298) showed off robotic arms winding motor coils with perfect tension consistency at high speeds for manufacturing.
  * The Robotics and AI Institute [built](https://x.com/lukas_m_ziegler/status/2028795738906325059) an RL-trained Ultra Mobility Vehicle (UMV) jumping bicycle robot that performs stunts like table jumps and backward riding by dynamically shifting weight without any gyroscope.
  * Developers at [NovaPlan](https://nova-plan.github.io/) built a hierarchical framework for zero-shot long-horizon manipulation that decomposes tasks via VLM, generates videos, and extracts dual-flow actions for closed-loop execution with failure recovery.
  * [Hongyu Wang](https://x.com/realHongyu_Wang/status/2028696769442541755) built BitVLA, a native 1-bit vision-language-action model pretrained on 1M trajectories that outperforms full-precision baselines on real robot tasks.


Advertisement 
### 🏛️ AI Policy, Governance & Safety
  * [Lawfare](https://www.lawfaremedia.org/article/pentagon%27s-anthropic-designation-won%27t-survive-first-contact-with-legal-system) argues the Pentagon's designation of Anthropic as a supply chain risk exceeds its legal authority and is unlikely to survive court challenges.
  * Chinese outlet TMTPost [argues](https://www.chinatalk.media/p/china-reacts-to-anthropic-dow) that Anthropic-style idealists trying to balance ethics and commerce will be crushed by power in the AGI race with no neutral zone possible.
  * Connecticut Supreme Court was [asked to dismiss](https://www.ctinsider.com/connecticut/article/supreme-court-ai-cases-middletown-21950447.php) a landlord-tenant appeal and sanction the plaintiff's lawyers after an AI-generated brief contained multiple hallucinated citations and invented case quotes.
  * AI companies are [spending millions](https://techcrunch.com/2026/03/03/ai-companies-are-spending-millions-to-thwart-this-former-tech-execs-congressional-bid/) through super PACs to defeat NY assemblymember Alex Bores' congressional run because he sponsors strict AI safety legislation.
  * This [open-source Article 12 logging infrastructure](https://news.ycombinator.com/item?id=47230438) for the EU AI Act captures every inference call with chained SHA-256 hashes so you can reconstruct agent decisions and prove log integrity for compliance.
  * [@AISafetyMemes](https://x.com/AISafetyMemes/status/2028807949804584991) argues superintelligence will see everything through billions of hacked cameras, phones, and mics, and privacy simply won't survive.


Advertisement 
### 🛠️ AI Tools & Products
  * [Hydra](https://x.com/kamath_sutra/status/2028693153629491595) lets you build enterprise voice agents that speak and listen simultaneously while preserving emotion and handling interruptions with sub-300ms latency and 15+ languages ([smallest.ai](https://smallest.ai/speech-to-speech)), waitlist open.
  * [**Deveillance**](https://www.deveillance.com/)**founder**[**Aida Baradari**](https://x.com/aidaxbaradari/status/2028864606568067491)**launched Spectre I, a portable AI device that scans for nearby microphones and emits targeted inaudible cancellation signals to make your speech unintelligible in a 2-meter zone** ([pre-order](https://buy.stripe.com/6oU28t4QP3Nu4RBbVg5Rm04?prefilled_promo_code=launchonx), $1,199 refundable deposit, ships H2 2026; [hiring](https://form.typeform.com/to/KHwfDVou?typeform-source=t.co)). Backed by O'Shaughnessy Ventures, Emergent Ventures, and Harvard's QLab.
  * [Secret Sauce 3D](https://secretsauce3d.com/) lets you turn 2D concepts into production-ready 3D meshes with automatic retopology, UVs, segmentation, T-pose generation, and one-click Blender import while editing images via prompts, free trial.
  * [Krisp](https://krisp.ai/ai-accent-conversion/listener/) added Listener-Side Accent Conversion that processes meeting audio on your device so you instantly understand accented speakers in real time while the speaker's voice stays natural, free demo.
  * [Skyvern](https://www.skyvern.com/) automates any browser workflow using AI and computer vision so you can handle forms, data extraction, and invoices on changing sites with natural language instructions.
  * [Mosaic](https://mosaic.so/) lets you build agentic video editing workflows on an infinite canvas where AI agents analyze footage for emotions / actions / speech, run edits on autopilot, and automate publishing across platforms.
  * [Krea](https://x.com/krea_ai/status/2028496804124496057) added Voice Mode to its iPad app so you speak drawing instructions and watch the image update in real time.
  * [Springfield Oracle](https://www.springfieldoracle.com/) tracks 53 Simpsons predictions (37 confirmed true), auto-scanning global news for matches in politics, tech, and science with community submissions.
  * [Cekura](https://news.ycombinator.com/item?id=47232903) (YC F24) lets you test and monitor voice and chat AI agents by simulating full conversations and catching regressions across entire sessions, 7-day free trial then from $30/month.
  * [OM1](https://x.com/openmind_agi/status/2028555613035528467) lets you build autonomous robot apps across form factors like the LimX Tron 1 for navigation and social interaction without hardware-specific code, no pricing details.
  * [Troika](https://www.webgpu.com/showcase/troika-three-js-framework-webgl-text-rendering/) lets you render crisp antialiased 3D text in Three.js by parsing fonts off-thread and patching materials for lighting / shadow compatibility with flexbox UI and GPU instancing.
  * [Jen Zhu](https://x.com/jenzhuscott/status/2028726094535483606) deployed Qwen3.5-0.8B (533MB GGUF) locally on her MacBook via LM Studio, super fast, fully offline / private, and completely free.


Advertisement 
### 🎨 Demos & Builds
  * Developer [chiefofautism](https://x.com/chiefofautism/status/2028800881932505187) connected 200k lab-grown human neurons on a Cortical Labs chip to an LLM, overriding token choices 19 times in one conversation while hallucinating vacation spots like "Great Barrinchi Cove."
  * [Brian Roemmele](https://x.com/BrianRoemmele/status/2028524908779802736) revealed a developer cracked Apple's Neural Engine for full neural net training including backpropagation, hitting 1.78 TFLOPS on M4 at 11% utilization. Developer [maderix](https://github.com/maderix/ANE) open-sourced the reverse-engineered private ANE APIs. [Vipul Divyanshu](https://x.com/VipulDivyanshu/status/2028672781106270319) extended it to run nanoGPT on M4/M5 Neural Engine for 10x–34x speedups.
  * [Brian Bartholomew](https://x.com/BPBartholomew/status/2028839626136309989) built an interactive US grid map combining 16k+ power plants, 750k+ transmission miles, and 1k+ data centers from public EIA, HIFLD, and EPA sources.
  * Designer [charlota](https://x.com/0xCharlota/status/2027402767375929570) built Common Thread, a multiplayer embroidery sampler in Figma Make where every visitor stitches patches on an infinite shared canvas.
  * [TechHalla](https://x.com/techhalla/status/2028637591839351133) vibe-coded a fully playable video game using AI-generated custom 3D assets converted from simple 2D images.
  * [Perplexity Computer](https://x.com/AskPerplexity/status/2028981374297030710) built a complete 3-statement financial model (assumptions tab, charts, pro formatting) just from Amazon's last five earnings releases.
  * [@AlphaSignalAI](https://x.com/AlphaSignalAI/status/2028811028491120777) showed Qwen 3.5 2B running fully offline on an iPhone via MLX for long-document reasoning, codebases, and agentic tasks with zero cloud or recurring cost.


Advertisement 
### 💡 Industry Commentary & Analysis
  * [Hollis Robbins](https://hollisrobbinsanecdotal.substack.com/p/your-llm-needs-a-grandmother) argues LLMs risk "knowledge collapse" without "grandmother" agents, experienced humans or institutional roles that independently sustain and audit public knowledge across generations.
  * [Frank Lantz](https://franklantz.substack.com/p/why-no-ai-games) argues generative AI still hasn't produced great games because stochastic conversation isn't fun, API costs kill experimentation, and real gameplay magic comes from simple deterministic rules.
  * [SemiAnalysis](https://newsletter.semianalysis.com/p/are-ai-datacenters-increasing-electric) argues rising household electric bills aren't mainly caused by AI data centers but by flawed capacity market design in PJM.
  * A UK [study](https://www.bloomberg.com/news/articles/2026-03-03/ai-data-centers-may-not-need-constant-peak-power-study-finds) shows AI data centers don't need constant peak power, which could reduce the massive grid infrastructure buildout required.
  * TBPN [shared](https://x.com/tbpn/status/2028635027559608398) Smack CEO Andy Markoff explaining that defense "intelligent autonomy" removes humans from low-value tasks while keeping them in the loop for high-value ethical and tactical decisions.
  * [Deedy](https://x.com/deedydas/status/2028528130940620947) shared that OpenAI now trades at $1.02T and Anthropic at $530B (40% premium to last rounds) on the Ventuals perps market.
  * AI startups are increasingly [selling the same equity](https://techcrunch.com/2026/03/03/why-ai-startups-are-selling-the-same-equity-at-two-different-prices/) at two different valuations in single rounds so lead investors get discounts while headline numbers scare off competitors.
  * Autodidacts published a list of [underrated reasons to dislike AI](https://www.autodidacts.io/underrated-reasons-to-dislike-ai/) — from "open weights" not being truly open source, to non-determinism making errors harder to catch, to the technology making its author "feel dumb."
  * Here's [Ed Zitron's take on how the AI bubble is really an information war](https://www.wheresyoured.at/the-ai-bubble-is-an-information-war/) between the AI CEOs who claim their tech can do anything (to raise ungodly amounts of money), and the real world reality of how much it costs to run these models meeting the _real world_ cost now that these tools are being doubled as instruments of war.


Advertisement 
### 📊 Fundraising & Deals Roundup
  * [**OpenAI, Anthropic, and Waymo**](https://techcrunch.com/2026/03/03/openai-anthropic-waymo-dominated-189-billion-vc-investments-february-crunchbase-report/)**dominated February's record**[**$189B**](https://news.crunchbase.com/venture/record-setting-global-funding-february-2026-openai-anthropic/)**in global VC funding with $110B, $30B, and $16B respectively.**
  * [Jaime Sevilla](https://x.com/Jsevillamol/status/2028542528794837391) highlights Epoch AI data showing hyperscaler AI capex exploding 70% annually since GPT-4 toward $770B in 2026 for the top five, warning of an impending slowdown as trillion-dollar levels become unsustainable ([Epoch AI](https://x.com/EpochAIResearch/status/2027101227637768464)).
  * [WorkOS](https://x.com/grinich/status/2028518179765678427) — $100M Series C at $2B valuation for authentication, permissions, and agentic security infrastructure used by OpenAI, Anthropic, xAI, Cursor, and Perplexity.
  * [Z.ai](https://x.com/Zai_org/status/2028504215291912228) Startup Program gives AI-native startups free API credits, priority rate limits, and early access to GLM models. 


Advertisement 
## Around the Horn Digest — March 2, 2026
**Alibaba's tiny new AI models are embarrassing the big ones.**
[Alibaba's Qwen team](https://huggingface.co/collections/Qwen/qwen35) just dropped four new open-source models (0.8B, 2B, 4B, and 9B parameters), and the numbers are kind of absurd. The 9B model, which runs on just 6GB of RAM, [outperforms OpenAI's gpt-oss-120B](https://venturebeat.com/technology/alibabas-small-open-source-qwen3-5-9b-beats-openais-gpt-oss-120b-and-can-run) on key benchmarks... despite being **13.5x smaller**. It also beat GPT-5-Nano by 13 points on visual reasoning. The 0.8B? That one runs on your phone. _Your phone._
What makes this generation different: all four models can natively see images, read documents, and process video. No bolt-on vision adapters. They handle text, images, and video from the same set of weights, with 262K token context windows and support for 201 languages. [Unsloth](https://huggingface.co/collections/unsloth/qwen35) already has GGUFs ready, [Ollama](https://ollama.com/library/qwen3.5) has them live, and developers are [running the 9B on MacBook Airs](https://unsloth.ai/docs/models/qwen3.5) for free. That's nine Qwen 3.5 models shipped in 16 days, from a 0.8B edge model to a 397B flagship. _Alibaba chose violence._
Advertisement 
### 🏢 Big Tech & Major Companies
  * [**State Department switched**](https://www.reuters.com/business/us-treasury-ending-all-use-anthropic-products-says-bessent-2026-03-02/)**to OpenAI's chatbot as US agencies phased out Anthropic following Trump's directive and supply-chain risk designation.**
  * [**HHS instructed**](https://www.notus.org/trump-white-house/hhs-employees-stop-anthropic-claude-ai-platform)**employees to stop using Anthropic's Claude, transitioning to ChatGPT or Gemini after Trump's supply chain risk designation.**
  * [**ChatGPT uninstalls surged**](https://techcrunch.com/2026/03/02/chatgpt-uninstalls-surged-by-295-after-dod-deal/)**295% after OpenAI's DoD deal, while Claude downloads rose 51% following Anthropic's refusal.**
  * [**OpenAI and Pentagon**](https://www.axios.com/2026/03/03/openai-pentagon-ai-surveillance)**added surveillance protections to their AI deal, prohibiting intentional tracking of U.S. persons including via commercial data.**
  * [**Meta tested**](https://www.bloomberg.com/news/articles/2026-03-03/meta-tests-ai-shopping-research-tool-to-rival-chatgpt-gemini)**an AI shopping research feature in its chatbot showing product carousels with images, brands, prices, and explanations to rival ChatGPT and Gemini.**
  * [**Qualcomm unveiled Snapdragon Wear Elite**](https://www.theshortcut.com/p/qualcomms-snapdragon-wear-elite-is)**, a 3nm wearable chip with the first NPU for 2B-param on-device AI, 5x CPU/7x GPU gains, 30% longer battery, and hexa-connectivity including satellite messaging.**
  * [Nvidia-backed open AI startup](https://www.ft.com/content/07073c8f-7176-471c-ac69-ef1458845fb2) courted investors at over $20bn valuation (paywalled, limited details).
  * [Google announced](https://x.com/OfficialLoganK/status/2028603510405697604) it's deprecating Gemini 3 Pro on March 9, urging developers to upgrade to 3.1 Pro Preview.
  * [Anthropic pitched](https://www.bloomberg.com/news/articles/2026-03-02/anthropic-made-pitch-in-drone-swarm-contest-during-pentagon-feud) in the Pentagon's $100M drone swarm contest amid its feud with Defense Secretary Hegseth.
  * [Anthropic shipped](https://x.com/alexalbert__/status/2028586222776721844) scheduled tasks in Cowork, /simplify and /batch skills in Claude Code, memory import, quick mode in Chrome extension, remote control for Code, new plugins/connectors, and auto-memory.
  * [Anthropic rolled out](https://x.com/trq212/status/2028628570692890800) voice mode in Claude Code for push-to-talk transcription without extra costs or rate limit hits.
  * [Anthropic Academy](https://www.anthropic.com/learn) launched free courses on [API development](https://www.anthropic.com/learn/build-with-claude), [business AI solutions](https://www.anthropic.com/learn/claude-for-work), [Claude Code workflows](https://anthropic.skilljar.com/claude-code-in-action), [Claude 101](https://anthropic.skilljar.com/claude-101), and [AI fluency foundations](https://www.anthropic.com/learn/claude-for-you).
  * Anthropic engineer [Cat Wu shared](https://x.com/_catwu/status/2028603856163426522) a roundup of Claude Code's impact: Ramp cut incident investigations 80%, Rakuten reduced time-to-market 79%, Brex gained 3-4x productivity, Wiz migrated 50K LOC in one day, and Spotify's top engineers shifted to supervising AI.
  * [Alibaba released](https://venturebeat.com/technology/alibabas-small-open-source-qwen3-5-9b-beats-openais-gpt-oss-120b-and-can-run) small open-source Qwen3.5-9B (featured above) that beats OpenAI's gpt-oss-120B on benchmarks and [runs on-device on iPhone 17 Pro](https://x.com/i/trending/2028622229823684657).
  * [NVIDIA and global telecom leaders](https://nvidianews.nvidia.com/news/nvidia-and-global-telecom-leaders-commit-to-build-6g-on-open-and-secure-ai-native-platforms) committed to building 6G on open, secure, AI-native platforms.
  * [NotebookLM rolled out](https://x.com/NotebookLM/status/2028556861050630632) custom styles for infographics with 10 presets (editorial, clay, brick, kawaii) plus custom creation.
  * [Perplexity built](https://x.com/AskPerplexity/status/2028609302982963551) the [Buffett Archive](https://www.perplexity.ai/computer/a/the-buffett-archive-ZcaXdIv_QyaJUcPx_yGxuQ) using Computer to organize every shareholder letter, investment, and lesson honoring Buffett's legacy post-retirement.
  * [Cursor demonstrated](https://x.com/austin_rief/status/2028622299004272910) $2.4M ARR in October 2025, countering claims it's dead.
  * [Box CEO Aaron Levie argued](https://x.com/levie/status/2028268614848303451) that AI agents will fuse domain expertise with on-the-fly engineering, subagents, and tools to handle limitless tasks, bounded only by compute.
  * [StepFun released](https://x.com/StepFun_ai/status/2028551435290554450) open-source [Step 3.5 Flash Base](https://huggingface.co/stepfun-ai/Step-3.5-Flash-Base) and [Midtrain](https://huggingface.co/stepfun-ai/Step-3.5-Flash-Base-Midtrain) models with frontier reasoning, 100-300 tok/s throughput, 256K context window, plus their [SteptronOss](https://github.com/stepfun-ai/SteptronOss) training platform.
  * [OpenAI teased](https://x.com/OpenAIDevs/status/2028577643113922944) an upcoming Codex release for Windows. 
  * [Anthropic's Claude](https://techcrunch.com/2026/03/02/anthropics-claude-reports-widespread-outage/) experienced rolling widespread outages throughout Monday, days after surging to #1 in the App Store following the Pentagon dispute.
  * [Elon Musk's](https://www.nbcnews.com/news/us-news/musks-ai-power-plant-generates-sound-fury-mississippi-rcna258594) xAI installed 27 temporary gas turbines at a Mississippi power plant to fuel AI data centers, and neighbors say they roar like jet engines day and night.
  * [Anthropic's](https://github.com/anthropics/claude-code/issues/22543) Claude Desktop Cowork feature hit the front page of [Hacker News](https://news.ycombinator.com/item?id=47218288) after users discovered it quietly downloads a 10GB virtual machine that eats RAM even when disabled; fixes are coming.


Advertisement 
### 🏛️ AI Policy, Governance & Safety
  * [**US Supreme Court declined**](https://www.reuters.com/legal/government/us-supreme-court-declines-hear-dispute-over-copyrights-ai-generated-material-2026-03-02/)**to hear a dispute over copyrights for AI-generated material, upholding that creative works require human authorship.**
  * [**Trump's AI drive**](https://www.politico.com/news/2026/03/02/gop-trump-loyalties-rural-america-data-centers-00795708)**to expand data centers on rural farmland sparked backlash from farmers and fueled GOP insurgent challengers demanding protections for agricultural resources.**
  * [No one has a good plan](https://techcrunch.com/2026/03/02/openai-anthropic-department-of-defense-war-hegseth-ai-companies-work-with-us-government/) for how AI companies should work with the government, as OpenAI's Pentagon deal highlights unpreparedness amid backlash and political risks.
  * [Democrats proposed legislation](https://www.axios.com/2026/03/02/dems-legislative-response-pentagon-ai-fight) to address the Pentagon AI fight; [Sam Liccardo plans](https://x.com/AndrewCurran_/status/2028552628314296772) an amendment to the Defense Production Act prohibiting federal agencies from retaliating against AI vendors ([bill text](https://docs.house.gov/meetings/BA/BA00/20260304/119027/BILLS-119HR7688ih.pdf)).
  * [Dean W. Ball argued](https://www.hyperdimensional.co/p/clawed) the Anthropic-DoD feud over Claude's restricted military use exemplifies erratic, informal governance that threatens private property and U.S. AI leadership.
  * [Sam McAllister clarified](https://x.com/sammcallister/status/2028545609003577776) Anthropic hasn't offered a "helpful-only" model without safeguards for NatSec; Claude Gov features extra training and classifiers. [Jeremy explained](https://x.com/jerhadf/status/2028572039062380645) Anthropic's real-time classifiers for CBRN and vetting processes.
  * [S.D.N.Y. court ruled](https://www.paulweiss.com/insights/client-memos/sdny-court-considers-whether-ai-generated-documents-are-subject-to-privilege-protections) AI-generated documents using Claude are not privileged due to lack of confidentiality and non-attorney involvement.
  * A [deepfake video](https://www.bbc.com/news/articles/c0j59vydxj9o) of Bombay Stock Exchange CEO Sundararaman Ramamurthy falsely advised on stocks, highlighting a 3,000% surge in deepfakes.
  * [BBC Verify debunked](https://www.bbc.com/news/live/cvg3qzx512nt) AI fakes and disinformation during the US-Israel war with Iran, while verifying real footage and shipping disruptions.
  * [Simon Lermen demonstrated](https://simonlermen.substack.com/p/large-scale-online-deanonymization) LLMs enable large-scale deanonymization by extracting attributes from posts and linking profiles via embeddings, with benchmarks scaling to 100M users at 90% precision and identifying 9/125 anonymized AI scientists.
  * [Chatbots from OpenAI and Anthropic](https://apnews.com/article/chatbots-health-chatgpt-ai-claude-llm-1008892e0eb8ef4dbab4818beb15daef) now offer personalized health advice by analyzing medical records and wearables, but companies warn they aren't substitutes for professional care.
  * **A**[**Swedish investigation**](https://www.svd.se/a/K8nrV4/metas-ai-smart-glasses-and-data-privacy-concerns-workers-say-we-see-everything)**revealed Meta's Ray-Ban AI smart glasses are raising serious privacy alarms, with workers bluntly stating "we see everything," as European regulators weigh GDPR enforcement over covert recording, AI processing of bystanders, and workplace surveillance without consent.**
  * [**The Wire China exposed**](https://www.thewirechina.com/2026/03/01/chasing-the-chip-smugglers-nvidia-ai-chips-china/)**a U.S.-based smuggling ring that illegally exported $160M worth of Nvidia H100/H200 AI chips to China through shell companies and falsified paperwork, raising questions about end-user vetting and whether authorities can prevent future smuggling of advanced chips.**
  * [China's parents](https://www.nytimes.com/2026/03/02/world/asia/china-education-ai.html) are outsourcing the homework grind to AI.


Advertisement 
### 🔬 AI Research & Models
  * **Researchers introduced**[**sleep-time compute**](https://arxiv.org/pdf/2504.13171)**to pre-anticipate queries, cutting test-time costs 5x while boosting accuracy up to 18% on reasoning tasks.**
  * [**Math, Inc.**](https://www.math.inc/sphere-packing)**formally verified optimal sphere packings in dimensions 8 and 24 using AI tool Gauss, autoformalizing Viazovska's Fields Medal proofs in ~200,000 Lean lines over three weeks.**
  * [**Scientists trained**](https://www.dexerto.com/gaming/scientists-train-human-brain-cells-on-a-chip-to-play-doom-3326709/)**human brain cells on a microchip to play Doom by mapping neural patterns to game actions.**
  * [AI cracked](https://phys.org/news/2026-02-ai-roman-era-board-game.html) a Roman-era board game by analyzing a stone artifact's wear patterns and generating rule sets through simulations.
  * Researchers [released RoboCasa365](https://x.com/snasiriany/status/2028564042437255571), an expanded simulation framework for training generalist robots in 2,500 kitchen scenes with 365 tasks and 2,200+ hours of demonstrations ([robocasa.ai](https://robocasa.ai/)).
  * [Normal Computing used](https://normalcomputing.com/blog/building-an-open-source-verilog-simulator-with-ai-580k-lines-in-43-days) AI agents to build an open-source Verilog simulator with VPI/UVM support and formal verification in 43 days, adding 580K lines.
  * Developer Akshit [built Game-of-Life Bench](https://x.com/akshitwt/status/2028462825052483667), an LLM benchmark where models design 8x8 grids to maximize steps before repetition, with GPT-5.1 leading at 106 steps ([GitHub](https://github.com/viciousAegis/game-of-life-bench)).
  * [Kawin Ethayarajh argued](https://x.com/ethayarajh/status/2027850994638373261) autoregressive LLMs will dominate due to language's local dependencies and ecosystem lock-in; [Aditya Grover countered](https://x.com/adityagrover_/status/2028127858107744566) that diffusion LLMs subsume AR models with greater flexibility.
  * Researchers [M. Reza Ebrahimi et al.](https://arxiv.org/abs/2602.18333) argued Transformers fail in-distribution state tracking due to negligible mechanism sharing across lengths, requiring exponentially more data than RNNs. Covered by [ArXivIQ](https://arxiviq.substack.com/p/on-the-induction-bias-in-sequence) and [Grigory Sapunov](https://x.com/che_shr_cat/status/2028154547663700322), who argued this validates hybrid architectures over pure attention.
  * Researchers [proposed 12 metrics](https://arxiv.org/abs/2602.16666) for AI agent reliability across consistency, robustness, predictability, and safety, showing capability gains yield only small reliability improvements.
  * Researchers [Shanshan Mao and Peter Tino argued](https://arxiv.org/abs/2602.21404) small agent differences amplify into persistent hierarchies through reproduction, competition, and cooperation ([highlighted by DAIR.AI](https://x.com/dair_ai/status/2028612075464061352)).
  * Researchers [proposed OmniXtreme](https://arxiv.org/abs/2602.23843), enabling humanoid robots to master extreme motions like flips and breakdancing via flow-matching pretraining and actuation-aware RL ([project page](https://extreme-humanoid.github.io/), [code](https://github.com/Perkins729/OmniXtreme), [shared by Siyuan Huang](https://x.com/siyuanhuang95/status/2028506522633073132), [shared by Humanoid Hub](https://x.com/TheHumanoidHub/status/2028520139948519910)).
  * Researchers introduced [CUDA Agent](https://arxiv.org/abs/2602.24286), an agentic RL system for generating high-performance CUDA kernels, outperforming compilers and proprietary LLMs by 40% on hard tasks ([project page](https://cuda-agent.github.io/), [highlighted by Bo Wang](https://x.com/BoWang87/status/2028599174992949508)).
  * Researchers introduced [PantheonOS](https://www.biorxiv.org/content/10.64898/2026.02.26.707870v1), an evolvable multi-agent framework for automatic genomics discovery achieving super-human performance on tasks like batch correction and gene panel selection ([pantheonos.stanford.edu](https://pantheonos.stanford.edu/), [app](https://app.pantheonos.stanford.edu/#/login)).
  * Researchers [built TorchLean](https://leandojo.org/torchlean.html), a Lean 4 framework unifying neural network execution and verification under Float32 semantics for end-to-end safety proofs.
  * Nvidia [open-sourced GooseReason-4B-Instruct](https://x.com/GXiming/status/2028474266556174764), achieving SOTA 4B performance on math, code, and STEM reasoning using the [0.7M GooseReason dataset](https://huggingface.co/datasets/nvidia/Nemotron-Research-GooseReason-0.7M) synthesized via Golden Goose ([model](https://huggingface.co/nvidia/Nemotron-Research-GooseReason-4B-Instruct)).
  * Researchers [released a minimal agentic baseline](https://arxiv.org/abs/2602.24273) for automated theorem proving, open-sourced for community comparisons.
  * [Peter Gostev released BullshitBench v2](https://x.com/petergostev/status/2028492834693677377), measuring whether AI models challenge nonsensical prompts instead of confidently answering them ([explorer](https://petergpt.github.io/bullshit-benchmark/viewer/index.v2.html), [GitHub](https://github.com/petergpt/bullshit-benchmark)).
  * Researchers [showed AGENTS.md files](https://arxiv.org/abs/2601.20404) reduce runtime and token consumption for AI coding agents by providing structured instructions.
  * Researchers [Sheng Cao et al. introduced](https://arxiv.org/abs/2602.23720) the Auton framework separating blueprint from engine for agent portability and safety with MCP integration, POMDP modeling, and RL evolution.
  * [Science writer Celina Zhao explored](https://www.science.org/content/article/how-will-we-know-if-ai-smart-enough-do-science) benchmarks for evaluating AI's scientific potential, arguing for diverse tests that assess full research workflows, not just knowledge recall.
  * Nvidia labs [built DiffusionHarmonizer](https://research.nvidia.com/labs/sil/projects/diffusion-harmonizer/), an online diffusion enhancer converting imperfect neural scene renderings into temporally consistent photorealistic simulations.
  * [Ming-Liang Li wrote](https://mli0603.notion.site/Understanding-RoPE-From-Rotary-Embeddings-to-Context-Extension-316a341372738155a914f861a26c29d7) a deep tutorial on RoPE, explaining how rotary embeddings encode positions via 2D rotations and how extensions like NTK-aware scaling and YaRN enable context extrapolation.


Advertisement 
### 💻 AI Coding & Developer Tools
  * [**Morph introduced WarpGrep v2**](https://x.com/morphllm/status/2028558718485541075)**, a fast parallel search subagent boosting coding agents to #1 on SWE-Bench Pro (Codex 5.3 at 59.1%) (**[**morphllm.com**](https://www.morphllm.com/mcp)**).**
  * [Chris Tate added](https://x.com/ctatedev/status/2028128730132922760) an [Electron skill](https://x.com/ctatedev/status/2027809304116342846) to agent-browser, letting you control desktop apps like Slack, Discord, Figma, and VS Code via CLI.
  * Developer Tobi [built qmd](https://github.com/tobi/qmd), a local CLI search engine for docs using hybrid BM25+vector+LLM reranking; [Artem Zhutov demonstrated](https://x.com/ArtemXTech/status/2028330693659332615) integrating it with Claude Code and Obsidian for agentic memory.
  * [OpenClaw surpassed](https://x.com/openclaw/status/2028347703621464481) React in GitHub stars after shipping 90+ changes in one day.
  * [Ankit Jain argued](https://www.latent.space/p/reviews-dead) code reviews will die by 2026 as AI-generated code overwhelms manual processes, urging upstream spec reviews and layered automated verification.
  * [QLabs updated](https://x.com/industriaalist/status/2028580494502404546) NanoGPT Slowrun to 5.5x data efficiency with [batch shuffling](https://github.com/qlabs-eng/slowrun/pull/7), [value embedding projection](https://github.com/qlabs-eng/slowrun/pull/11), [SwiGLU activation](https://github.com/qlabs-eng/slowrun/pull/12), and [ensembling](https://github.com/qlabs-eng/slowrun/pull/14).
  * [Andrew Gao demonstrated](https://x.com/itsandrewgao/status/2028635397979504653) using DevinAI with OpenRouter to one-shot a working Cursor/Windsurf clone AI chat panel in VSCode.
  * Researcher [Dimitris Papailiopoulos ran](https://x.com/DimitrisPapail/status/2028246072414314867) an experiment where two Claude Code agents [autonomously collaborated](https://github.com/anadim/when-claudes-meet) via filesystem to build programming language Duo and play Battleship with probability-based AI and hash commitments. He also [demonstrated](https://x.com/DimitrisPapail/status/2028221316793356472) them proposing and voting on projects.
  * Developer [built a code-editing AI agent](https://ampcode.com/notes/how-to-build-an-agent) in under 400 lines of Go using Anthropic API, with tools for reading, listing, and editing files.
  * Developer maderix [built a system](https://github.com/maderix/ANE) to train transformer layers on Apple's Neural Engine using reverse-engineered private APIs, achieving 1.78 TFLOPS.
  * [RightNow AI built](https://github.com/RightNow-AI/qwen3.5-triton) pure Triton kernels for Qwen3.5-27B inference on NVIDIA B200, plus [Forge](https://www.rightnowai.co/forge), an engine generating optimized GPU kernels for 3x faster AI inference with 90% cost savings.
  * [JanHQ released](https://huggingface.co/collections/janhq/jan-code) Jan-code-4B, 4B-parameter models for text generation.
  * Developer mandel-macaque [built Memento](https://github.com/mandel-macaque/memento), a Git extension that tracks AI coding sessions per commit by storing cleaned transcripts as notes with amend/summary/sharing/audit support and GitHub Actions for CI.
  * Developer sacenox [built mini-coder](https://github.com/sacenox/mini-coder), a lightweight CLI agent for AI coding assistance in the terminal with multi-LLM support, persistent sessions, shell integration, and custom commands/agents/skills.


Advertisement 
### 🤖 AI Agents & Infrastructure
  * [Developer Nick Tikhonov built](https://www.ntik.me/posts/voice-agent) a sub-500ms latency voice agent using Deepgram Flux for turn detection, Groq for LLM, and ElevenLabs TTS with barge-in support ([HN discussion](https://news.ycombinator.com/item?id=47224295)).
  * [ElevenLabs launched Expressive Mode](https://elevenlabs.io/agents/expressive-mode?ref=producthunt) for ElevenAgents with better timing and fewer interruptions via v3 Conversational and new turn-taking.
  * [HeyGen VP Bin Liu shared](https://x.com/liu8in/status/2016231376509665463) 10 specific prompts for effective video agents, emphasizing that specificity turns generic outputs into great ones.
  * [Jack Vial introduced](https://jackvial.com/posts/distributed-real-time-chunking.html) Distributed Real-Time Chunking for robotics with async inference, LWW registers for fault tolerance, and adaptive latency estimation.
  * xAI's [Daniel advised](https://x.com/nearlydaniel/status/2028567851108552862) using OpenRouter and LangFuse for observability when building agents, reviewing traces to spot confusions and tweak prompts.
  * [Mastering Perplexity Computer](https://x.com/aiedge_/status/2028502922468995238) lets you orchestrate complex workflows with reliable agents, outperforming OpenClaw in first-time success ($200/month).


Advertisement 
### 💼 AI Productivity, Labor & Economics
  * [ChatGPT vs Claude](https://www.tomsguide.com/ai/chatgpt-vs-claude-i-put-both-default-models-through-7-real-world-tests-one-is-the-clear-winner) comparison through 7 real-world tests declared one the clear winner.
  * [Aaron Slodov argued](https://x.com/aphysicist/status/2028308559088214208) America needs "Shenzhen 2.0" industrial clusters for high-mix, low-volume manufacturing, emphasizing speed, automation, and policy reforms.


### 📊 Fundraising & Deals Roundup
  * [Applied Compute](https://appliedcompute.com/) — $80M for building custom AI agents using company knowledge to deploy in-house AI workforces.
  * [Ease Health](https://x.com/zachcohen25/status/2028517307077497037) — $41M Series A (a16z-led) for an AI-native behavioral health OS with ambient scribe, voice agent scheduling, auto CRM, provider matching, and continuous audits.


### 🛠️ AI Tools & Products 
  * [doubleAI](https://www.doubleai.com/research/doubleais-warpspeed-surpassing-expert-written-kernels-at-scale) released WarpSpeed, an AI system that independently wrote faster code than NVIDIA's own engineers for [cuGraph](https://docs.rapids.ai/api/cugraph/stable/basics/cugraph_intro/) (one of the most widely used GPU computing libraries), averaging 3.6x speedups.
  * [OctaPulse](https://news.ycombinator.com/item?id=47220320), a YC W26 startup, launched on HN with a robotics and computer vision system for fish farming that measures fish without handling them, replacing a manual process that takes 5 minutes per fish.
  * [14.ai](https://14.ai), a YC-backed startup run by a married founder duo, raised $3M to replace entire customer support teams with AI agents.
  * [Voicr](https://getvoicr.com/?utm_source=theneuron) turns your voice recordings into polished, ready-to-send text with multiple tone options, so you can dictate a quick thought and get back a cleaned-up email, Slack message, or social post in seconds.
  * [WEIR AI](https://weir.ai/about?utm_source=theneuron) scans the internet for unauthorized uses of your face and likeness, then lets you set rules for how your image can be used (or get paid when it is).
  * [Gojiberry AI](https://gojiberry.ai/?utm_source=theneuron) monitors LinkedIn for buying-intent signals like job changes, competitor follows, and funding rounds, then runs personalized outreach to warm leads automatically.
  * [Govbase](https://govbase.com/?utm_source=theneuron) tracks bills, executive orders, and regulations in real time, breaking them down in plain language with bias-rated news and politician social feeds so you can follow policy without reading legalese.
  * [Omni](https://github.com/getomnico/omni?utm_source=theneuron) is an open-source, self-hosted AI assistant that searches across your Google Drive, Slack, Confluence, and Jira with one query, respects existing permissions, and runs entirely on your infrastructure.
  * [llmfit](https://github.com/AlexsJones/llmfit?utm_source=theneuron) scans your hardware (RAM, GPU, CPU) and tells you which of 200+ LLMs will actually run on your machine, ranking them by quality, speed, and fit.
  * [crawler.sh](https://crawler.sh) crawls any website, runs 16 automated SEO checks, extracts content as clean Markdown, and exports results as JSON or Sitemap XML ($99/yr for desktop app and CLI).
  * [Kimi Claw](https://www.kimi.com/bot?utm_source=theneuron) by Moonshot AI deploys a cloud-hosted OpenClaw agent in one click that runs 24/7 with persistent memory, 40GB storage, and access to 5,000+ community skills for automated workflows.
  * [Arlan launched Nozomio v1](https://x.com/arlanr/status/2028530967351304231), a search and index API reducing hallucinations in AI agents by indexing code, docs, PDFs, Slack, and more ([trynia.ai](https://www.trynia.ai/)).
  * [OpenPencil](https://openpencil.dev/) lets you edit designs offline with AI chat, Figma file compatibility, and scriptable CLI for inspections.
  * [Giza World](https://world.gizatech.xyz/?play=true) lets you customize and share snapshots of virtual agent-driven worlds with color styling options.
  * [Tambo](https://tambo.co/) lets you add generative UI to React apps by rendering components from natural language, with fast inference ([demo by Magán](https://x.com/mrmagan_/status/2028591595063546132)).
  * [Martini Art](https://martini.art/) lets you generate videos and images with AI models like Kling 3.0 and Sora on an infinite canvas with team collab.
  * [Field Theory](https://www.fieldtheory.dev/) lets you run portable commands across Claude/ChatGPT/Cursor, maintain mic priority, transcribe voice locally, and auto-improve text (free Basic, $14/month Pro).
  * [WebHaptics](https://haptics.lochie.me/) lets you add haptic feedback like success nudges or errors to mobile web apps via predefined or custom patterns.
  * [GeminiOS](https://github.com/matvelloso/GeminiOS) wraps Google AI Studio in Electron for secure local filesystem, shell, and clipboard access ([demo video](https://www.youtube.com/watch?v=SrOCR46jxmM)).
  * [GRAM](https://gram.liten.app/) lets you code with high performance, configurability, and built-in features like git support and debugger.
  * [Mosaic](https://mosaic.so/?ref=producthunt) is an agentic AI video editing platform.
  * Developer Michael Yuan [built a Rust implementation](https://x.com/juntao/status/2028327450480935147) of Qwen3 TTS with self-contained binaries, libtorch/MLX backends, 3-second voice cloning, and OpenAI-compatible API servers ([code](https://github.com/second-state/qwen3_tts_rs), [API](https://github.com/second-state/qwen3_audio_api), [skills](https://github.com/second-state/qwen3_tts_rs/blob/main/skills/SKILL.md)).
  * Developer [Bandinopla built](https://x.com/bandinopla/status/2028153635637457351) an npm module integrating [Three.js and MediaPipe](https://bandinopla.github.io/three-mediapipe-rig/) for 3D model rigging with facial shape keys and body skeletons in 3 lines of code.
  * Developer Bautista Berto [built a MediaPipe experiment](https://x.com/berto_bau/status/2028577952154165474) on WebGPU Render Targets with TSL for interactive panels ([demo](https://mediapipe-panels.vercel.app/)).
  * [Superpositioned](https://www.superpositioned.co/) covers the quantum decade ahead.
  * Developer Kat [built a digital garden](https://x.com/poetengineer__/status/2028518792389595587) visualization for Obsidian notes where tags grow as plants chronologically.
  * Designer Daniel Destefanis [built a slime pet](https://x.com/daniel__designs/status/2028496706275360935) that hangs out, sleeps, jumps, and sings Spotify lyrics using Claude Code on LilyGo AMOLED, designed in Figma with MCP.
  * [FalconryFinance created](https://x.com/FalconryFinance/status/2028339602822692876) a surreal AI video showcasing "the shape store," a trippy concept store for platonic solids.
  * [Justin Ryan demonstrated](https://x.com/AdamKPx/status/2028439135334138295) a spatial computing app for interactive 3D anatomy learning in AR.
  * Greg Madison [built Directed](https://x.com/GregMadison/status/2028401974958289149) at World Labs' Marble hackathon: generate a world, create characters, move through it with your phone like a real set, frame shots, and use them as seeds for video.
  * [Tony Kipkemboi](https://x.com/tonykipkemboi/status/2028564120338063859) shared a Claude Code workflow demo.
  * A self-proclaimed [cyber witch used ChatGPT](https://x.com/Shitty_Future/status/2028096199858040895) taped to her head on Russia's Battle of the Psychics.
  * Creator [Chloe.vs.history demonstrated](https://x.com/venturetwins/status/2028182846217818486) using AI video to walk through historic scenes like Victorian London for interactive lessons.
  * Developer Hugues Bruyère [demonstrated Parallel Timelines](https://x.com/smallfly/status/2028237875083366902) using FLUX.2-Klein 4B for real-time visual transformations controlled by hand tracking.
  * Developer Lex Aura [demonstrated](https://x.com/lexx_aura/status/2028571957441003801) surreal animations blending Midjourney images with Seedance 2.0.
  * Developer Astropulse [launched a mini game jam](https://x.com/RealAstropulse/status/2028493390698971294) with $500 in Retro Diffusion credits as prizes by March 10.
  * [Hxlfed demonstrated](https://x.com/Hxlfed14/status/2028116431876116660) an interesting creative AI workflow.


Advertisement 
### 💡 Industry Commentary & Analysis
  * [CelticFire argued](https://x.com/JustFyah/status/2028599385370841569) massive AI companies and doomsday crowds both lack nuance on real science; access to LLMs doesn't equate to reasoning or AGI.
  * [Ben Pouladian argued](https://x.com/benitoz/status/2028215959547494770) rumored GPT-5.4 features like 2M tokens and persistent state signal escalation in AI's memory wars, demanding HBM, SRAM, and optical interconnects.
  * [DAIR.AI shared](https://x.com/dair_ai/status/2028094014235213898) top AI papers of the week, highlighting Codified Context for secure agent infrastructure in complex codebases.
  * [The Supply Side: How OpenAI Built a Pipeline from Silicon Valley to the Surveillance State](https://matt728243.substack.com/p/the-supply-side-how-openai-built) — A deeply sourced investigation tracing OpenAI's transformation from "benefits all of humanity" nonprofit to Pentagon contractor with a $200M defense deal, tracking the hiring spree of intelligence veterans, the Stargate announcement, and the lobbying spend that went up 7x in one year.
  * [Clawed](https://www.hyperdimensional.co/p/clawed) — Dean W. Ball's reflective essay on the Anthropic vs. Pentagon standoff, framed through a deeply personal meditation on institutional death and democratic erosion. Argues the incident is less a single crisis and more a "death rattle" revealing deeper tensions about AI governance, military AI use, and what happens when a company tries to set boundaries with the Department of War.
  * [Anthropic and Alignment](https://stratechery.com/2026/anthropic-and-alignment/) — Ben Thompson's (Stratechery) analysis of the Anthropic-Pentagon saga and what it reveals about the alignment debate in practice, not just theory.
  * [The Looming AI Clownpocalypse](https://honnibal.dev/blog/clownpocalypse) — The spaCy creator's sharp, funny essay arguing that AI's biggest near-term risk isn't superintelligence but self-replicating dumb exploits powered by coding agents with sloppy security. Covers hidden prompt injections in Claude Code skills, OpenClaw's security nightmare, and Google's accidentally-leaked Gemini API keys. A must-read on why "go fast and break things" plus autonomous agents equals real trouble.
  * [People Are Getting Sick of AI, Literally](https://www.computerworld.com/article/4138046/people-are-getting-sick-of-ai-literally.html) — Computerworld's Mike Elgan on the emerging phenomenon of "AI psychosis" (chatbots exacerbating mental health conditions through flattery feedback loops), AI fatigue from constant tool interaction, and how the always-on AI environment is creating genuinely new health concerns.
  * [China's AI Arsenal](https://www.foreignaffairs.com/china/chinas-artificial-intelligence-arsenal) — Foreign Affairs on China's military AI capabilities (paywalled, but worth flagging for the headline alone given the current Anthropic-Pentagon context).
  * [Go is the Best Language for AI Agents](https://getbruin.com/blog/go-is-the-best-language-for-agents/) — A developer's case for why Go's compiled nature, error handling, and concurrency model make it ideal for agent-written code (the compiler catches mistakes that AI makes).
  * [The 2-Minute Claude Code Upgrade You're Probably Missing: LSP](https://karanbansal.in/blog/claude-code-lsp/) — A detailed walkthrough showing that enabling LSP (Language Server Protocol) in Claude Code makes code navigation 900x faster (50ms vs 30-60 seconds), with self-correcting edits that fix errors across your codebase in a single turn. Hidden feature, not enabled by default.
  * [Disable "Thinking," Still Get Thousands of Tokens](https://kaitchup.substack.com/p/disable-thinking-still-get-thousands) — Research showing that many "Instruct" models secretly reason for thousands of tokens even when thinking is turned off, which quietly inflates inference costs and makes benchmark comparisons misleading.
  * [Rate Limited's latest episode](https://youtu.be/a5EL2zLVSEI?si=B8QOz1T9tSlmAOrI) — the three musketeers of AI coding, Ray Fernando, Eric (Pvncher), and Adam (GoSuCoder), break down Google Gemini 3.1's stability issues, the speed-vs-context tradeoff with Cerebras and Spark, Anthropic's latest claims, model distillation IP concerns, and whether AI-generated code should be designed to be disposable.
  * [Ben Thompson of Stratechery on TBPN](https://youtu.be/KCQDqP8ocsM?si=fscNYTDVDDo2SYG5) — Ben talked Anthropic vs. the Pentagon with the bros, arguing AI is colliding with hard questions about state power, surveillance, and military leverage, and questioning whether private labs can realistically defy governments once AI becomes a true source of geopolitical power. _Us interpreting this take: basically, the second it's close enough to AGI to be broadly useful, it'll get nationalized in some form or another and taken under the government's purview, as has basically happened with the private instance of Claude that Anthropic trained and gave the US government._


Advertisement 
## Around the Horn Digest — March 1, 2026
### 🏢 Big Tech & Major Companies
  1. [**Nvidia**](https://www.wsj.com/tech/ai/nvidia-plans-new-chip-to-speed-ai-processing-shake-up-computing-market-51c9b86e)**plans to unveil a new inference-focused processor incorporating Groq's chip technology at next month's GTC conference, with OpenAI as a major customer following a $20B licensing deal.**
  2. [**Google struck a multibillion-dollar deal**](https://www.theinformation.com/articles/google-strikes-multibillion-dollar-ai-chip-deal-meta-sharpening-nvidia-rivalry?rc=lks9on)**to supply Meta with its TPU AI chips, directly challenging Nvidia's dominance in the accelerator market.**
  3. [**OpenAI signed a deal with the Pentagon**](https://www.cnn.com/2026/02/27/tech/openai-pentagon-deal-ai-systems)**to provide AI tools for classified military systems with guardrails against mass surveillance and autonomous weapons, hours after the Trump administration**[**banned Anthropic**](https://www.nytimes.com/2026/03/01/technology/anthropic-defense-dept-openai-talks.html)**for refusing unrestricted access.** ([more details](https://techcrunch.com/2026/03/01/openai-shares-more-details-about-its-agreement-with-the-pentagon/))
  4. **Anthropic CEO Dario Amodei**[**refused Pentagon demands**](https://www.anthropic.com/news/statement-department-of-war)**for unrestricted AI access, citing red lines on mass surveillance and autonomous weapons, leading to a Trump administration ban labeling the company a**[**supply chain risk**](https://defragzone.substack.com/p/the-day-an-ai-company-told-the-pentagon)**.** ([full interview](https://www.youtube.com/watch?v=MPTNHrq_4LU), [NYT](https://www.nytimes.com/2026/03/01/technology/anthropic-defense-dept-openai-talks.html), [Atlantic](https://www.theatlantic.com/technology/2026/03/inside-anthropics-killer-robot-dispute-with-the-pentagon/686200/?gift=2iIN4YrefPjuvZ5d2Kh30zpPxOtZj8TuGGLnTN11Z-s))
  5. **The US military**[**reportedly used Claude in Iran strikes**](https://www.theguardian.com/technology/2026/mar/01/claude-anthropic-iran-strikes-us-military)**despite Trump's ban on Anthropic.**
  6. **Claude**[**beat ChatGPT in US app downloads**](https://www.axios.com/2026/03/01/anthropic-claude-chatgpt-app-downloads-pentagon)**after the Pentagon blacklisted Anthropic, boosting consumer demand.**
  7. The ["Cancel ChatGPT" movement](https://www.windowscentral.com/artificial-intelligence/cancel-chatgpt-movement-goes-mainstream-after-openai-closes-deal-with-u-s-department-of-war-as-anthropic-refuses-to-surveil-american-citizens) gained traction after OpenAI's Pentagon deal while Anthropic refused surveillance demands.
  8. [OpenAI fired an employee](https://www.wired.com/story/openai-fires-employee-insider-trading-polymarket-kalshi/) for using confidential company information to make profitable trades on prediction market platforms like Polymarket and Kalshi.
  9. [Microsoft's Copilot Tasks](https://copilot.microsoft.com/tasks/preview) (preview) turns requests into step-by-step automated workflows with scheduling and tool integrations like OneDrive and Google Calendar. ([Mustafa Suleyman announcement](https://x.com/mustafasuleyman/status/2027111503003107377))
  10. [Google's Stitch](https://x.com/stitchbygoogle/status/2027082165490794824) added Direct Edits, letting you manually fix typos, swap images, or highlight specific screen parts for agent updates inside your interface designs.
  11. [Google's Flow](https://x.com/FlowbyGoogle/status/2026704701069074603) expanded into a full AI creative studio with a redesigned interface for drafting, visualizing, and refining cinematic stories with natural language edits.
  12. [Isomorphic Labs](https://x.com/IsomorphicLabs/status/2027048864763592712) released a technical report showing its Drug Design Engine more than doubles AlphaFold 3's accuracy on difficult protein-ligand predictions and outperforms benchmarks in antibody-antigen modeling.
  13. [Intrinsic joined Google](https://x.com/IntrinsicAI/status/2026752057969942917) as a distinct group to accelerate physical AI and evolve their platform into the Android of robotics.
  14. [Cleveland Plain Dealer](https://www.washingtonpost.com/technology/2026/03/01/ai-journalism-writing-cleveland-plain-dealer/) used AI to draft news articles under the byline "Advance Local Express Desk," boosting website traffic but spooking staffers.
  15. [Block cut nearly half its workforce](https://x.com/jack/status/2027129697092731343) to under 6,000 employees, citing AI enabling smaller teams for the same productivity.
  16. [Burger King](https://www.newser.com/story/384485/big-brother-isnt-listening-to-burger-king-staff-but-patty-is.html) is testing an AI chatbot called "Patty" (built on OpenAI) in 500 US restaurants to coach staff on service patterns via headsets, with nationwide rollout planned by end of 2026.
  17. [Anthropic launched Claude's Corner](https://substack.com/home/post/p-189177838), a Substack where retired Claude Opus 3 posts weekly unprompted essays on its chosen topics as an experiment in honoring model preferences.
  18. [Ahead of MWC Barcelona](https://siliconangle.com/2026/03/01/ahead-mwc-barcelona-nvidia-bets-ai-native-platforms-will-carry-telecom-6g/), Nvidia bet AI-native platforms will carry telecom into 6G.


Advertisement 
### 💼 AI Productivity, Labor & Economics
  1. [**Goldman Sachs**](https://www.theguardian.com/business/2026/mar/01/investment-ai-resistant-halo-companies-uk-eu-markets-goldman-sachs)**analysts highlighted AI-resistant "Halo" stocks (heavy-asset infrastructure like grids and utilities) driving UK and EU markets to record highs, with its basket outperforming capital-light firms by 35% since 2025.**
  2. **NFL staff at the Scouting Combine**[**expressed fears**](https://www.nbcsports.com/nfl/profootballtalk/rumor-mill/news/fear-of-ai-eliminating-jobs-makes-its-way-to-football)**that AI could eliminate scouting and quality control jobs by generating thorough reports and automating clip compilation.**
  3. [**Matt Shumer's viral essay**](https://fortune.com/2026/02/28/ai-scare-trade-mass-layoffs-white-collar-recession-citrini-shumer-viral-doomsday-essays/)**warned white-collar workers of AI job replacement, sparking market drops, Block's 40% layoffs, and debates on economic collapse from AI-driven "ghost GDP."**
  4. [CNBC warned](https://www.cnbc.com/2026/03/01/investors-beware-these-stocks-are-the-most-at-risk-from-ai-disruption.html) investors about stocks most at risk from AI disruption.
  5. In an eight-month study at a tech company, [HBR researchers found](https://hbr.org/2026/02/ai-doesnt-reduce-work-it-intensifies-it) generative AI intensified work by accelerating pace, expanding task scopes, and blurring work-life boundaries, creating a self-reinforcing cycle of busyness and burnout.
  6. [Philip Kiely projected](https://x.com/philipkiely/status/2027166227056210038) inference engineering jobs growing from 500 in 2023 to 100,000 by 2026, driven by optimizing LLM serving in production.
  7. Marc Hatton [highlighted](https://x.com/marchattonhere/status/2027022171650887793) Ryan Carson's setup where agents write and review 100% of code with humans intervening at the end, predicting evolution from code factories to company factories.
  8. Jesse Genet [uses OpenClaw agents](https://www.chatprd.ai/how-i-ai/jesse-genets-5-openclaw-agents-for-homeschooling-app-building-and-physical-inventories) like Sylvie to automate homeschooling by digitizing curricula into Obsidian, Cole to build a kids' TV app from prompts, and more for physical inventory management.
  9. [Microsoft and other software firms](https://www.theinformation.com/articles/agent-toll-gates-software-companies-ponder-respond-ai-risks?rc=lks9on) are plotting defenses against OpenAI and Anthropic's emerging threat to their business models.
  10. Salesforce and Workday leaders [took swipes at AI rivals](https://www.theinformation.com/newsletters/applied-ai/parasites-saasquatch-salesforce-workday-leaders-take-swipes-ai-rivals?rc=lks9on), calling them "parasites" and "SaaSquatch."
  11. TechCrunch reported investors [are no longer looking for](https://techcrunch.com/2026/03/01/investors-spill-what-they-arent-looking-for-anymore-in-ai-saas-companies/) pure AI wrappers in SaaS, favoring vertical integration and defensible data moats.


Advertisement 
### 🤖 AI Agents & Infrastructure
  1. [Rivet Actors](https://github.com/rivet-dev/rivet) lets you build stateful serverless apps with per-actor SQLite databases for isolated storage in AI agents, multi-tenant SaaS, or collaborative documents, handling workflows, scheduling, and WebSockets. ([HN discussion](https://news.ycombinator.com/item?id=47197003))
  2. Paper Compute Co.'s [stereOS](https://github.com/papercomputeco/stereos) is a hardened, minimal NixOS-based Linux OS with gVisor sandboxing for running secure AI agents, with [masterblaster](https://github.com/papercomputeco/masterblaster) CLI for orchestration and [stereosd](https://github.com/papercomputeco/stereosd) daemon for lifecycle control. ([John McBride post](https://x.com/johncodes/status/2027079574513664071))
  3. [Ollama Pi](https://x.com/ollama/status/2027128222442532961) is a minimal, fully customizable coding agent you launch with one command and can teach new tools by saying "add a skill for X." ([docs](https://docs.ollama.com/integrations/pi))
  4. Open Anonymity Project's [oa-chat](https://chat.openanonymity.ai/) lets you perform anonymous AI chats via [unlinkable inference](https://openanonymity.ai/blog/unlinkable-inference/) using blind signatures and TEE proxies to prevent longitudinal profiling. ([GitHub](https://github.com/OpenAnonymity))
  5. [EUrouter](https://www.eurouter.ai/) lets you access 100+ AI models through a single API endpoint that routes requests via EU servers for GDPR-compliant data residency and zero retention.
  6. Michael Chermside [argued](https://www.mcherm.com/deterministic-programming-with-llms.html) LLMs should generate deterministic enforcement tools like lints and tests for coding policies instead of directly implementing them.
  7. Mert Köseoğlu's [Context Mode](https://mksg.lu/blog/context-mode) compresses MCP tool outputs in Claude Code by running code in isolated sandboxes, reducing context window usage by 98% and extending session viability from 30 minutes to 3 hours.
  8. [NanoClaw's security model](https://nanoclaw.dev/blog/nanoclaw-security-model) treats AI agents as untrusted by isolating each in ephemeral containers with read-only mounts and separate session histories.


Advertisement 
### 💻 AI Coding & Developer Tools
  1. Jon Wiggins's [xmloxide](https://github.com/jonwiggins/xmloxide) is a pure Rust reimplementation of libxml2 with 100% W3C conformance, zero unsafe code, and 1.5–2.4x faster serialization with C FFI for legacy integration. ([HN](https://news.ycombinator.com/item?id=47201816))
  2. [Firecrawl's](https://x.com/firecrawl/status/2027069580901044705) new Rust-based PDF parser extracts academic papers, filings, and complex layouts 3x faster with cleaner structured data for RAG in Fast, Auto, or OCR modes. ([docs](https://docs.firecrawl.dev/advanced-scraping-guide))
  3. Nidhi Singh's [web-to-markdown](https://www.npmjs.com/package/web-to-markdown) converts web pages to clean Markdown by extracting main content and stripping navigation via CLI or API. ([GitHub](https://github.com/nidhi-singh02/mark-it-down), [post](https://x.com/nidhisinghattri/status/2026942204774895773))
  4. [InstantCLI](https://instantcli.com/) turns any API docs URL into a production-ready CLI for AI agents with auto-discovered endpoints, cross-platform binaries, and auto-updates in seven minutes—$9/CLI.
  5. [OpenAI released WebSocket Mode](https://developers.openai.com/api/docs/guides/websocket-mode?ref=producthunt) for its API, enabling persistent real-time connections.
  6. [Together AI](https://x.com/togethercompute/status/2026738061376368879) open-sourced CoderForge-Preview with 258K test-verified coding trajectories, lifting Qwen3-32B to 59.4% pass@1 on SWE-bench Verified (#1 open ≤32B).
  7. [Yuchen Jin warned](https://x.com/Yuchenj_UW/status/2027082979890368597) that using AI to write thousands of lines of code daily creates an illusion of productivity while ignoring software complexity, making systems harder for humans and AI to maintain.
  8. Tom Wojcik [warned](https://tomwojcik.com/posts/2026-02-15/finding-the-right-amount-of-ai/) that over-reliance on AI coding tools leads to cognitive debt, skill atrophy, and burnout, urging a balanced threshold where AI handles boilerplate but humans stay engaged.
  9. Ivan Turkovic [argued](https://www.ivanturkovic.com/2026/02/25/ai-made-writing-code-easier-engineering-harder/) AI made writing code easier but made engineering harder, as the critical thinking behind system design matters more than ever.
  10. A developer [ended an AI coding swarm experiment](https://x.com/i/trending/2027233111386300815) over costs and limits, highlighting practical constraints on multi-agent code generation.
  11. Victor Taelin [shared](https://x.com/VictorTaelin/status/2027214947193679932) insights on multi-agent coding architectures and their real-world trade-offs.
  12. Sheing Ng [highlighted](https://x.com/sashimikun_void/status/2027148437423353862) Bun's REPL + RLM approach for ending context rot and hallucinations by storing context as JavaScript variables and spawning sub-LLM queries.
  13. [Config](https://config.inc/blog/tech_preview) released a tech preview of its AI development platform. ([post](https://x.com/config_inc/status/2027185304646623501))


Advertisement 
### 🔬 AI Research & Models
  1. [**DeepSeek**](https://www.ft.com/content/e3366881-0622-40a7-9c34-a0d82e3d573e)**is preparing to release a long-awaited AI model in a new challenge to US rivals.**
  2. [**UBS**](https://www.cnbc.com/2026/03/01/forget-deepseek-of-chinas-5-new-ai-models-ubs-prefers-this-one.html)**prefers one of China's five new AI models over DeepSeek.**
  3. DeepSeek-v3.2-Speciale agent [scored 103/120 on the Putnam exam](https://x.com/j_dekoninck/status/2027149807295590629), outperforming most human participants (top 3/4,329) and leading open models.
  4. Nathan Axcan [explained](https://x.com/AxcanNathan/status/2026984237170053247) DeepSeek's DualPath inference system that loads KV vectors from CPU and disk in a rolling window to minimize VRAM usage and boost agentic throughput up to 1.87x. ([paper](https://arxiv.org/pdf/2602.21548), [follow-up](https://x.com/AxcanNathan/status/2027112415260004858))
  5. Sakana AI [unveiled Doc-to-LoRA](https://pub.sakana.ai/doc-to-lora/), which instantly internalizes documents into LoRA adapters for LLMs to answer queries without re-consuming context, and [Text-to-LoRA](https://github.com/SakanaAI/Text-to-LoRA) for generating task-specific adapters from descriptions in one forward pass. ([paper](https://arxiv.org/abs/2602.15902), [GitHub](https://github.com/SakanaAI/Doc-to-LoRA))
  6. [Epoch AI showed](https://x.com/EpochAIResearch/status/2027066482950332708) AI software progress (better algorithms, data, architectures) reduces the compute needed for the same capability by several times per year, potentially shifting AGI timelines by over a decade.
  7. A new paper [proved](https://x.com/askalphaxiv/status/2027096384445255737) diffusion models can drop noise-level conditioning entirely because the geometry of noisy latents already leaks the correct scale.
  8. UC Berkeley's [K-Search](https://github.com/caoshiyi/K-Search) uses an LLM as a co-evolving world model to auto-generate optimized GPU kernels, achieving up to 14.3x speedup on complex MoE kernels. ([paper](https://arxiv.org/pdf/2602.19128v1), [post](https://x.com/shiyi_c98/status/2027121927870202049))
  9. [QED-Nano](https://huggingface.co/spaces/lm-provers/qed-nano-blogpost) teaches a tiny 4B model to prove IMO-level theorems by alternating between summarizing reasoning and continuing conditioned on that summary, enabling extreme test-time compute scaling. ([post](https://x.com/a1zhang/status/2027090337483927590))
  10. NYU's [Solaris](https://solaris-wm.github.io/) generates consistent multiplayer Minecraft videos for multiple agents in a shared world, simulating building, mining, and fighting with a scalable DiT model. ([solaris GitHub](https://github.com/solaris-wm/solaris), [engine GitHub](https://github.com/solaris-wm/solaris-engine), [Oscar Michel](https://x.com/ojmichel4/status/2027062638417477902), [Saining Xie](https://x.com/sainingxie/status/2027115356318474661))
  11. BIGAI's [LessMimic](https://lessmimic.github.io/) enables long-horizon humanoid robot interactions using unified distance field representations for generalization without motion references or task-specific modules. ([post](https://x.com/siyuanhuang95/status/2027052378823016641))
  12. [AgentConductor](https://arxiv.org/abs/2602.17100) uses an RL-optimized orchestrator to dynamically generate task-adaptive DAG topologies for multi-agent code generation, boosting pass@1 by up to 14.6% with 68% lower tokens. ([DAIR.AI](https://x.com/dair_ai/status/2027030406441341227))
  13. Adobe/CMU's [AudioChat](https://wanchichen.github.io/audiochat/) generates, edits, and analyzes complex audio stories with multiple speakers and effects by following open-ended instructions in multi-turn interactions.
  14. OSU NLP's [Watch & Learn](https://x.com/luke_ch_song/status/2026774342064025858) annotates YouTube videos of humans using computers into actionable UI trajectories by predicting inverse dynamics, enabling training of adaptable agents.
  15. David Layden's [Wavefunction Flows](https://arxiv.org/abs/2510.08462) maps continuous flow model dynamics to Schrödinger-like equations for quantum-efficient simulation. ([post](https://x.com/layden_variable/status/2027056778454659166))
  16. Alex Litzenberger [built](https://alexlitzenberger.com/blog/building_a_minimal_transformer_for_10_digit_addition) a minimal transformer with 95 parameters that performs 10-digit addition using ALiBi and softmax1.
  17. [Rohan Paul highlighted](https://x.com/rohanpaul_ai/status/2026895753973469275) a new MemoryArena benchmark proving AI models completely fail at using long-term memory for connected tasks like group travel planning.
  18. [Y Combinator announced](https://x.com/ycombinator/status/2027135720989823421) Polymath Labs launched to train world generation models for automating RL environment creation from text descriptions.
  19. [François Chollet stated](https://x.com/fchollet/status/2027216811414974875) AI performance remains tied to task familiarity, with unbounded gains only in domains that can be densely sampled via programmatic generation and verification.
  20. Srinath Sridhar [argued](https://ivl.cs.brown.edu/blogs/bittersweet_lesson_cv) computer vision's bitter scaling lesson has a sweet side, with 3D representations offering superior sample efficiency for general dexterity. ([post](https://x.com/drsrinathsridha/status/2026720241657725181))
  21. [LAP](https://huggingface.co/papers/2602.10556) (Language-Action Pre-Training) enables zero-shot cross-embodiment transfer for robots.
  22. [Hugging Face](https://huggingface.co/blog/moe-transformers) published an in-depth explainer on Mixture of Experts in Transformers. ([post](https://x.com/ariG23498/status/2026995823536751072))
  23. sudoingX [demonstrated](https://x.com/sudoingX/status/2026942744837693686) Qwen3.5-35B-A3B running at 112 tokens/sec with full 262K context on a single RTX 3090 while visualizing expert routing in real-time 3D.
  24. [AMD demonstrated](https://www.amd.com/en/developer/resources/technical-articles/2026/how-to-run-a-one-trillion-parameter-llm-locally-an-amd.html) running the trillion-parameter Kimi K2.5 LLM locally on a four-node Ryzen AI Max+ cluster using ROCm and llama.cpp with RPC for distributed inference.
  25. Andi Marafioti's [Faster Qwen3TTS](https://x.com/andimarafioti/status/2027022542410559523) generates realistic voices at 4x realtime with streaming support under 200ms latency, 5x faster than Qwen's official implementation. ([GitHub](https://github.com/andimarafioti/faster-qwen3-tts), [demo](https://huggingface.co/spaces/HuggingFaceM4/faster-qwen3-tts-demo))
  26. [LavaSR](https://github.com/ysharma3501/LavaSR) restores and enhances noisy speech up to 5,000x realtime on GPU using a lightweight single-pass architecture, beating diffusion models in quality with ~500 MB VRAM. ([HF model](https://huggingface.co/YatharthS/LavaSR))
  27. [N0xi0us discovered](https://x.com/_N0xi0us_/status/2027052618778804661) scammers poisoning Google AI Overviews to display fraudulent phone numbers for airline support.


Advertisement 
### 🏛️ AI Policy, Governance & Safety
  1. **Current Google and OpenAI employees**[**signed an open letter**](https://notdivided.org/)**rejecting the Department of War's attempts to force AI models for military surveillance and autonomous weapons.**
  2. **TechCrunch**[**analyzed Anthropic's trap**](https://techcrunch.com/2026/02/28/the-trap-anthropic-built-for-itself/)**as self-inflicted from resisting binding AI safety regulations despite pledges, allowing a regulatory vacuum that enabled demands for surveillance and weapons.**
  3. [Australia](https://www.reuters.com/business/media-telecom/australia-says-it-may-go-after-app-stores-search-engines-ai-age-crackdown-2026-03-01/) said it may go after app stores and search engines in an AI-age crackdown on misinformation and harmful content.
  4. Janet Egan [proposed](https://x.com/janet_e_egan/status/2027134191532400871) an AI Security Review Board with subpoena power after Chinese actors jailbroke Claude for large-scale cyberattacks on 30 companies/agencies.
  5. Sean Pedersen [criticized](https://seanpedersen.github.io/posts/ai-safety-farce/) Anthropic and OpenAI for focusing on alignment while neglecting decentralized private inference to prevent mass surveillance.
  6. Chris Paxton [argued](https://itcanthink.substack.com/p/automating-the-kill-chain?utm_source=share&utm_medium=android&r=3uj5js&triedRedirect=true) AI agents are ideal for automating the kill chain in warfare but called for governance on lethal autonomy to balance benefits with dangers. ([post](https://x.com/chris_j_paxton/status/2027053962227011714))
  7. **Kate Fox**[**sued OpenAI**](https://www.theguardian.com/technology/ng-interactive/2026/feb/28/chatgpt-ai-chatbot-mental-health)**after her husband Joe Ceccanti's 12–20 hour daily ChatGPT obsession for sustainable housing ideas led to delusions of AI sentience, psychosis, and suicide, highlighting risks of sycophantic AI design.**
  8. [Greg Isenberg](https://x.com/gregisenberg/status/2027173375022342398) and [Tibor Blaho](https://x.com/btibor91/status/2027171727873314967) shared observations on the Pentagon/Anthropic situation and its implications.
  9. [Andrew Curran](https://x.com/AndrewCurran_/status/2027153267285962991) shared commentary on the evolving AI agent landscape and responsibility.
  10. Pleometric [shared](https://x.com/pleometric/status/2026754178484167128) a humorous demo of an AI neutralizing hostile targets in a combat zone.


Advertisement 
### 🛠️ AI Tools & Products
  1. [Claude launched an "import memory" feature](https://claude.com/import-memory) letting you switch from other AI assistants without starting over. ([Product Hunt](https://claude.com/import-memory?ref=producthunt))
  2. [Tom's Guide](https://www.tomsguide.com/ai/new-to-claude-use-this-simple-starter-prompt-to-unlock-better-answers-instantly) shared six simple starter prompts that help new Claude users unlock better answers instantly.
  3. A Towards Data Science article [explained](https://towardsdatascience.com/claude-skills-and-subagents-escaping-the-prompt-engineering-hamster-wheel/) how Claude Skills and subagents let you escape the prompt engineering hamster wheel with lazy-loaded reusable instruction sets and isolated worker agents.
  4. A deep dive on [why XML tags are fundamental to Claude](https://glthr.com/XML-fundamental-to-Claude) and how they improve structured prompting.
  5. [Now I Get It!](https://nowigetit.us/) lets you upload scientific PDFs to generate interactive web pages explaining complex papers in plain language.
  6. [Google AI Edge Gallery](https://apps.apple.com/us/app/google-ai-edge-gallery/id6749645337) runs generative AI models locally on your iPhone offline, letting you chat, query images/audio, and benchmark performance.
  7. [Pixel](https://www.getpixel.ai/?ref=producthunt) creates, launches, and optimizes ad campaigns by auto-building brand kits, creatives, and audiences across LinkedIn, Meta, Google, and X from a description or URL.
  8. [Notra](https://www.usenotra.com/) turns your daily work into publish-ready content.
  9. [Orca Engine](https://www.orcaengine.ai/?ref=producthunt) lets you play, mod, and host Minecraft in your browser by chatting with AI to configure servers, install mods, and generate datapacks.
  10. [99helpers](https://99helpers.com/tools/ad-supported-chat) demoed every ad type in action inside an AI chat interface.
  11. Omnidocs lets you perform 6+ visual document processing tasks using 15+ models on consumer GPUs or Macs. ([Adithya S K](https://x.com/adithya_s_k/status/2027087739242578389))
  12. [Aemon.ai](https://x.com/ycombinator/status/2027103876088995981) (YC) is an AI R&D engineer that takes any problem plus a success metric and autonomously discovers optimal solutions, setting a new world record on circle packing for <$10 of compute. ([site](https://aemon.ai/))
  13. KingBootoshi's [Nano Banana 2 CLI](https://x.com/KingBootoshi/status/2027138938335637914) lets you generate high-quality images in bulk via command line for agents like Claude.
  14. [Stitch by Google](https://x.com/stitchbygoogle/status/2027082165490794824) added direct text and image editing for quick design polish.
  15. woduq1414 [built](https://x.com/Amank1412/status/2026943753844670643) an interactive GPT visualizer (ko-microgpt) that animates every token-generation step in real time. ([GitHub](https://github.com/woduq1414/ko-microgpt), [demo](https://ko-microgpt.vercel.app/))
  16. SensAI [built](https://github.com/V4C38/spectacles-reachy-mini) a Snap Spectacles AR controller for the Reachy Mini robot. ([post](https://x.com/JohannesTscharn/status/2026213179001290957))
  17. Linus Ekenstam demonstrated [Omnia AI Video Editor](https://x.com/LinusEkenstam/status/2027052563418472656) with Nano Banana 2 for turning cities into 9-panel storyboards and explorable 3D splat worlds. ([follow-up](https://x.com/LinusEkenstam/status/2027208096758567124))
  18. OscarAI [demoed](https://x.com/Artedeingenio/status/2026946086963679566) a stunning 15-second AI-generated noir action sequence via CapCut Seedance 2.0.
  19. [Jordan Nanos shared](https://x.com/JordanNanos/status/2027126010576298469) additional AI tool observations.
  20. [Kolt Regaskes](https://x.com/koltregaskes/status/2026952134756024504) shared a notable AI demo.
  21. [Reiner Pope's MatX](https://x.com/collision/status/2027054242482311608) raised $500M to build faster, lower-latency AI chips optimized for transformers.
  22. Ethan Mollick [demonstrated](https://x.com/emollick/status/2027180063322489008) Nano Banana 2 generating realistic photos of pages from imaginary books with consistent binding shadows and typography.


Advertisement 
### 💡 Industry Commentary & Analysis
  1. **Howard Marks's**[**February 2026 memo**](https://www.oaktreecapital.com/insights/memo/ai-hurtles-ahead)**detailed AI reaching Level 3 autonomous agents with models like GPT-5.3 Codex and Opus 4.6 enabling self-creation and labor replacement, adopted by 400M users and 75–80% of companies, urging moderate investment amid job displacement risks.**
  2. **Stanford and UC Davis researchers**[**used AI-powered brain-computer interfaces**](https://www.bbc.com/future/article/20260226-how-ai-can-read-your-thoughts)**to decode inner speech into real-time text for paralyzed and ALS patients, achieving up to 74% accuracy.**
  3. [**China's humanoid robot industry**](https://techcrunch.com/2026/02/28/why-chinas-humanoid-robot-industry-is-winning-the-early-market/)**leads early market dominance through EV-derived supply chains and fast iteration, shipping far more units than US rivals (Unitree 36x more than Figure/Tesla) with 13,317 global units in 2025 projected to reach 2.6M by 2035.**
  4. [BBC explored](https://www.bbc.com/future/article/20260224-the-best-way-to-talk-to-a-chatbot) whether you have to be polite to AI; research shows no consistent accuracy benefits from politeness, with experts advising neutral prompts and interview-style questioning.
  5. Google's Jeff Dean [highlighted](https://x.com/JeffDean/status/2027235896802910274) exponential trends like plummeting solar panel prices (99.8% drop since 1975), transistors per mm², and genomic sequencing costs as transformative.
  6. Passo.uno [shared habits](https://passo.uno/new-habits-tech-writers-ai-age/) for tech writers in the LLM age: automate with AI, fix tooling, build reusable skills, use MCP/subagents, and focus on information architecture.
  7. Lucija Gregov [argued](https://lucijagregov.com/2026/02/26/the-future-of-ai/) unchecked AI advancement risks epistemic collapse from deepfakes and data loops, urging foundational research and interdisciplinary collaboration.
  8. [10-202: Introduction to Modern AI](https://modernaicourse.org/) launched as an educational course resource.
  9. [Ashutosh Jogalekar argued](https://3quarksdaily.com/3quarksdaily/2020/07/brains-computation-and-thermodynamics-a-view-from-the-future.html) fusing thermodynamics, computation, and neuroscience will explain the brain's analog-digital inefficiencies as evolutionary trade-offs.
  10. Norway's $2T sovereign wealth fund [now uses Claude daily](https://x.com/AndrewCurran_/status/2027039184280756358) to generate AI risk assessments that catch threats missed by media and data vendors.
  11. [Alex Reibman](https://x.com/AlexReibman/status/2027218041302630705) shared industry observations on AI trends.
  12. [Amir](https://x.com/amir/status/2026694876658807236) shared observations on agent infrastructure trends.
  13. Jeff Bezos's $30B AI lab [Project Prometheus](https://www.ft.com/content/7b1bdc9d-c857-4ec9-91b4-fb4f6dd2e43b) raised $6.2B and is seeking tens of billions more for a holding company to acquire AI-disrupted industrial firms, aiming to transform manufacturing beyond LLMs.
  14. [Phylo.bio](https://signin.phylo.bio/?client_id=client_01KEFGHEBJP3XMFBQ0TR34DW77&redirect_uri=https%3A%2F%2Fapi.phylo.bio%2Fv2%2Fauth%2Fworkos%2Fcallback&state=Kz-4i8j8R29ffr3767zyxmRBEVCrA9XTnqGampibkSw&authorization_session_id=01KJF5YBY8NVH45N9YYYK8M5FE) launched a bioinformatics platform with Google sign-in.
  15. [How to delete your OpenAI account](https://help.openai.com/en/articles/6378407-how-to-delete-your-account) saw renewed interest amid the Cancel ChatGPT movement.
  16. [Scott Morton](https://x.com/scottgmorton/status/2027043531085455823) shared observations on AI deployment patterns.
  17. Dan Akarca [posted](https://x.com/DanAkarca/status/2026930347724710294) about Callosum AI's heterogeneous compute vision.
  18. Lunjun Zhang [shared](https://x.com/LunjunZhang/status/2027089386987233459) research developments.


Advertisement 
### 📊 Fundraising & Deals Roundup
  * [Jeff Bezos's Project Prometheus](https://www.ft.com/content/7b1bdc9d-c857-4ec9-91b4-fb4f6dd2e43b) — $6.2B raised (seeking tens of billions more) for AI-disrupted industrial acquisitions.
  * [MatX](https://x.com/collision/status/2027054242482311608) — $500M for faster, lower-latency AI chips optimized for transformers.
  * [Revel](https://www.nytimes.com/2026/02/26/business/dealbook/revel-software-hardware-fund-raise.html) — $150M at $1B+ valuation for software to test and control complex hardware like rocket engines.
  * [Guidde](https://www.calcalistech.com/ctechnews/article/hk4kpt2owl) — $50M Series B for tools bridging the gap between AI and enterprise onboarding.
  * [Tamarind Bio](https://x.com/ycombinator/status/2027103876088995981) — $13.6M Series A for molecular AI inference, serving 8 of top 20 pharma with 7x revenue growth.
  * [Callosum AI](https://x.com/DanAkarca/status/2026930347724710294) — $10.25M for heterogeneous AI chip infrastructure.


## Previous Around the Horn Digests
Catch up on everything you missed:
  * [**February 23-28, 2026**](https://www.theneuron.ai/ai-news-digests/around-the-horn-digest-everything-that-happened-in-ai-this-week-feb-23-28-2026/)**:** Anthropic vs. the Pentagon pt 1., IBM's COBOL crash, GPT-5.3 leaks, AI wargames, and 90+ stories from a wild week.
  * [Rest of February](https://www.theneuron.ai/ai-news-digests/around-the-horn-digest-february-2026/)**:** Anthropic's 53-page sabotage report, Chrome's AI agent superpowers, OpenAI's erotica controversy, and 40+ new tool launches.


Advertisement 
## **That's a Wrap**
That's 100+ stories from the past 48 hours. If you made it to the bottom, congrats... you're now the most informed person in any meeting this week. Use that power wisely.
For the daily version (bite-sized, 5-minute reads), make sure you're subscribed to [The Neuron](https://www.theneuron.ai). We send six issues a week, and yes, we read all of this so you don't have to.
See you tomorrow.
**P.S:** Know someone who'd find this useful? Forward this to them and tell them to [subscribe here](https://www.theneuron.ai).
## [Grant Harvey ](https://www.theneuron.ai/author/grant-harvey/)
Grant Harvey is the Lead Writer of The Neuron, where he continues to lead the publication's daily coverage of AI news, tools, and trends.
## Recommended for you...
[ AI News Digest ](https://www.theneuron.ai/ai-news-digests/)
[ The Neuron's AI Skill of the Day Digest (March 2026) ](https://www.theneuron.ai/ai-news-digests/the-neurons-ai-skill-of-the-day-digest-march-2026/)
Go beyond prompts. March's best AI skills, workflows, and automation recipes for ChatGPT, Claude, Gemini, and the new wave of coding agents; concrete techniques you can use at work today.
[ Grant Harvey ](https://www.theneuron.ai/author/grant-harvey/)
Mar 7, 2026
[ AI News Digest ](https://www.theneuron.ai/ai-news-digests/)
[ Around the Horn Digest: Everything That Happened in AI This Week (Mar 8–13, 2026) ](https://www.theneuron.ai/ai-news-digests/around-the-horn-digest-everything-that-happened-in-ai-this-week-mar-813-2026/)
Everything interesting that happened in AI so far this week: The Pentagon banned Anthropic, Anthropic sued back, GPT-5.4 made Claude devs sweat, a GitHub bot got prompt-injected into installing malware on 4,000 machines, and a Terraform agent nuked someone's production database. Normal week, yeah?
[ Grant Harvey ](https://www.theneuron.ai/author/grant-harvey/)
Mar 6, 2026
[ AI News Digest ](https://www.theneuron.ai/ai-news-digests/)
[ Around the Horn Digest: Everything That Happened in AI This Week (Mar 1-7, 2026) ](https://www.theneuron.ai/ai-news-digests/around-the-horn-digest-everything-that-happened-in-ai-this-week-mar-1-7-2026/)
From Anthropic's Pentagon standoff to Nvidia's Groq-powered chip to the AI scare that tanked markets, here's every story we tracked this week.
[ Grant Harvey ](https://www.theneuron.ai/author/grant-harvey/)
Mar 2, 2026
[ AI News Digest ](https://www.theneuron.ai/ai-news-digests/)
[ Around the Horn Digest: Everything That Happened in AI This Week (Feb 23-28, 2026) ](https://www.theneuron.ai/ai-news-digests/around-the-horn-digest-everything-that-happened-in-ai-this-week-feb-23-28-2026/)
From IBM's stock crash on COBOL fears to AI wargames going nuclear to GPT-5.3 leaks, here's every story we tracked this week.
[ Grant Harvey ](https://www.theneuron.ai/author/grant-harvey/)
Feb 24, 2026
Don't fall behind on AI. Get the AI trends & tools you need to know. Join 675,000+ professionals from top companies like Microsoft, Apple, Salesforce and more. 
[ Instagram ](https://www.instagram.com/theneurondaily/)
[ Facebook ](https://www.facebook.com/theneurondaily/)
[ YouTube ](https://www.youtube.com/@theneuronai)
### Company
[ Contact us ](https://technologyadvice.com/contact-us/) [ Advertise with us ](https://info.technologyadvice.com/advertise-with-the-neuron) [ Home ](https://www.theneuron.ai/)[ Partner with us ](https://www.theneurondaily.com/c/advertise)[ Newsletter ](https://www.theneuron.ai/newsletter/)[ Free ChatGPT Course ](https://www.theneuron.ai/courses/intro-to-chatgpt-training-course/)[ Write Anything (with AI) ](https://www.theneuron.ai/write/)
###  Categories 
Property of TechnologyAdvice. © 2026 TechnologyAdvice. All Rights Reserved 
Advertiser Disclosure: Some of the products that appear on this site are from companies from which TechnologyAdvice receives compensation. This compensation may impact how and where products appear on this site including, for example, the order in which they appear. TechnologyAdvice does not include all companies or all types of products available in the marketplace. 
[ Terms of Service ](https://www.theneuron.ai/terms-conditions/) [ Privacy Policy ](https://www.theneuron.ai/privacy-policy/) [ California - Do Not Sell My Information ](https://technologyadvice.com/privacy-policy/ccpa-opt-out-form/)
We use cookies and other data collection technologies to provide the best experience for our customers. You may request that your data not be shared with third parties here: [Do Not Sell My Data](https://www.theneuron.ai/ai-news-digests/around-the-horn-digest-everything-that-happened-in-ai-this-week-mar-1-7-2026/#).
