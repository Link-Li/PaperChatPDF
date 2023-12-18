# -*- coding: utf-8 -*-
"""
@Time        : 2023/12/17 21:28
@Author      : noahzhenli
@Email       : 
@Description : 
"""


from llama_cpp import Llama



model_file = "/data/zhenli/model_file/yi/01-ai--Yi-34B-Chat/ggml-model-q4_0.gguf"
# model_file = "/data/zhenli/model_file/yi/Yi-6B-Chat/ggml-model-q4_0.gguf"
llm = Llama(model_path=model_file, verbose=True, n_ctx=4096, n_threads=16, n_gpu_layers=40)

prompt = "你是谁？"



input = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant"
# output = llm(input, temperature=0.3, top_k=5, top_p=0.85, repeat_penalty=1.1, max_tokens=4096, stop=["<|im_end|>"])
output = llm(input, temperature=0.6, top_p=0.8, repeat_penalty=1.1, max_tokens=4096, stop=["<|im_end|>"])
print(output)





prompt = '''You are a document sorter, and you need to organize the following jumbled documents. Each line in the document is a separate piece of text, and you need to adjust the order of the different lines to restore it to a coherent article. Please note that you should select text from the given jumbled document, and you are not allowed to rewrite the text of the jumbled document, only to modify the order between different lines. If the text of a certain line cannot be combined with other texts, then place these texts at the end:


Jumbled Document"""
In this study, we introduce VL-GPT, a large vision-
language generative pre-trained transformer that enables the
unified training of both visual and linguistic data using an
auto-regressive objective, as depicted in Fig. 1. To achieve
this, we propose an image tokenizer-detokenizer framework
for the conversion between raw image pixels and contin-
uous visual embeddings, analogous to the role of the text
tokenization [19, 43] in language models. The framework
1arXiv:2312.09251v1  [cs.CV]  14 Dec 2023
Image TokenizerImage DetokenizerImage TokenizerText TokenizerLarge Vision-Language TransformerModelImage DetokenizerText DetokenizerVL-GPTInterleavedImage-text InputInterleavedImage-text GenerationMultimodal  Sequence Multimodal  Sequence Visual  Embeddings
Causal TransformerTransformerDecoder
Diffusion Decoder
Visual EncoderFigure 1. Overview of our proposed approach. The upper part delineates the image tokenizer-detokenizer framework, designed for encoding
images into continuous visual embeddings and reconstructing them in the pixel space. The lower part demonstrates the implementation
of our VL-GPT, where interleaved image-text data are encoded into multimodal sequence using image and text tokenizers, subsequently
processed by a transformer model auto-regressively. The image and text detokenizers are employed for generating respective outputs.
comprises an image tokenizer and an image detokenizer,
where the tokenizer encodes raw images into a sequence of
continuous visual embeddings, and the detokenizer decodes
the continuous embeddings into pixel space. To obtain vi-
sual continuous embeddings that are rich in both image de-
tails and semantic information, we employ the image em-
beddings and their corresponding caption embeddings ex-
tracted by pre-trained encoders ( i.e., CLIP [32]) as the su-
pervision for training of the framework. Furthermore, the
efficiency of the framework training is enhanced through
weight initialization from pre-trained image encoders and
high-quality image diffusion models.
"""

Restored Document:'''