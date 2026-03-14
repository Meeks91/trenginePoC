# LLM  
The LLM pipeline runs prompts through a large language model (LLM). This pipeline autodetects the LLM framework based on the model path.
## Example
The following shows a simple example using this pipeline.
```
fromtxtaiimport LLM

# Create LLM pipeline
llm = LLM()

# Run prompt
llm(
"""
  Answer the following question using the provided context.

  Question:
  What are the applications of txtai?

  Context:
  txtai is an open-source platform for semantic search and
  workflows powered by language models.
  """
)

# Prompts with chat templating can be directly passed
# The template format varies by model
llm(
"""
  <|im_start|>system
  You are a friendly assistant.<|im_end|>
  <|im_start|>user
  Answer the following question...<|im_end|>
  <|im_start|>assistant
  """
)

# Chat messages automatically handle templating
llm([
  {"role": "system", "content": "You are a friendly assistant."},
  {"role": "user", "content": "Answer the following question..."}
])

# When there is no system prompt passed to instruction tuned models
# the default role is inferred `defaultrole="auto"`
llm("Answer the following question...")

# To always generate chat messages for string inputs
llm("Answer the following question...", defaultrole="user")

# To never generate chat messages for string inputs
llm("Answer the following question...", defaultrole="prompt")

```

The LLM pipeline automatically detects the underlying LLM framework. This can also be manually set. The following methods are supported.
  * [Hugging Face Transformers](https://github.com/huggingface/transformers)
  * [LLM APIs via LiteLLM](https://github.com/BerriAI/litellm)


`llama.cpp` models support both local and remote GGUF paths on the HF Hub. See the [LiteLLM documentation](https://litellm.vercel.app/docs/providers) for the options available with LiteLLM models. See the [OpenCode documentation](https://opencode.ai/docs/server/) for more on how to integrate the LLM pipeline with a running OpenCode instance.
```
fromtxtaiimport LLM

# Transformers
llm = LLM("openai/gpt-oss-20b")
llm = LLM("openai/gpt-oss-20b", method="transformers")

# llama.cpp
llm = LLM("unsloth/gpt-oss-20b-GGUF/gpt-oss-20b-Q4_K_M.gguf")
llm = LLM("unsloth/gpt-oss-20b-GGUF/gpt-oss-20b-Q4_K_M.gguf",
           method="llama.cpp")

# LiteLLM
llm = LLM("ollama/gpt-oss")
llm = LLM("ollama/gpt-oss", method="litellm")

# Custom Ollama endpoint
llm = LLM("ollama/gpt-oss", api_base="http://localhost:11434")

# Custom OpenAI-compatible endpoint
llm = LLM("openai/gpt-oss", api_base="http://localhost:4000")

# LLM APIs - must also set API key via environment variable
llm = LLM("gpt-5.2")
llm = LLM("claude-opus-4-5-20251101")
llm = LLM("gemini/gemini-3-pro-preview")

# Local OpenCode server started via `opencode serve`
llm = LLM("opencode")
llm = LLM("opencode/big-pickle", url="http://localhost:4000")

```

Models can be externally loaded and passed to pipelines. This is useful for models that are not yet supported by Transformers and/or need special initialization.
```
importtorch

fromtransformersimport AutoModelForCausalLM, AutoTokenizer
fromtxtaiimport LLM

# Load Qwen3 0.6B
path = "Qwen/Qwen3-0.6B"
model = AutoModelForCausalLM.from_pretrained(
  path,
  dtype=torch.bfloat16,
)
tokenizer = AutoTokenizer.from_pretrained(path)

llm = LLM((model, tokenizer))

```

See the links below for more detailed examples.
Notebook | Description  
---|---  
[Prompt-driven search with LLMs](https://github.com/neuml/txtai/blob/master/examples/42_Prompt_driven_search_with_LLMs.ipynb) | Embeddings-guided and Prompt-driven search with Large Language Models (LLMs)  
[Prompt templates and task chains](https://github.com/neuml/txtai/blob/master/examples/44_Prompt_templates_and_task_chains.ipynb) | Build model prompts and connect tasks together with workflows  
[Build RAG pipelines with txtai](https://github.com/neuml/txtai/blob/master/examples/52_Build_RAG_pipelines_with_txtai.ipynb) [▶️](https://www.youtube.com/watch?v=t_OeAc8NVfQ) | Guide on retrieval augmented generation including how to create citations  
[Integrate LLM frameworks](https://github.com/neuml/txtai/blob/master/examples/53_Integrate_LLM_Frameworks.ipynb) | Integrate llama.cpp, LiteLLM and custom generation frameworks  
[Generate knowledge with Semantic Graphs and RAG](https://github.com/neuml/txtai/blob/master/examples/55_Generate_knowledge_with_Semantic_Graphs_and_RAG.ipynb) | Knowledge exploration and discovery with Semantic Graphs and RAG  
[Build knowledge graphs with LLMs](https://github.com/neuml/txtai/blob/master/examples/57_Build_knowledge_graphs_with_LLM_driven_entity_extraction.ipynb) | Build knowledge graphs with LLM-driven entity extraction  
[Advanced RAG with graph path traversal](https://github.com/neuml/txtai/blob/master/examples/58_Advanced_RAG_with_graph_path_traversal.ipynb) | Graph path traversal to collect complex sets of data for advanced RAG  
[Advanced RAG with guided generation](https://github.com/neuml/txtai/blob/master/examples/60_Advanced_RAG_with_guided_generation.ipynb) | Retrieval Augmented and Guided Generation  
[RAG with llama.cpp and external API services](https://github.com/neuml/txtai/blob/master/examples/62_RAG_with_llama_cpp_and_external_API_services.ipynb) | RAG with additional vector and LLM frameworks  
[How RAG with txtai works](https://github.com/neuml/txtai/blob/master/examples/63_How_RAG_with_txtai_works.ipynb) | Create RAG processes, API services and Docker instances  
Full cycle speech to speech workflow with RAG  
[Analyzing Hugging Face Posts with Graphs and Agents](https://github.com/neuml/txtai/blob/master/examples/68_Analyzing_Hugging_Face_Posts_with_Graphs_and_Agents.ipynb) | Explore a rich dataset with Graph Analysis and Agents  
[Granting autonomy to agents](https://github.com/neuml/txtai/blob/master/examples/69_Granting_autonomy_to_agents.ipynb) | Agents that iteratively solve problems as they see fit  
[Getting started with LLM APIs](https://github.com/neuml/txtai/blob/master/examples/70_Getting_started_with_LLM_APIs.ipynb) | Generate embeddings and run LLMs with OpenAI, Claude, Gemini, Bedrock and more  
[Analyzing LinkedIn Company Posts with Graphs and Agents](https://github.com/neuml/txtai/blob/master/examples/71_Analyzing_LinkedIn_Company_Posts_with_Graphs_and_Agents.ipynb) | Exploring how to improve social media engagement with AI  
[Parsing the stars with txtai](https://github.com/neuml/txtai/blob/master/examples/72_Parsing_the_stars_with_txtai.ipynb) | Explore an astronomical knowledge graph of known stars, planets, galaxies  
[Chunking your data for RAG](https://github.com/neuml/txtai/blob/master/examples/73_Chunking_your_data_for_RAG.ipynb) | Extract, chunk and index content for effective retrieval  
[Medical RAG Research with txtai](https://github.com/neuml/txtai/blob/master/examples/75_Medical_RAG_Research_with_txtai.ipynb) | Analyze PubMed article metadata with RAG  
[GraphRAG with Wikipedia and GPT OSS](https://github.com/neuml/txtai/blob/master/examples/77_GraphRAG_with_Wikipedia_and_GPT_OSS.ipynb) | Deep graph search powered RAG  
[RAG is more than Vector Search](https://github.com/neuml/txtai/blob/master/examples/79_RAG_is_more_than_Vector_Search.ipynb) | Context retrieval via Web, SQL and other sources  
[OpenCode as a txtai LLM](https://github.com/neuml/txtai/blob/master/examples/81_OpenCode_as_a_txtai_LLM.ipynb) | Integrate OpenCode with the txtai ecosystem  
[Agentic College Search](https://github.com/neuml/txtai/blob/master/examples/82_Agentic_College_Search.ipynb) | Identify a list of strong engineering colleges  
Integrate skill.md files with your agent  
## Configuration-driven example
Pipelines are run with Python or configuration. Pipelines can be instantiated in [configuration](https://neuml.github.io/txtai/api/configuration/#pipeline) using the lower case name of the pipeline. Configuration-driven pipelines are run with [workflows](https://neuml.github.io/txtai/workflow/#configuration-driven-example) or the [API](https://neuml.github.io/txtai/api#local-instance).
### config.yml
```
# Create pipeline using lower case class name
llm:

# Run pipeline with workflow
workflow:
llm:
tasks:
-action:llm

```

Similar to the Python example above, the underlying [Hugging Face pipeline parameters](https://huggingface.co/docs/transformers/main/main_classes/pipelines#transformers.pipeline.model) and [model parameters](https://huggingface.co/docs/transformers/model_doc/auto#transformers.AutoModel.from_pretrained) can be set in pipeline configuration.
```
llm:
path:Qwen/Qwen3-0.6B
dtype:torch.bfloat16

```

### Run with Workflows
```
fromtxtaiimport Application

# Create and run pipeline with workflow
app = Application("config.yml")
list(app.workflow("llm", [
"""
  Answer the following question using the provided context.

  Question:
  What are the applications of txtai? 

  Context:
  txtai is an open-source platform for semantic search and
  workflows powered by language models.
  """
]))

```

### Run with API
```
CONFIG=config.ymluvicorn"txtai.api:app"

curl\
-XPOST"http://localhost:8000/workflow"\
-H"Content-Type: application/json"\
-d'{"name":"llm", "elements": ["Answer the following question..."]}'

```

## Methods
Python documentation for the pipeline.
###  `__init__(path=None, method=None, **kwargs)`
Creates a new LLM.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`path` |  model path |  `None`  
`method` |  llm model framework, infers from path if not provided |  `None`  
`kwargs` |  model keyword arguments  
Source code in `txtai/pipeline/llm/llm.py`
```
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
```
| ```
def__init__(self, path=None, method=None, **kwargs):
"""
    Creates a new LLM.

    Args:
        path: model path
        method: llm model framework, infers from path if not provided
        kwargs: model keyword arguments
    """

    # Default LLM if not provided
    path = path if path else "ibm-granite/granite-4.0-350m"

    # Generation instance
    self.generator = GenerationFactory.create(path, method, **kwargs)

```
  
---|---  
###  `__call__(text, maxlength=512, stream=False, stop=None, defaultrole='auto', stripthink=None, **kwargs)`
Generates content. Supports the following input formats:
  * String or list of strings (instruction-tuned models must follow chat templates)
  * List of dictionaries with `role` and `content` key-values or lists of lists


Parameters:
Name | Type | Description | Default  
---|---|---|---  
`text` |  text|list |  _required_  
`maxlength` |  maximum sequence length |  `512`  
`stream` |  stream response if True, defaults to False |  `False`  
`stop` |  list of stop strings, defaults to None |  `None`  
`defaultrole` |  default role to apply to text inputs (`auto` to infer (default), `user` for user chat messages or `prompt` for raw prompts) |  `'auto'`  
`stripthink` |  strip thinking tags, defaults to False if stream is enabled, True otherwise |  `None`  
`kwargs` |  additional generation keyword arguments  
Returns:
Type | Description  
---|---  
generated content  
Source code in `txtai/pipeline/llm/llm.py`
```
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
```
| ```
def__call__(self, text, maxlength=512, stream=False, stop=None, defaultrole="auto", stripthink=None, **kwargs):
"""
    Generates content. Supports the following input formats:

      - String or list of strings (instruction-tuned models must follow chat templates)
      - List of dictionaries with `role` and `content` key-values or lists of lists

    Args:
        text: text|list
        maxlength: maximum sequence length
        stream: stream response if True, defaults to False
        stop: list of stop strings, defaults to None
        defaultrole: default role to apply to text inputs (`auto` to infer (default), `user` for user chat messages or `prompt` for raw prompts)
        stripthink: strip thinking tags, defaults to False if stream is enabled, True otherwise
        kwargs: additional generation keyword arguments

    Returns:
        generated content
    """

    # Debug logging
    logger.debug(text)

    # Default stripthink to False when streaming, True otherwise
    stripthink = not stream if stripthink is None else stripthink

    # Run LLM generation
    return self.generator(text, maxlength, stream, stop, defaultrole, stripthink, **kwargs)

```
  
---|---
