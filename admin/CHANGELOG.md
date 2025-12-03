# Admin Panel 更新日誌

## [v1.2.0] - 2025-12-04

### ✨ 新增功能

#### Publications Tab 分頁功能
- 新增 Bootstrap Nav Tabs 分頁介面
- 4 個 Tab：全部、Journal、Conference、Book
- 每個 Tab 顯示對應類型的出版物
- 每個 Tab 都有專屬的表格欄位設計
- Dissertation 類型比較特別，不在 Admin 中管理

#### Tab 專屬欄位
- **全部 Tab**：顯示所有欄位 + 類型標籤（僅供查看，不支援拖曳）
- **Journal Tab**：顯示 Volume、Pages 欄位
- **Conference Tab**：顯示 Location 欄位
- **Book Tab**：顯示 Publisher 欄位

#### 拖曳排序增強
- 只有類型專屬的 Tab 支援拖曳排序（Journal、Conference、Book）
- 「全部」Tab 不支援拖曳，避免不同類型交錯
- 拖曳時只會重新排序該類型的出版物，其他類型保持不變
- 拖曳後自動重新載入頁面同步所有 Tab
- 使用 localStorage 記住當前 Tab，重新載入後自動回到原本的 Tab

### 🎨 UI/UX 改進

#### Tab 樣式優化
- 現代化的 Tab 設計
- 藍色底線高亮選中的 Tab
- 懸停效果（藍色文字 + 底線）
- 每個 Tab 都有對應的 Font Awesome 圖示

#### 視覺效果
- 移除舊的下拉篩選器
- 更清晰的分類顯示
- 減少視覺雜訊

### 📚 文件更新
- 新增 `TABS_GUIDE.md` - Tab 分頁功能使用指南
- 更新 `README.md` - 添加 Tab 功能說明
- 更新 `FEATURES.md` - 更新功能列表
- 更新 `QUICK_START.md` - 更新快速開始指南

### 🔧 技術改進
- 重構 HTML 結構，使用 Bootstrap Tab 組件
- 更新 JavaScript，支援多個 sortable 表格
- 優化 CSS，添加 Tab 專屬樣式
- 改進拖曳排序邏輯，確保所有 Tab 同步

---

## [v1.1.0] - 2025-12-04

### ✨ 新增功能

#### Publications 拖曳排序
- 新增 jQuery UI Sortable 拖曳排序功能
- 拖曳手柄位於最左側（⋮⋮ 圖示）
- 即時視覺回饋（陰影、佔位符）
- 自動儲存順序到 JSON

#### 後端 API
- 新增 `POST /api/publications/reorder` 端點
- 支援重新排序出版物
- 自動驗證和儲存順序

### 🎨 UI/UX 改進
- 拖曳時顯示陰影效果
- 目標位置顯示灰色佔位符
- 拖曳手柄懸停效果
- 響應式設計，保持列寬度一致

### 📚 文件
- 新增 `SORTABLE_GUIDE.md` - 拖曳排序使用指南
- 新增 `test_sortable.html` - 拖曳功能測試頁面
- 更新 `README.md` - 添加拖曳排序說明

### 🔧 技術細節
- 使用 jQuery UI 1.13.2
- 自定義 helper 函數保持列寬度
- AJAX 自動儲存順序
- 篩選時自動停用拖曳

---

## [v1.0.0] - 2025-12-03

### 🎉 初始版本

#### Publications 管理
- 新增、編輯、刪除出版物
- 支援 4 種類型：Journal、Conference、Book、Dissertation
- 類型特定欄位（Volume、Pages、Location、Editors、Publisher）
- 類型篩選功能
- 作者高亮功能

#### Members 管理
- 新增、編輯、刪除成員
- 照片上傳與預覽
- 年份篩選（2025-2010）
- 狀態篩選（在學中/已畢業）
- Contact Person 資訊顯示
- 畢業狀態管理（畢業帽圖示）

#### Events 管理
- 新增、編輯、刪除活動
- 活動照片上傳
- 卡片式網格顯示
- 日期格式化

#### 檔案上傳
- 支援 JPG、PNG、GIF 格式
- 最大 16MB 檔案大小
- 照片預覽功能
- 安全檔名處理

#### 儀表板
- 統計資訊顯示
- 快速導航連結
- Git 操作指南
- 查看前端網站連結

#### 技術架構
- Flask 3.0.0 後端
- Bootstrap 5.3.3 前端
- jQuery 3.6.4
- Font Awesome 6.4.0
- JSON 資料儲存

#### 文件
- `README.md` - 完整使用說明
- `FEATURES.md` - 功能列表
- `QUICK_START.md` - 快速開始指南
- `requirements.txt` - Python 依賴
- `start_admin.sh` - 啟動腳本

---

## 統計資訊

### 程式碼統計
- **總行數**：約 2000+ 行
- **Python 文件**：1 個（app.py - 290 行）
- **HTML 模板**：5 個（約 1500 行）
- **文件**：6 個 Markdown 文件

### 功能統計
- **API 端點**：15 個
- **管理頁面**：4 個（Dashboard、Publications、Members、Events）
- **支援的資料類型**：3 個（Publications、Members、Events）
- **上傳類型**：3 個（member、event、general）

### 資料統計（當前）
- **Publications**：25 筆
  - Journal: 13 筆
  - Conference: 10 筆
  - Book: 2 筆
  - Dissertation: 0 筆
- **Members**：55 位
  - 在學中: 30 位
  - 已畢業: 25 位
- **Events**：8 個

---

## 未來計劃

### 短期計劃
- [ ] Members 拖曳排序
- [ ] Events 拖曳排序
- [ ] 批次操作（批次刪除、批次編輯）
- [ ] 搜尋功能

### 中期計劃
- [ ] 資料匯入/匯出（CSV、Excel）
- [ ] 圖片裁切/編輯功能
- [ ] 操作歷史記錄
- [ ] 資料備份/還原

### 長期計劃
- [ ] 使用者認證系統
- [ ] 權限管理
- [ ] 多語言支援
- [ ] API 文件（Swagger）
- [ ] 單元測試
- [ ] 部署指南（Docker）

---

## 貢獻者

- **開發者**：Augment Agent
- **專案**：Laboratory Website Admin Panel
- **授權**：MIT License

---

## 相關連結

- **前端網站**：http://localhost:3000
- **Admin Panel**：http://localhost:5000
- **GitHub**：https://github.com/paomllab-csie-ntust/paomllab-csie-ntust.github.io

