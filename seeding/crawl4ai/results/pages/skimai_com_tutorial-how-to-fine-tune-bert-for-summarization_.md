# Tutorial: How to Fine-Tune BERT for Extractive Summarization
December 28, 2020 | 4 minutes read


Table of Contents
Table of Contents
```
    Originally published by Skim AI's Machine Learning Researcher, Chris Tran
```

Summarization has long been a challenge in Natural Language Processing. To generate a short version of a document while retaining its most important information, we need a model capable of accurately extracting the key points while avoiding repetitive information. Fortunately, recent works in NLP such as Transformer models and language model pretraining have advanced the state-of-the-art in summarization.
In this article, we will explore BERTSUM, a simple variant of BERT, for extractive summarization from [Text Summarization with Pretrained Encoders](https://arxiv.org/abs/1908.08345) (Liu et al., 2019). Then, in an effort to make extractive summarization even faster and smaller for low-resource devices, we will fine-tune DistilBERT ([Sanh et al., 2019](https://arxiv.org/abs/1910.01108)) and MobileBERT ([Sun et al., 2019](https://arxiv.org/abs/2004.02984)), two recent lite versions of BERT, and discuss our findings.
There are two types of summarization: _abstractive_ and _extractive summarization_. Abstractive summarization basically means rewriting key points while extractive summarization generates summary by copying directly the most important spans/sentences from a document.
Abstractive summarization is more challenging for humans, and also more computationally expensive for machines. However, which summaration is better depends on the purpose of the end user. If you were writing an essay, abstractive summaration might be a better choice. On the other hand, if you were doing some research and needed to get a quick summary of what you were reading, extractive summarization would be more helpful for the task.
In this section we will explore the architecture of our extractive summarization model. The BERT summarizer has 2 parts: a BERT encoder and a summarization classifier.
_The overview architecture of BERTSUM_
Our BERT encoder is the pretrained BERT-base encoder from the masked language modeling task ([Devlin et at., 2018](https://github.com/google-research/bert)). The task of extractive summarization is a binary classification problem at the sentence level. We want to assign each sentence a label $y_i in {0, 1}$ indicating whether the sentence should be included in the final summary. Therefore, we need to add a token `[CLS]` before each sentence. After we run a forward pass through the encoder, the last hidden layer of these `[CLS]` tokens will be used as the representions for our sentences.
After getting the vector representation of each sentence, we can use a simple feed forward layer as our classifier to return a score for each sentence. In the paper, the author experimented with a simple linear classifier, a Recurrent Neural Network and a small Transformer model with 3 layers. The Transformer classifier yields the best results, showing that inter-sentence interactions through self-attention mechanism is important in selecting the most important sentences.
So in the encoder, we learn the interactions among tokens in our document while in the summarization classifier, we learn the interactions among sentences.
Transformer models achieve state-of-the-art performance in most NLP bechmarks; however, training and making predictions from them are computationally expensive. In an effort to make summarization lighter and faster to be deployed on low-resource devices, I have modified the [source codes](https://github.com/nlpyang/PreSumm) provided by the authors of BERTSUM to replace the BERT encoder with DistilBERT and MobileBERT. The summary layers are kept unchaged.
Here are training losses of these 3 variants: [TensorBoard](https://tensorboard.dev/experiment/Ly7CRURRSOuPBlZADaqBlQ/#scalars)
Despite being 40% smaller than BERT-base, DistilBERT has the same training losses as BERT-base while MobileBERT performs slightly worse. The table below shows their performance on CNN/DailyMail dataset, size and running time of a forward pass:
Models | ROUGE-1 | ROUGE-2 | ROUGE-L | Inference Time* | Size | Params  
---|---|---|---|---|---|---  
bert-base | 43.23 | 20.24 | 39.63 | 1.65 s | 475 MB | 120.5 M  
distilbert | 42.84 | 20.04 | 39.31 | 925 ms | 310 MB | 77.4 M  
mobilebert | 40.59 | 17.98 | 36.99 | 609 ms | 128 MB | 30.8 M  
*_Average running time of a forward pass on a single GPU on a standard Google Colab notebook_
Being 45% faster, DistilBERT have almost the same performance as BERT-base. MobileBERT retains 94% performance of BERT-base, while being 4x smaller than BERT-base and 2.5x smaller than DistilBERT. In the MobileBERT paper, it’s shown that MobileBERT significantly outperforms DistilBERT on SQuAD v1.1. However, it’s not the case for extractive summarization. But this is still an impressive result for MobileBERT with a disk size of only 128 MB.
All pretrained checkpoints, training details and setup instruction can be found in [this GitHub repository](https://github.com/chriskhanhtran/bert-extractive-summarization/). In addition, I have deployed a demo of BERTSUM with the MobileBERT encoder.
**Web app:** <https://extractive-summarization.herokuapp.com/>
**Code:**
```
import torch
from models.model_builder import ExtSummarizer
from ext_sum import summarize
# Load model
model_type = 'mobilebert' #@param ['bertbase', 'distilbert', 'mobilebert']
checkpoint = torch.load(f'checkpoints/{model_type}_ext.pt', map_location='cpu')
model = ExtSummarizer(checkpoint=checkpoint, bert_type=model_type, device='cpu')
# Run summarization
input_fp = 'raw_data/input.txt'
result_fp = 'results/summary.txt'
summary = summarize(input_fp, result_fp, model, max_length=3)
print(summary)

```

**Summary sample**
Original: <https://www.cnn.com/2020/05/22/business/hertz-bankruptcy/index.html>
```
By declaring bankruptcy, Hertz says it intends to stay in business while restructuring its debts and emerging a
financially healthier company. The company has been renting cars since 1918, when it set up shop with a dozen
Ford Model Ts, and has survived the Great Depression, the virtual halt of US auto production during World War II
and numerous oil price shocks. "The impact of Covid-19 on travel demand was sudden and dramatic, causing an
abrupt decline in the company's revenue and future bookings," said the company's statement.

```

In this article, we have explored BERTSUM, a simple variant of BERT, for extractive summarization from the paper **Text Summarization with Pretrained Encoders** (Liu et al., 2019). Then, in an effort to make extractive summarization even faster and smaller for low-resource devices, we fine-tuned DistilBERT (Sanh et al., 2019) and MobileBERT (Sun et al., 2019) on CNN/DailyMail datasets.
DistilBERT retains BERT-base’s performance in extractive summarization while being 45% smaller. MobileBERT is 4x smaller and 2.7x faster than BERT-base yet retains 94% of its performance.
Finally, we deployed a web app demo of MobileBERT for extractive summarization at <https://extractive-summarization.herokuapp.com/>.
  * [1] [PreSumm: Text Summarization with Pretrained Encoders](https://github.com/nlpyang/PreSumm)
  * [2] [DistilBERT: Smaller, faster, cheaper, lighter version of BERT](https://huggingface.co/transformers/model_doc/distilbert.html)
  * [3] [MobileBERT: a Compact Task-Agnostic BERT for Resource-Limited Devices](https://github.com/google-research/google-research/tree/master/mobilebert)
  * [4] [MobileBert_PyTorch](https://github.com/lonePatient/MobileBert_PyTorch)


### Let’s Discuss your AI Solution
### Related Posts
  * February 19, 2025 | 9 minutes read
[ 10 Best Prompting Techniques for LLMs in 2025 ](https://skimai.com/10-best-prompting-techniques-for-llms-in-2025/)
The art of crafting effective large language model (LLM) prompts has become a crucial skill for AI practitioners. Well-designed prompts can significantly enhance an LLM's performance, enabling more accurate, relevant, and creative outputs. This blog post explores ten of
[Prompt Engineering](https://skimai.com/category/prompt-engineering/)
  * February 19, 2025 | 6 minutes read
[ Top Ten AI YouTubers You Need to Follow in 2025 ](https://skimai.com/top-ten-ai-youtubers-you-need-to-follow-in-2025/)
The field of artificial intelligence demands continuous learning, and YouTube has emerged as one of the most powerful platforms for AI education and professional development. While research papers and traditional learning paths remain crucial, leading AI YouTubers are breaking
[Generative AI](https://skimai.com/category/generative-ai/)
  * February 19, 2025 | 5 minutes read
[ Top Ten AI Tools for YouTubers in 2025 ](https://skimai.com/top-ten-ai-tools-for-youtubers-in-2025/)
In the dynamic world of YouTube content creation, leveraging AI tools can significantly enhance your video creation process, streamline workflows, and boost your channel's growth. From video editing software to keyword research tools, these AI-powered solutions assist YouTube creators
[TV, Film & Content](https://skimai.com/category/film-tv/)


## Ready To Supercharge Your Business
