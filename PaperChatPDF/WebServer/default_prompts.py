# -*- coding: utf-8 -*-
"""
@Time        : 2024/1/21 20:32
@Author      : noahzhenli
@Email       : 
@Description : 
"""

extract_abstract_core_keywords_prompt = '''Based on the provided abstract, identify and select 3 professional keywords. These keywords should meet the following criteria:

1. Specificity: They should precisely reflect the core themes and methods of the research.
2. Relevance: They must be closely related to the content of the abstract and suitable for referring to the key aspects of the study.
3. Professionalism: They should be terms that are widely recognized and utilized within the research field.
4. They will be used to retrieve research papers in similar fields through academic search engines. Ensure that the chosen keywords can effectively guide researchers or scholars in finding research works akin to this abstract.
5. Do not directly select vocabulary from the abstract unless you believe they are irreplaceable and directly indicate the specific fields of research. The choice of keywords should demonstrate the ability to comprehend and analyze the contents of the abstract.
6.The length of each keyword should not exceed 3.

Abstract: """
{prompt}
"""

Please list your selected keywords below:
1.
2.
3.
'''


extract_title_core_keywords_prompt = '''Based on the provided paper title, identify and select 2 professional keywords. These keywords should meet the following criteria:

1. Specificity: They should precisely reflect the core themes and methods of the research.
2. Relevance: They must be closely related to the content of the abstract and suitable for referring to the key aspects of the study.
3. Professionalism: They should be terms that are widely recognized and utilized within the research field.
4. They will be used to retrieve research papers in similar fields through academic search engines. Ensure that the chosen keywords can effectively guide researchers or scholars in finding research works akin to this abstract.
5. The length of each keyword should not exceed 3.

Abstract: """
{prompt}
"""

Please list your selected keywords below:
1.
2.
'''