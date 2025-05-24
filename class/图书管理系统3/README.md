# 图书管理系统

这是一个基于PyQt5和SQLite的图书管理系统，提供图书借阅、用户管理等功能。

## 项目结构

```
├── config.py           # 配置文件
├── database.py         # 数据库操作
├── models.py           # 数据模型
├── utils.py           # 工具函数
├── requirements.txt    # 项目依赖
├── library.db         # SQLite数据库文件
└── ui/                # UI相关文件
    ├── *.ui           # Qt Designer UI文件
    └── *.py           # UI Python文件
```

## 功能特性

- 用户管理（注册、登录、修改信息）
- 图书管理（添加、修改、删除图书）
- 借阅管理（借书、还书、超期提醒）
- 数据持久化（SQLite数据库存储）

## 安装说明

1. 克隆项目到本地
2. 创建虚拟环境（推荐）：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
4. 初始化数据库：
   ```bash
   python database.py
   ```
5. 运行程序：
   ```bash
   python main.py
   ```

## 使用说明

1. 首次使用需要注册管理员账号
2. 使用管理员账号可以：
   - 添加/修改/删除图书
   - 管理用户账号
   - 查看借阅记录
3. 普通用户可以：
   - 借阅/归还图书
   - 查看个人借阅记录
   - 修改个人信息

## 注意事项

- 图书借阅期限为30天
- 超期将产生罚款（0.5元/天）
- 请及时归还图书 