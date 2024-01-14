# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/6 21:45
@Author      : noahzhenli
@Email       : 
@Description :


<|im_start|>user\n你是谁？<|im_end|>\n<|im_start|>assistant

 temperature=0.6, top_p=0.8, repeat_penalty=1.1

./main -m /home/lizhen/test/model_file/01-yi/01-yi-6b-chat/ggml-model-q4_0.gguf -n 256 --repeat_penalty 1.0 --temp 0.6 --top-p 0.8 -ngl 20 --in-prefix '<|im_start|>' -r '<|im_end|>' -p '<|im_start|>user\n你是谁？<|im_end|>\n<|im_start|>assistant'
./server -m /home/lizhen/test/model_file/01-yi/01-yi-6b-chat/ggml-model-q4_0.gguf -n 50 -ngl 20


"""

import requests

def api(message_list):
    headers = {"Content-Type": "application/json"}
    data_json = {}
    data_json["message_list"] = message_list
    ip_url = "http://192.168.31.137:9020/model_chat"
    respone = requests.post(url=ip_url, json=data_json, headers=headers)
    return respone.json()



message_list = [
    {"role": "user", "content": "你是谁？"},
    {"role": "assistant", "content": "我是零一万物开发的智能助手，我叫 Yi，我是由零一万物的研究团队通过大量的文本数据进行训练的。我拥有广泛的知识和能力，我可以回答问题、提供信息，还能帮助用户解决问题。我被设计成具有语言理解和生成的能力，以便与人类用户互动。我的目标是尽可能准确和有用地为用户提供服务。"},
    {"role": "user", "content": "我上句话说了啥？"},
]

message_list = [
    {"role": "user", "content": "你是谁？"}
]

prompt = f'''请将下述英文学术文本翻译成高质量的中文版本。翻译应确保学术精确度和专业性，并遵循学术论文的写作规范与风格。预期的翻译将用于论文发表，因此请确保语言的正式性、准确性和连贯性。
英文学术文本"""
In this work, we introduce Vision-Language Generative Pre-trained Transformer (VL-GPT), a transformer model proficient at concurrently perceiving and generating visual and linguistic data. VL-GPT achieves a unified pre-training approach for both image and text modalities by employing a straightforward auto-regressive objective, thereby enabling the model to process image and text as seamlessly as a language model processes text. To accomplish this, we initially propose a novel image tokenizer-detokenizer framework for visual data, specifically designed to transform raw images into a sequence of continuous embeddings and reconstruct them accordingly. In combination with the existing text tokenizer and detokenizer, this framework allows for the encoding of interleaved image-text data into a multimodal sequence, which can subsequently be fed into the transformer model. Consequently, VL-GPT can perform largescale pre-training on multimodal corpora utilizing a unified auto-regressive objective ( i.e ., next-token prediction). Upon completion of pre-training, VL-GPT exhibits remarkable zero-shot and few-shot performance across a diverse range of vision and language understanding and generation tasks, including image captioning, visual question answering, text-to-image generation, and more. Additionally, the pre-trained model retrains in-context learning capabilities when provided with multimodal prompts. We further conduct instruction tuning on our VL-GPT, highlighting its exceptional potential for multimodal assistance. Driven by the remarkable success of large language models (LLMs) in the field of natural language processing (NLP) , there has been a surge of interest within multimodal community to develop large vision-language (VL) models. One of the promising approaches, exemplified by Flamingo , BLIP2 , LLAVA , have explored how to build large VL models based on powerful pre-trained LLMs. These studies typically adopted a similar architecture: a pre-trained image encoder and an LLM are connected via a trainable connection module, which aligns the image feature and text embeddings, thereby enabling language models to accept images and text as inputs and generate a text sequence. To expand the capabilities of generating image in a multimodal context, certain efforts, e.g ., Visual ChatGPT , attempt to connect LLMs with image generation tools in a cascaded pipeline by transferring text messages, which inevitably introduce instability and noise. Alternatively, another line of research achieves it by optimizing models in an end-to-end manner . By aligning the output space with the image diffusion models, VL models can not only perceive but also generate images and text.
"""
'''

message_list = [
    {"role": "user", "content": prompt}
]


while True:
    res = api(message_list)
    # print(res)
    print(res["response"])




# 关键词提取prompt
prompt = f'''基于下面的摘要，请识别并列出3个专业术语作为关键词，使得这些关键词能有效用于学术搜索引擎中，来查找相关领域的研究论文。关键词应该具体、相关，并且是此研究领域内通用的术语。

摘要："""
We present a scalable method to build a high quality instruction following language model by automatically labelling human-written text with corresponding instructions. Our approach, named instruction backtranslation , starts with a language model finetuned on a small amount of seed data, and a given web corpus. The seed model is used to construct training examples by generating instruction prompts for web documents ( self-augmentation ), and then selecting high quality examples from among these candidates ( self-curation ). This data is then used to finetune a stronger model. Finetuning LLaMa on two iterations of our approach yields a model that outperforms all other LLaMa-based models on the Alpaca leaderboard not relying on distillation data, demonstrating highly effective self-alignment.
"""

注意：关键词应捕捉摘要中最重要和最具代表性的概念，同时关键词不一定是摘要中的原文。

关键词生成：
1.
2.
3.
'''

prompt = f'''Based on the abstract provided, please extract 3 concisely formulated keywords, each no longer than three words, that encapsulate the core technologies or concepts presented. These keywords should not only be central to this specific research but also have the potential to be leveraged effectively in academic search engines to locate related studies. It is important that these terms are commonly recognized and utilized within this area of expertise.

Abstract: """
We present a scalable method to build a high quality instruction following language model by automatically labelling human-written text with corresponding instructions. Our approach, named instruction backtranslation , starts with a language model finetuned on a small amount of seed data, and a given web corpus. The seed model is used to construct training examples by generating instruction prompts for web documents ( self-augmentation ), and then selecting high quality examples from among these candidates ( self-curation ). This data is then used to finetune a stronger model. Finetuning LLaMa on two iterations of our approach yields a model that outperforms all other LLaMa-based models on the Alpaca leaderboard not relying on distillation data, demonstrating highly effective self-alignment.
"""

Please ensure that the selected keywords are technically robust and focus on representing the most critical aspects of the abstract. The chosen terms may be synthesized from the abstract content and should not necessarily be limited to exact phrases from the text.

Suggested Keywords:
1.
2.
3.
'''

message_list = [
    {"role": "user", "content": prompt}
]

res = api(message_list)
print(res["response"])
print(res["response"]["choices"][0]["text"])




# 翻译prompt
prompt = f'''请将下述英文学术文本翻译成高质量的中文版本。翻译应确保学术精确度和专业性，并遵循学术论文的写作规范与风格。预期的翻译将用于论文发表，因此请确保语言的正式性、准确性和连贯性。
英文学术文本"""
In this work, we introduce Vision-Language Generative Pre-trained Transformer (VL-GPT), a transformer model proficient at concurrently perceiving and generating visual and linguistic data. VL-GPT achieves a unified pre-training approach for both image and text modalities by employing a straightforward auto-regressive objective, thereby enabling the model to process image and text as seamlessly as a language model processes text. To accomplish this, we initially propose a novel image tokenizer-detokenizer framework for visual data, specifically designed to transform raw images into a sequence of continuous embeddings and reconstruct them accordingly. In combination with the existing text tokenizer and detokenizer, this framework allows for the encoding of interleaved image-text data into a multimodal sequence, which can subsequently be fed into the transformer model. Consequently, VL-GPT can perform largescale pre-training on multimodal corpora utilizing a unified auto-regressive objective ( i.e ., next-token prediction). Upon completion of pre-training, VL-GPT exhibits remarkable zero-shot and few-shot performance across a diverse range of vision and language understanding and generation tasks, including image captioning, visual question answering, text-to-image generation, and more. Additionally, the pre-trained model retrains in-context learning capabilities when provided with multimodal prompts. We further conduct instruction tuning on our VL-GPT, highlighting its exceptional potential for multimodal assistance.
"""
'''

message_list = [
    {"role": "user", "content": prompt}
]

res = api(message_list)
print(res["response"])
print(res["response"]["choices"][0]["text"])









# llama cpp server test
# 20层

import requests

prompt = f'''Based on the provided abstract, identify and select 3 professional keywords. These keywords should meet the following criteria:

1. Specificity: They should precisely reflect the core themes and methods of the research.
2. Relevance: They must be closely related to the content of the abstract and suitable for referring to the key aspects of the study.
3. Professionalism: They should be terms that are widely recognized and utilized within the research field.
4. They will be used to retrieve research papers in similar fields through academic search engines. Ensure that the chosen keywords can effectively guide researchers or scholars in finding research works akin to this abstract.
5. Do not directly select vocabulary from the abstract unless you believe they are irreplaceable and directly indicate the specific fields of research. The choice of keywords should demonstrate the ability to comprehend and analyze the contents of the abstract.

Abstract: """
We present a scalable method to build a high quality instruction following language model by automatically labelling human-written text with corresponding instructions. Our approach, named instruction backtranslation , starts with a language model finetuned on a small amount of seed data, and a given web corpus. The seed model is used to construct training examples by generating instruction prompts for web documents ( self-augmentation ), and then selecting high quality examples from among these candidates ( self-curation ). This data is then used to finetune a stronger model. Finetuning LLaMa on two iterations of our approach yields a model that outperforms all other LLaMa-based models on the Alpaca leaderboard not relying on distillation data, demonstrating highly effective self-alignment.
"""

Please list your selected keywords below:
1.
2.
3.
'''

headers = {"Content-Type": "application/json"}
data_json = {
    "prompt": f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant",
    "temperature": 0.6,
    "top_p": 0.8,
    "repeat_penalty": 1.1,
    "stop": ["<|im_end|>"]
}
ip_url = "http://localhost:8080/completion"
respone = requests.post(url=ip_url, json=data_json, headers=headers)
for key, value in respone.json().items():
    print(key, ": ", value)
print(respone.json())
print(respone.text)