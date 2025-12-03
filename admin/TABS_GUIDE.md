# Publications Tab 分頁功能使用指南

## 功能概述

Publications 管理頁面現在使用 **Bootstrap Nav Tabs** 來分類顯示不同類型的出版物，讓管理更加直觀和高效。

## Tab 分頁說明

### 📋 全部 (All)

**用途**：顯示所有類型的出版物（僅供查看）

**欄位**：
- ID
- 類型（帶顏色標籤）
- 標題
- 作者
- 年份
- 操作（編輯、刪除）

**特色**：
- ⚠️ **不支援拖曳排序**（避免不同類型交錯）
- 可以看到完整的出版物列表
- 適合快速瀏覽所有出版物
- 類型標籤使用不同顏色區分：
  - 🔵 Journal - 藍色
  - 🟢 Conference - 綠色
  - 🟡 Book - 黃色

**注意**：
- 此 Tab 僅供查看，無法拖曳排序
- 請切換到 Journal、Conference 或 Book Tab 進行排序

### 📘 Journal

**用途**：只顯示 Journal 類型的出版物

**欄位**：
- 拖曳手柄 (⋮⋮)
- ID
- 標題
- 作者
- 年份
- **Volume**（期刊卷號）
- **Pages**（頁碼）
- 操作（編輯、刪除）

**特色**：
- 專注於 Journal 相關資訊
- 顯示 Journal 特有的 Volume 和 Pages 欄位
- 適合批次檢視和管理 Journal 出版物

### 🎤 Conference

**用途**：只顯示 Conference 類型的出版物

**欄位**：
- 拖曳手柄 (⋮⋮)
- ID
- 標題
- 作者
- 年份
- **Location**（會議地點）
- 操作（編輯、刪除）

**特色**：
- 專注於 Conference 相關資訊
- 顯示 Conference 特有的 Location 欄位
- 適合管理會議論文

### 📖 Book

**用途**：只顯示 Book 類型的出版物

**欄位**：
- 拖曳手柄 (⋮⋮)
- ID
- 標題
- 作者
- 年份
- **Publisher**（出版社）
- 操作（編輯、刪除）

**特色**：
- 專注於 Book 相關資訊
- 顯示 Book 特有的 Publisher 欄位
- 適合管理書籍章節



## 使用方式

### 切換 Tab

1. 點擊頁面上方的 Tab 按鈕
2. 頁面會立即切換到對應的分類
3. 只顯示該類型的出版物

### 在 Tab 中拖曳排序

⚠️ **重要**：只有類型專屬的 Tab（Journal、Conference、Book）支援拖曳排序，「全部」Tab 不支援拖曳。

1. **選擇 Tab**：切換到想要排序的類型 Tab（Journal、Conference、Book）
2. **拖曳排序**：
   - 點擊並按住最左側的 ⋮⋮ 圖示
   - 拖曳到想要的位置
   - 放開滑鼠
3. **自動儲存**：
   - 只會重新排序該類型的出版物
   - 其他類型的順序保持不變
   - 順序會自動儲存到 `dataset/publications.json`
   - 頁面會自動重新載入
   - 重新載入後會自動回到拖曳前的 Tab

### 建議的工作流程

#### 新增出版物
1. 點擊「新增 Publication」按鈕
2. 選擇類型
3. 填寫資訊
4. 儲存後會出現在對應的 Tab 中

#### 編輯出版物
1. 切換到對應的 Tab（或在「全部」Tab）
2. 點擊「✏️」編輯按鈕
3. 修改資訊
4. 儲存

#### 刪除出版物
1. 切換到對應的 Tab（或在「全部」Tab）
2. 點擊「🗑️」刪除按鈕
3. 確認刪除

#### 調整順序
1. **切換到對應的類型 Tab**（Journal、Conference、Book）
2. 只會重新排序該類型的出版物
3. 拖曳到想要的位置
4. 自動儲存並重新載入
5. 重新載入後會自動回到拖曳前的 Tab
6. ⚠️ 「全部」Tab 不支援拖曳排序

## 視覺設計

### Tab 樣式

- **未選中**：灰色文字，無底線
- **懸停**：藍色文字，藍色底線
- **選中**：藍色文字，藍色底線，粗體

### Tab 圖示

- 📋 全部 - `fa-list`
- 📘 Journal - `fa-book`
- 🎤 Conference - `fa-users`
- 📖 Book - `fa-book-open`

## 技術細節

### HTML 結構

```html
<div class="nav nav-tabs" id="nav-tab" role="tablist">
    <button class="nav-link active" id="nav-all-tab" ...>全部</button>
    <button class="nav-link" id="nav-journal-tab" ...>Journal</button>
    <button class="nav-link" id="nav-conference-tab" ...>Conference</button>
    <button class="nav-link" id="nav-book-tab" ...>Book</button>
</div>

<div class="tab-content" id="nav-tabContent">
    <div class="tab-pane fade show active" id="nav-all" ...>...</div>
    <div class="tab-pane fade" id="nav-journal" ...>...</div>
    <div class="tab-pane fade" id="nav-conference" ...>...</div>
    <div class="tab-pane fade" id="nav-book" ...>...</div>
</div>
```

### JavaScript 初始化

每個 Tab 的表格都會初始化 jQuery UI Sortable：

```javascript
// Only initialize sortable for type-specific tabs (NOT "All" tab)
initSortable('publicationsTableJournal', 'journal', 'nav-journal-tab');
initSortable('publicationsTableConference', 'conference', 'nav-conference-tab');
initSortable('publicationsTableBook', 'book', 'nav-book-tab');
```

### 拖曳排序邏輯

- 只有類型專屬的 Tab 支援拖曳排序
- 拖曳時只會重新排序該類型的出版物
- 其他類型的順序保持不變，避免交錯
- 儲存後會重新載入頁面，同步所有 Tab
- 使用 localStorage 記住當前 Tab，重新載入後自動回到原本的 Tab

## 優點

✅ **分類清晰**：每個類型獨立顯示，不會混淆

✅ **欄位優化**：每個 Tab 只顯示相關欄位，減少視覺雜訊

✅ **操作便捷**：快速切換 Tab，專注於特定類型

✅ **排序安全**：只能在類型專屬 Tab 中排序，避免不同類型交錯

✅ **視覺美觀**：現代化的 Tab 設計，符合 Bootstrap 風格

## 注意事項

⚠️ **「全部」Tab 不支援拖曳**：為了避免不同類型的出版物交錯，「全部」Tab 僅供查看

⚠️ **只能在類型 Tab 中排序**：請切換到 Journal、Conference 或 Book Tab 進行排序

⚠️ **拖曳後會重新載入**：為了同步所有 Tab 的順序，拖曳後頁面會自動重新載入

✅ **Tab 狀態會保存**：重新載入後會自動回到拖曳前的 Tab，不會跳回「全部」Tab

## 相關資源

- [Bootstrap Nav Tabs 文件](https://getbootstrap.com/docs/5.3/components/navs-tabs/)
- [jQuery UI Sortable 文件](https://jqueryui.com/sortable/)

