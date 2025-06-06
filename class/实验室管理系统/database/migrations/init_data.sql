-- 插入管理员账号
INSERT OR IGNORE INTO users (
    username,
    password,
    role,
    real_name,
    teacher_id,
    create_time
) VALUES (
    'admin',           -- 用户名
    '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',          -- 密码admin123
    'admin',          -- 角色
    '系统管理员',      -- 真实姓名
    1,                -- teacher_id（管理员的teacher_id指向自己的id）
    CURRENT_TIMESTAMP  -- 创建时间
);

-- 更新管理员的teacher_id为其自己的id
UPDATE users 
SET teacher_id = id 
WHERE username = 'admin'; 
-- 插入教师测试账号
INSERT OR IGNORE INTO users (
    username,
    password,
    role,
    real_name,
    teacher_id,
    create_time
) VALUES (
    'teacher',           -- 用户名
    'cde383eee8ee7a4400adf7a15f716f179a2eb97646b37e089eb8d6d04e663416',          -- 密码teacher123
    'teacher',          -- 角色
    '教师测试账号',      -- 真实姓名
    1,                -- teacher_id（管理员的teacher_id指向自己的id）
    CURRENT_TIMESTAMP  -- 创建时间
);

-- 更新管理员的teacher_id为其自己的id
UPDATE users 
SET teacher_id = id 
WHERE username = 'teacher'; 
INSERT OR IGNORE INTO users (
    username,
    password,
    role,
    real_name,
    teacher_id,
    create_time
) VALUES (
    '123456',           -- 用户名
    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',          -- 密码teacher123
    'student',          -- 角色
    '李四',      -- 真实姓名
    1,                -- teacher_id（管理员的teacher_id指向自己的id）
    CURRENT_TIMESTAMP  -- 创建时间
);
INSERT OR IGNORE INTO users (
    username,
    password,
    role,
    real_name,
    teacher_id,
    create_time
) VALUES (
    '1234567',           -- 用户名
    '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',          -- 密码teacher123
    'student',          -- 角色
    '张三',      -- 真实姓名
    1,                -- teacher_id（管理员的teacher_id指向自己的id）
    CURRENT_TIMESTAMP  -- 创建时间
);
INSERT OR IGNORE INTO experiments (
    creator_id,
    title,
    description,
    create_time
) VALUES (
    2,
    '图书管理系统',
    '写一个图书管理系统需要用python实现',
    CURRENT_TIMESTAMP

);
INSERT OR IGNORE INTO experiments (
    creator_id,
    title,
    description,
    create_time
) VALUES (
    2,
    '数据管理系统',
    '写一个数据管理系统需要用python实现',
    CURRENT_TIMESTAMP

);
INSERT OR IGNORE INTO experiments (
    creator_id,
    title,
    description,
    create_time
) VALUES (
    2,
    '实验管理系统',
    '写一个实验管理系统需要用python实现',
    CURRENT_TIMESTAMP

);
