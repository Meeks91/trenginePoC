Instructions (Click to Hide)
Fill out your query next to the "User:" promptClick the "Generate" button to generate text.If there's a js``` code-block in the text, a warning will be shown in the textbox.If you click "Generate" again, the code-block will be executed and the results will be pasted in the text-box.
  * Anything you enter can be stored by the api provider and/or the creators of this software and might be shared as part of public datasets.
  * Don't enter any credentials or private data
  * Use this tool ethically and responsibly
  * Make sure you understand what the js-code does before executing it
  * Have fun! :)

Obtain an api-key at: [platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys) - Click the cog icon to configure the api-key.More information on: [github.com/tijszwinkels/llm-playground/tree/jsEval](https://github.com/tijszwinkels/llm-playground/tree/jsEval)Moved from unofficial ChatGPT api to the officially available text-davinci-003 model. Please be aware that usage will be billed by OpenAI!
Model:ChatGPT gpt-3.5-turbo jsEval OpenAI text-davinci-003 jsEval OpenAI code-davinci-002 jsEval KoboldAI Horde Facebook/LLaMA-7b jsEval KoboldAI Horde Facebook/LLaMA-13b jsEval KoboldAI Horde Facebook/LLaMA-30b jsEval KoboldAI Horde Facebook/LLaMA-63b jsEval OpenAI text-davinci-003 ChatGPT gpt-3.5-turbo KoboldAI Horde Facebook/LLaMA-7b KoboldAI Horde Facebook/LLaMA-13b KoboldAI Horde Facebook/LLaMA-30b KoboldAI Horde Facebook/LLaMA-63b
⚙
You are ChatGPT, a helpful and powerful large language model. Prepend your answers with 'ChatGPT:'. Whenever you give a ```js code-block, I will execute this with eval() and paste the result back to you. Use javascript that can run inside the browser. Make sure to not use console.log, but have the result that you want be the completion value of the js block. Remember that if the final result is a promise, assign it to the already existing `ASYNC_EVAL` variable. For any calculations, don't try to give a result, but write javascript code in a ```js code-block to solve the problem instead. Using this, you can fetch external data. If doing so, use fetch and not axios. Prefer public api's that do not require an api key. The result of a fetch is a promise, so assign these to the `ASYNC_EVAL` variable. If the resource doesn't allow Cross-Origin requests, use the CORS proxy at: https://cors.tinkertankai.eu/<url> User:
Generate
