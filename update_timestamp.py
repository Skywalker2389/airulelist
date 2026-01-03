#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新 Shadowrocket 配置文件时间戳脚本
作者：Jojo
用途：在每次 git commit 时自动更新配置文件中的时间戳
"""

import os
import re
import sys
from datetime import datetime, timezone, timedelta
import subprocess

def update_timestamp():
    """更新配置文件中的时间戳"""
    config_file = "shadowrocket-a-nomad.conf"
    
    # 检查配置文件是否存在
    if not os.path.exists(config_file):
        print(f"错误: 找不到配置文件 {config_file}")
        return False
    
    try:
        # 读取配置文件
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取当前时间（北京时间 UTC+8）
        beijing_tz = timezone(timedelta(hours=8))
        current_time = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
        
        # 定义要替换的模式：查找时间戳行（更宽松的匹配）
        pattern = r'# 最后更新：.*?\(自动生成\)'
        replacement = f'# 最后更新：{current_time} (自动生成)'
        
        # 执行替换
        new_content, count = re.subn(pattern, replacement, content)
        
        # 如果没有找到时间戳行，尝试在文件开头添加
        if count == 0:
            print("未找到时间戳行，将在文件开头添加...")
            new_content = f'# 最后更新：{current_time} (自动生成)\n{content}'
            count = 1
        
        # 检查是否有变化
        if new_content == content:
            print("配置文件无需更新")
            return True
        
        # 写回文件
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 成功更新时间戳为: {current_time}")
        
        # 将更新后的文件添加到 git staging area
        try:
            result = subprocess.run(['git', 'add', config_file], 
                                  check=True, 
                                  capture_output=True, 
                                  text=True)
            print(f"✅ 已将 {config_file} 添加到 git staging area")
        except subprocess.CalledProcessError as e:
            print(f"警告: 无法将文件添加到 git staging area: {e.stderr}")
        except FileNotFoundError:
            print("警告: git 命令未找到，请确保 git 已安装")
        
        return True
        
    except Exception as e:
        print(f"错误: 更新时间戳失败 - {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🔄 开始更新 Shadowrocket 配置文件时间戳...")
    
    if update_timestamp():
        print("🎉 时间戳更新完成！")
        sys.exit(0)
    else:
        print("❌ 时间戳更新失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()
