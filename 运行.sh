#!/bin/bash

echo "温馨提示："
echo "1. 本程序在 Python 3.13 上开发，请确保已安装 Python3.13 或相近版本。"
echo "2. 本程序依赖 tkinter 模块，请确保已安装 tkinter。参考安装命令：python3 -m pip install tkinter"
echo "3. 本程序在 MacOS 上开发，请确保已安装 python-tk。参考安装命令：brew install python-tk"

which Python3 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "没有检测到 Python3，请安装 Python3 之后再运行本程序。"
else
    python3 main.py
    echo "程序运行结束。"
fi