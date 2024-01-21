
-- 创建pdf存储表
CREATE TABLE pdf_info (
 id int AUTO_INCREMENT PRIMARY KEY,
 title VARCHAR(255) NOT NULL COMMENT 'paper的标题',
 abstract TEXT NOT NULL COMMENT 'paper的摘要',
 abstract_chinese TEXT COMMENT 'paper的摘要的中文翻译结果',
 title_llm_generates TEXT COMMENT '根据paper的标题提取的关键词的大模型生成结果',
 title_core_keywords TEXT COMMENT '根据paper的标题提取的关键词',
 abstract_llm_generates TEXT COMMENT '根据paper的摘要提取的关键词的大模型生成结果',
 abstract_core_keywords TEXT COMMENT '根据paper的摘要提取关键词',
 pdf_save_path VARCHAR(2048) NOT NULL COMMENT 'paper的pdf的保存位置',
 json_save_path VARCHAR(2048) NOT NULL COMMENT 'paper的json解析结果的保存位置'
);