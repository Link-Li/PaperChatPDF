
```
你是一个文档排序人员，你需要将下面的乱序文档进行排序。
文档中每一行都是一个段独立的文本，你需要调整不同行的顺序，然后组合成一篇通顺的文章。
请注意要从给定乱序文档中选择文本，并且不允许改写乱序文档的文本，只能修改不同行之间的顺序。
如果某行的文本无法和其他文本进行组合，那么就把这些文本放到最后：

参考范例"""
乱序文档"""
Given any interleaved image-text data, the image tok-
enizer and the text tokenizer initially encode them into a
multimodal sequence. More specifically, the image tok-
enizerEvconverts each image into Ncontinuous visual em-
beddings xv. Additionally, two special tokens [IMG]and
[/IMG]are appended at the beginning and end of the vi-
sual embeddings, respectively. The visual embeddings are
4
Rec LossRec LossInput imageImage caption
Visual continuous embedding xvImage embedding evText embedding	et
Estimated image embedding zvEstimated text embedding ztImage Tokenizer
Reconstruction Image !xUnused DuringTrainingImage Detokenizer
Causal TransformerTransformerDecoder
Visual Encoder
then combined with the discrete text tokens encoded by the
text tokenizer Etto form a interleaved multimodal sequence
v= (v1, v2, . . . , v n), where vican be either a discrete text
token or a continuous visual embedding. The multimodal
sequence vis then fed into the large VL model Mfor uni-
fied auto-regressive modeling.
"""

还原之后的文档："""
Given any interleaved image-text data, the image tokenizer and the text tokenizer initially encode them into a multimodal sequence. More specifically, the image tokenizerEvconverts each image into Ncontinuous visual embeddings xv. Additionally, two special tokens [IMG]and [/IMG]are appended at the beginning and end of the visual embeddings, respectively. The visual embeddings are then combined with the discrete text tokens encoded by the text tokenizer Etto form a interleaved multimodal sequence v= (v1, v2, . . . , v n), where vican be either a discrete text token or a continuous visual embedding. The multimodal sequence vis then fed into the large VL model Mfor unified auto-regressive modeling.

4
Rec LossRec LossInput imageImage caption
Visual continuous embedding xvImage embedding evText embedding	et
Estimated image embedding zvEstimated text embedding ztImage Tokenizer
Reconstruction Image !xUnused DuringTrainingImage Detokenizer
Causal TransformerTransformerDecoder
Visual Encoder
"""
"""

乱序文档"""
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

还原之后的文档：

```





v1
```
You are a document sorter, and you need to organize the following disordered documents. Each line in the document is a separate text block. You need to adjust the order of different lines and then restore it into a coherent article. Please note that you must select text from the given disordered document, and you are not allowed to rewrite the text of the disordered document, only to change the order of the different lines:

Disordered Document"""
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

Restored Document:

```




v2
```
You are a document sorter, and you need to organize the following jumbled documents. Each line in the document is a separate piece of text, and you need to adjust the order of the different lines to restore it to a coherent article. Please note that you should select text from the given jumbled document, and you are not allowed to rewrite the text of the jumbled document, only to modify the order between different lines. If the text of a certain line cannot be combined with other texts, then place these texts at the end:

Reference Example"""
Jumbled Document"""
Given any interleaved image-text data, the image tok-
enizer and the text tokenizer initially encode them into a
multimodal sequence. More specifically, the image tok-
enizerEvconverts each image into Ncontinuous visual em-
beddings xv. Additionally, two special tokens [IMG]and
[/IMG]are appended at the beginning and end of the vi-
sual embeddings, respectively. The visual embeddings are
4
Rec LossRec LossInput imageImage caption
Visual continuous embedding xvImage embedding evText embedding	et
Estimated image embedding zvEstimated text embedding ztImage Tokenizer
Reconstruction Image !xUnused DuringTrainingImage Detokenizer
Causal TransformerTransformerDecoder
Visual Encoder
then combined with the discrete text tokens encoded by the
text tokenizer Etto form a interleaved multimodal sequence
v= (v1, v2, . . . , v n), where vican be either a discrete text
token or a continuous visual embedding. The multimodal
sequence vis then fed into the large VL model Mfor uni-
fied auto-regressive modeling.
"""

Restored Document:"""
Given any interleaved image-text data, the image tokenizer and the text tokenizer initially encode them into a multimodal sequence. More specifically, the image tokenizerEvconverts each image into Ncontinuous visual embeddings xv. Additionally, two special tokens [IMG]and [/IMG]are appended at the beginning and end of the visual embeddings, respectively. The visual embeddings are then combined with the discrete text tokens encoded by the text tokenizer Etto form a interleaved multimodal sequence v= (v1, v2, . . . , v n), where vican be either a discrete text token or a continuous visual embedding. The multimodal sequence vis then fed into the large VL model Mfor unified auto-regressive modeling.

4
Rec LossRec LossInput imageImage caption
Visual continuous embedding xvImage embedding evText embedding	et
Estimated image embedding zvEstimated text embedding ztImage Tokenizer
Reconstruction Image !xUnused DuringTrainingImage Detokenizer
Causal TransformerTransformerDecoder
Visual Encoder
"""
"""

You are a document sorter, and you need to organize the following jumbled documents. Each line in the document is a separate piece of text, and you need to adjust the order of the different lines to restore it to a coherent article. Please note that you should select text from the given jumbled document, and you are not allowed to rewrite the text of the jumbled document, only to modify the order between different lines. If the text of a certain line cannot be combined with other texts, then place these texts at the end:


Jumbled Document"""
Publicly available datasets are utilized for different phrase
of the VL-GPT training. The image tokenizer-detokenizer
framework is trained on image-text pairs from CC3M [37],
LAION-Aestheics [20], and LAION-COCO [36]. During the unified multimodal pre-training of VL-GPT, a
combination of paired and interleaved image-text data is
employed. The image-text pairs remain consistent with
the preview phase, while the interleaved image-text sequences are acquired from Multimodal-C4 (MMC4) [57]
and OBELICS [21]. We adopt similar preprocessing techniques for interleaved data implemented in Flamingo [1].
For each document, a maximum of 5 images and their associated captions are randomly sampled to construct a subsequence with a token length of up to 512. Additionally,
for paired and interleaved image-text data, each image is
randomly placed before or after its corresponding caption.
For the instruction tuning of VL-GPT, a compositional instruction tuning dataset is constructed from various sources,
encompassing conversational data from LLAVA [25] and
SVIT [55], image-text pair data from COCO Caption [5],
and image editing data from InstructPix2Pix [3] and Magicbrush [53]. These datasets are restructured into a conver
Models Image-Text understanding Text-to-image generations
COCO VQAv2 GQA OKVQA VizWiz VisDial COCO FID (↓)
▶ VL Understanding or generation Models
MetaLM [14] 82.2 41.1 - 11.4 - - -
Kosmos-1 [16] 84.7 51.0 - - 29.2 - -
Flamingo-9B¶
[1] 79.4 51.8 - 44.7 28.8 48.0 -
SD v1.5 [35] - - - - - - 9.22
▶ Unified VL understanding and generation Pre-trained Models
GILL [18] - - - - - - 12.2
Kosmos-G-1.9B [30] - - - - - - 10.99
SEED-OPT2.7B [11] 119.0 42.8 28.8 - - - -
Emu [39] 112.4 52.0 - 38.2 34.2 47.4 11.66
Emu†
[39] - 52.9 - 42.8 34.4 47.8 -
VL-GPT 116.4 51.7 34.6 35.8 34.7 49.9 12.25
VL-GPT†
119.2 55.3 38.1 41.5 35.2 49.6 -
▶ Unified VL understanding and generation Models with Instruction-tuning or Fine-tuning
CM3Leon-7B [51] 61.6 47.6 - 23.8 37.6 22.6 10.82
Emu-I [39] - 57.5 - 46.2 38.1 50.1 -
NExT-GPT§
[48] 156.7 - - - - - 11.28
DreamLLM-7B [9] 115.4 56.6 - 44.3 38.1 - 8.46
VL-GPT-I 133.7 67.2 51.5 50.3 38.9 51.8 11.53
sational format using the template provided in the appendix.
For further details regarding preprocessing and construction
of our training dataset, please refer to the appendix as well.
"""

Restored Document:

```





v3
```

You are a document sorter, and you need to organize the following jumbled documents. Each line in the document is a separate piece of text, and you need to adjust the order of the different lines to restore it to a coherent article. Please note that you should select text from the given jumbled document, and you are not allowed to rewrite the text of the jumbled document, only to modify the order between different lines. If the text of a certain line cannot be combined with other texts, then place these texts at the end:


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

Restored Document:

```

"In this study, we introduce VL-GPT, a large vision-language generative pre-trained transformer that enables the unified training of both visual and linguistic data using an auto-regressive objective, as depicted in Fig. 1. To achieve this, we propose an image tokenizer-detokenizer framework for the conversion between raw image pixels and continuous visual embeddings, analogous to the role of the text tokenization [19, 43] in language models.

The framework comprises an image tokenizer and an image detokenizer, where the tokenizer encodes raw images into a sequence of continuous visual embeddings, and the detokenizer decodes the continuous embeddings into pixel space. To obtain visual continuous embeddings that are rich in both image details and semantic information, we employ the image embeddings and their corresponding caption embeddings extracted by pre-trained encoders (i.e., CLIP [32]) as the supervision for training of the framework. Furthermore, the efficiency of the framework training is enhanced through weight initialization from pre-trained image encoders and high-quality image diffusion models.

Figure 1. Overview of our proposed approach. The upper part delineates the image tokenizer-detokenizer framework, designed for encoding images into continuous visual embeddings and reconstructing them in the pixel space. The lower part demonstrates the implementation of our VL-GPT, where interleaved image-text data are encoded into multimodal sequence using image and text tokenizers, subsequently processed by a transformer model auto-regressively. The image and text detokenizers are employed for generating respective outputs."


In this study, we introduce VL-GPT, a large vision-language generative pre-trained transformer that enables the unified training of both visual and linguistic data using an auto-regressive objective, as depicted in Fig. 1. To achieve this, we propose an image tokenizer-detokenizer framework for the conversion between raw image pixels and continuous visual embeddings, analogous to the role of the text tokenization [19, 43] in language models. The framework comprises an image tokenizer and an image detokenizer, where the tokenizer encodes raw images into a sequence of continuous visual embeddings, and the detokenizer decodes the continuous embeddings into pixel space. To obtain visual continuous embeddings that are rich in both image details and semantic information, we employ the image embeddings and their corresponding caption embeddings extracted by pre-trained encoders (i.e., CLIP [32]) as the supervision for training of the framework. Furthermore, the efficiency of the framework training is enhanced through weight initialization from pre-trained image encoders and high-quality image diffusion models.

Image TokenizerImage DetokenizerImage TokenizerText TokenizerLarge Vision-Language TransformerModelImage DetokenizerText DetokenizerVL-GPTInterleavedImage-text InputInterleavedImage-text GenerationMultimodal Sequence Multimodal Sequence Visual Embeddings
Causal TransformerTransformerDecoder
Diffusion Decoder
Visual EncoderFigure 1. Overview of our proposed approach. The upper part delineates the image tokenizer-detokenizer framework, designed for encoding images into continuous visual embeddings and reconstructing them in the pixel space. The lower part demonstrates the implementation of our VL-GPT, where interleaved image-text data are encoded into multimodal sequence using image and text tokenizers, subsequently processed by a transformer model auto-regressively. The image and text detokenizers are employed for generating respective outputs.

arXiv:2312.09251v1 [cs.CV] 14 Dec 2023