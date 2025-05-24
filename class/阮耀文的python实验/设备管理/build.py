import PyInstaller.__main__
import os
import shutil
from pathlib import Path

def build_exe():
    # 获取当前目录
    current_dir = Path(__file__).parent.absolute()
    
    # 清理之前的构建文件
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

    # PyInstaller参数
    args = [
        'main.py',  # 主程序文件
        '--name=设备管理系统',  # 生成的exe名称
        '--windowed',  # 使用GUI模式
        '--onefile',  # 打包成单个exe文件
        '--noconfirm',  # 覆盖输出目录
        '--clean',  # 清理临时文件
        f'--workpath={current_dir / "build"}',  # 指定构建目录
        f'--distpath={current_dir / "dist"}',  # 指定输出目录
        f'--specpath={current_dir}',  # 指定spec文件目录
        '--add-data=ui;ui',  # 添加UI资源
        '--add-data=database;database',  # 添加数据库脚本
        '--add-data=config.py;.',  # 添加配置文件
        '--hidden-import=PyQt5',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=bcrypt',
        '--hidden-import=sqlite3',
        '--hidden-import=python-dotenv',
        '--hidden-import=cryptography',
    ]

    # 运行PyInstaller
    PyInstaller.__main__.run(args)
    
    print("\n打包完成！")
    print(f"exe文件位于: {current_dir / 'dist' / '设备管理系统.exe'}")
    print("\n注意事项：")
    print("1. 首次运行时会自动创建SQLite数据库")
    print("2. 默认管理员账号：admin")
    print("3. 所有数据保存在程序所在目录的data.db文件中")

if __name__ == '__main__':
    build_exe() 