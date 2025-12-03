# Admin Panel 快速開始指南

## 🚀 5 分鐘快速上手

### 步驟 1：啟動服務

```bash
# 進入專案目錄
cd /mnt/e/project/newPao

# 啟動 Admin Panel
python3 admin/app.py

# 或使用啟動腳本
./start_admin.sh
```

服務會在 `http://localhost:5000` 啟動。

### 步驟 2：開啟瀏覽器

在瀏覽器中訪問：`http://localhost:5000`

你會看到儀表板，顯示目前的統計資訊。

### 步驟 3：管理 Publications

1. 點擊側邊欄的「Publications」
2. 嘗試以下操作：

#### 新增出版物
- 點擊「新增 Publication」按鈕
- 選擇類型（Journal/Conference/Book/Dissertation）
- 填寫資訊
- 點擊「儲存」

#### 拖曳排序（新功能！）
- 找到最左側的 ⋮⋮ 圖示
- 點擊並按住
- 拖曳到想要的位置
- 放開滑鼠，自動儲存

#### 編輯出版物
- 點擊「✏️」按鈕
- 修改資訊
- 點擊「儲存」

#### 刪除出版物
- 點擊「🗑️」按鈕
- 確認刪除

### 步驟 4：管理 Members

1. 點擊側邊欄的「Members」
2. 嘗試以下操作：

#### 新增成員
- 點擊「新增 Member」按鈕
- 填寫姓名、學位、年份
- 上傳照片（選填）
- 選擇狀態（在學中/已畢業）
- 點擊「儲存」

#### 篩選成員
- 使用年份下拉選單篩選
- 使用狀態下拉選單篩選

### 步驟 5：管理 Events

1. 點擊側邊欄的「Events」
2. 嘗試以下操作：

#### 新增活動
- 點擊「新增 Event」按鈕
- 填寫標題、日期
- 上傳活動照片（必填）
- 點擊「儲存」

---

## 💡 常用操作

### 查看前端網站

1. 啟動前端服務：
   ```bash
   python3 -m http.server 3000
   ```

2. 訪問：`http://localhost:3000`

3. 在 Admin Panel 中點擊「查看網站」連結

### 推送變更到 GitHub

```bash
# 檢查變更
git status

# 添加變更
git add dataset/*.json asset/

# 提交變更
git commit -m "Update publications/members/events"

# 推送到 GitHub
git push origin main
```

GitHub Pages 會自動更新網站。

---

## 🎯 拖曳排序快速教學

### Publications 拖曳排序

**目的**：調整出版物在前端網站的顯示順序

**步驟**：

1. **開啟 Publications 頁面**
   - 訪問：`http://localhost:5000/publications`

2. **確認顯示所有項目**
   - 篩選器選擇「所有類型」
   - 如果有篩選，拖曳功能會被停用

3. **開始拖曳**
   - 找到最左側的 ⋮⋮ 圖示（拖曳手柄）
   - 滑鼠移到圖示上，游標會變成移動圖示
   - 點擊並按住滑鼠左鍵

4. **移動到目標位置**
   - 按住滑鼠左鍵，上下移動
   - 會看到灰色佔位符顯示目標位置
   - 被拖曳的列會有陰影效果

5. **放開滑鼠**
   - 移動到目標位置後，放開滑鼠左鍵
   - 順序會自動儲存到 `dataset/publications.json`
   - 瀏覽器控制台會顯示 "Order saved successfully"

6. **驗證變更**
   - 重新整理頁面，確認順序已儲存
   - 訪問前端網站，確認顯示順序已更新

**提示**：
- ✅ 拖曳手柄在最左側，容易點擊
- ✅ 視覺回饋清晰（陰影、佔位符）
- ✅ 自動儲存，無需額外操作
- ⚠️ 篩選時無法拖曳，請先清除篩選

---

## 📱 鍵盤快捷鍵

目前沒有特定的鍵盤快捷鍵，但你可以使用瀏覽器的標準快捷鍵：

- **Ctrl+F5** - 強制重新載入頁面
- **F12** - 開啟開發者工具
- **Ctrl+Shift+I** - 開啟開發者工具
- **Esc** - 關閉模態框

---

## 🔍 疑難排解

### 問題：無法啟動 Admin Panel

**錯誤訊息**：`ModuleNotFoundError: No module named 'flask'`

**解決方案**：
```bash
pip3 install -r admin/requirements.txt
```

### 問題：照片無法顯示

**可能原因**：路徑錯誤或檔案不存在

**解決方案**：
1. 檢查照片是否存在於 `/asset/member/` 或 `/asset/event/`
2. 重新整理頁面（Ctrl+F5）
3. 檢查瀏覽器控制台的錯誤訊息

### 問題：拖曳沒有反應

**可能原因**：篩選功能已啟用

**解決方案**：
1. 清除篩選條件（選擇「所有類型」）
2. 重新整理頁面

### 問題：變更沒有儲存

**可能原因**：JSON 文件權限問題

**解決方案**：
```bash
# 檢查權限
ls -la dataset/

# 如果需要，修改權限
chmod 644 dataset/*.json
```

---

## 📚 更多資源

- **完整功能列表**：查看 `admin/FEATURES.md`
- **拖曳排序指南**：查看 `admin/SORTABLE_GUIDE.md`
- **使用說明**：查看 `admin/README.md`
- **測試頁面**：開啟 `admin/test_sortable.html`

---

## 🎉 開始使用！

現在你已經準備好開始使用 Admin Panel 了！

1. 啟動服務
2. 開啟瀏覽器
3. 開始管理資料
4. 推送到 GitHub

祝你使用愉快！🚀

