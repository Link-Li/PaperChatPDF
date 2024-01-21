# PaperChatPDF

## 计划

- [x] pdf文件解析
  - [x] 格式化标题和正文信息，丢弃表格和图片信息，表格和图片的说明信息单独存储
  - [ ] 额外存储未格式化的PDF信息，使用句号作为分割符
- [x] 设计prompt，理解论文内容
  - [x] 完成关键词抽取prompt设计
  - [x] 翻译prompt设计
  - [x] 总结prompt设计，paper总结
- [ ] 设计前后端
  - [x] 联调前后端数据库
  - [ ] paper切分向量化，向量数据库搭建
  - [ ] 自动爬取arxiv相关论文进行总结
  - [ ] 分优先级处理候选paper
  - [ ] 前端进行搜索结果展示

## pdf文件解析

- LlamaIndex   pymupdf
- LangChain    pypdf
- fitz   PyMuPDF
- borb
- PyPDF2
- pdfminer
- PDFQuery
- pdfplumber
