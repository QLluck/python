-- 初始化数据库结构

-- 创建用户表
-- 如果，不存在users 就创建表
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 用户ID，主键，自动递增 设置主键
    username TEXT NOT NULL UNIQUE,         -- 用户名，不能为空，必须唯一
    password TEXT NOT NULL,                -- 密码，不能为空
    role TEXT NOT NULL,                    -- 用户角色（如admin/teacher/student）
    real_name TEXT,                        -- 真实姓名，可以为空
    student_id TEXT,                       -- 学号，可以为空
    teacher_id INTEGER,                    -- 指导教师ID，对于学生指向其指导教师，对于教师和管理员指向自己
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间，默认为当前时间
    FOREIGN KEY (teacher_id) REFERENCES users(id)     -- teacher_id 关联到用户表的id
);

-- 创建实验任务表
-- 如果，不存在experiments 就创建表
CREATE TABLE IF NOT EXISTS experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 实验ID，主键，自动递增
    creator_id INTEGER NOT NULL,           -- 创建者ID（教师），外键关联users表
    title TEXT NOT NULL,                   -- 实验标题，不能为空
    description TEXT,                      -- 实验描述，可以为空
    deadline DATETIME,                     -- 截止时间
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间，默认为当前时间
    FOREIGN KEY (creator_id) REFERENCES users(id)     -- 关联到用户表（创建者）
);

-- 创建作业提交表
-- 如果，不存在submissions 就创建表
CREATE TABLE IF NOT EXISTS submissions ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 提交ID，主键，自动递增
    student_id INTEGER NOT NULL,           -- 学生ID，外键关联users表
    experiment_id INTEGER NOT NULL,        -- 实验ID，外键关联experiments表
    submit_time DATETIME NOT NULL,         -- 提交时间
    content TEXT NOT NULL,               -- 提交的内容
    score FLOAT,                           -- 分数
    comment TEXT,                          -- 评语
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 创建时间，默认为当前时间
    FOREIGN KEY (student_id) REFERENCES users(id),           -- 关联到用户表
    FOREIGN KEY (experiment_id) REFERENCES experiments(id)   -- 关联到实验表
);

-- 在此处添加其他表结构 