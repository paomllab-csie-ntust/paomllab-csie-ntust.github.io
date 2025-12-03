#!/bin/bash

# Laboratory Website Admin Panel 啟動腳本

echo "=========================================="
echo "  Laboratory Website Admin Panel"
echo "=========================================="
echo ""

# 檢查是否在正確的目錄
if [ ! -d "admin" ]; then
    echo "❌ 錯誤：請在專案根目錄執行此腳本"
    exit 1
fi

# 檢查 Python 是否安裝
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤：未找到 Python 3"
    exit 1
fi

# 檢查依賴是否安裝
echo "📦 檢查依賴..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask 未安裝，正在安裝依賴..."
    pip3 install -r admin/requirements.txt
fi

echo "✅ 依賴檢查完成"
echo ""

# 啟動 Flask Admin
echo "🚀 啟動 Admin Panel..."
echo "   URL: http://localhost:5000"
echo ""
echo "💡 提示："
echo "   - 按 Ctrl+C 停止服務"
echo "   - 前端網站預覽：http://localhost:3000"
echo ""

python3 admin/app.py

