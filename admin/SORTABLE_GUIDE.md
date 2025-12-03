# Publications 拖曳排序功能使用指南

## 功能說明

Publications 管理頁面現在支援拖曳排序功能，讓你可以輕鬆調整出版物的顯示順序。

## 使用方式

### 1. 開啟 Publications 頁面

訪問：`http://localhost:5000/publications`

### 2. 拖曳排序

1. **找到拖曳手柄**：每一列最左側有一個 ⋮⋮ 圖示（雙豎線）
2. **點擊並按住**：將滑鼠移到 ⋮⋮ 圖示上，點擊並按住滑鼠左鍵
3. **拖曳**：按住滑鼠左鍵的同時，上下移動滑鼠
4. **放開**：移動到目標位置後，放開滑鼠左鍵

### 3. 自動儲存

- 放開滑鼠後，新的順序會**自動儲存**到 `dataset/publications.json`
- 不需要額外點擊「儲存」按鈕
- 瀏覽器控制台會顯示 "Order saved successfully" 訊息

## 視覺效果

### 拖曳時的效果

- **被拖曳的列**：會有淺灰色背景和陰影效果
- **目標位置**：會顯示一個灰色的佔位符，表示放開後會插入的位置
- **滑鼠游標**：會變成移動圖示（十字箭頭）

### 拖曳手柄樣式

- **正常狀態**：淺灰色 (#999)
- **滑鼠懸停**：深灰色 (#333)
- **游標樣式**：移動游標 (cursor: move)

## 注意事項

### ⚠️ 篩選時無法拖曳

當使用「類型篩選」功能時，拖曳功能會自動停用。原因：

- 篩選會隱藏部分資料
- 在隱藏資料的情況下拖曳可能導致順序混亂
- 要使用拖曳功能，請先清除篩選條件（選擇「所有類型」）

### 💡 最佳實踐

1. **先清除篩選**：確保顯示所有出版物
2. **一次移動一個**：避免同時拖曳多個項目
3. **確認順序**：拖曳後檢查順序是否正確
4. **重新整理測試**：可以重新整理頁面確認順序已儲存

## 技術細節

### 使用的技術

- **jQuery UI Sortable**：拖曳排序核心功能
- **AJAX**：自動儲存順序到後端
- **Flask API**：`POST /api/publications/reorder` 端點

### 資料儲存

順序儲存在 `dataset/publications.json` 中：

```json
{
  "publications": [
    { "id": "j13", "type": "journal", ... },
    { "id": "j12", "type": "journal", ... },
    { "id": "c11", "type": "conference", ... },
    ...
  ]
}
```

陣列的順序就是顯示順序。

### API 端點

**POST** `/api/publications/reorder`

**請求格式**：
```json
{
  "order": ["j13", "j12", "c11", "j11", ...]
}
```

**回應格式**：
```json
{
  "success": true
}
```

## 疑難排解

### 問題：拖曳沒有反應

**可能原因**：
1. 篩選功能已啟用
2. JavaScript 載入失敗
3. jQuery UI 未正確載入

**解決方案**：
1. 清除篩選條件（選擇「所有類型」）
2. 重新整理頁面（Ctrl+F5 強制重新載入）
3. 檢查瀏覽器控制台是否有錯誤訊息

### 問題：順序沒有儲存

**可能原因**：
1. 後端 API 錯誤
2. JSON 文件權限問題

**解決方案**：
1. 檢查瀏覽器控制台的錯誤訊息
2. 檢查 Flask 終端機的錯誤日誌
3. 確認 `dataset/publications.json` 有寫入權限

### 問題：拖曳後頁面顯示錯亂

**解決方案**：
1. 重新整理頁面（F5）
2. 如果問題持續，檢查 JSON 文件格式是否正確：
   ```bash
   python3 -m json.tool dataset/publications.json
   ```

## 前端網站同步

拖曳排序後，前端網站 (`http://localhost:3000`) 會自動顯示新的順序：

1. Admin 修改順序 → 儲存到 `publications.json`
2. 前端網站讀取 `publications.json` → 顯示新順序
3. 重新整理前端網站即可看到變更

## 測試頁面

我們提供了一個簡單的測試頁面來驗證拖曳功能：

**開啟測試頁面**：
```bash
# 在瀏覽器中開啟
file:///mnt/e/project/newPao/admin/test_sortable.html
```

這個測試頁面可以幫助你：
- 理解拖曳功能的運作方式
- 測試拖曳手柄的互動效果
- 查看即時的順序變化

## 相關資源

- [jQuery UI Sortable 官方文件](https://jqueryui.com/sortable/)
- [Bootstrap 5 文件](https://getbootstrap.com/docs/5.3/)
- [Flask 文件](https://flask.palletsprojects.com/)

