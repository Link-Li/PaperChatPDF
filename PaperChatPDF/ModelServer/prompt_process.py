# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/21 20:01
@Author      : noahzhenli
@Email       : 
@Description : 
"""


def yi_prompt_process(message_list, llm_tokenizer):
    prompt = llm_tokenizer.apply_chat_template(conversation=message_list, tokenize=False,
                                       add_generation_prompt=True)
    return prompt
