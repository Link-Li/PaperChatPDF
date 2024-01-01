# PaperChatPDF

## 计划

- [ ] pdf文件解析
  - [ ] 格式化标题和正文信息，丢弃表格和图片信息，表格和图片的说明信息单独存储
  - [ ] 额外存储未格式化的PDF信息，使用句号作为分割符
- [ ] 总结prompt设计，部分paper文本进行重排序 
- [ ] 总结prompt设计，paper总结
- [ ] paper切分向量化
- [ ] 设计prompt，理解论文内容
- [ ] 设计前后端
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
