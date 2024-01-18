


-- mysql -h xxx.xxx.xxx.xxx -u root -P -p


-- 显示数据库
show databases;

-- 创建数据库
CREATE DATABASE paper_chat_pdf;

-- 创建测试表
CREATE TABLE userv2 (
 id int AUTO_INCREMENT PRIMARY KEY,
 username VARCHAR(50) NOT NULL,
 email VARCHAR(100) NOT NULL
);


-- 创建pdf存储表
CREATE TABLE pdf_info (
 id int AUTO_INCREMENT PRIMARY KEY,
 title VARCHAR(255) NOT NULL,
 abstract TEXT NOT NULL,
 abstract_chinese TEXT,
 paper_summary TEXT,
 pdf_save_path VARCHAR(2048) NOT NULL,
 json_save_path VARCHAR(2048) NOT NULL
);