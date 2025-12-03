# Admin Panel 功能列表

## 📚 Publications 管理

### 基本功能
- ✅ 新增出版物（Journal、Conference、Book、Dissertation）
- ✅ 編輯出版物資訊
- ✅ 刪除出版物

### 🆕 Tab 分頁功能
- ✅ **全部** Tab：顯示所有類型的出版物（僅供查看）
- ✅ **Journal** Tab：只顯示 Journal，包含 Volume、Pages 欄位
- ✅ **Conference** Tab：只顯示 Conference，包含 Location 欄位
- ✅ **Book** Tab：只顯示 Book，包含 Publisher 欄位
- ✅ 每個 Tab 都有獨立的表格欄位設計
- ✅ 美觀的 Tab 樣式（藍色底線高亮）
- ℹ️ Dissertation 類型比較特別，不在 Admin 中管理

### 🆕 拖曳排序功能
- ✅ 拖曳手柄位於最左側（⋮⋮ 圖示）
- ✅ 即時視覺回饋（拖曳時顯示陰影和佔位符）
- ✅ 自動儲存順序到 JSON
- ✅ Journal、Conference、Book Tab 支援拖曳排序
- ✅ 「全部」Tab 不支援拖曳，避免不同類型交錯
- ✅ 拖曳後自動重新載入頁面同步所有 Tab
- ✅ 使用 localStorage 記住當前 Tab，重新載入後自動回到原本的 Tab
- ✅ 響應式設計（保持列寬度一致）

### 類型特定欄位
- **Journal**：Volume、Pages
- **Conference**：Location、Date
- **Book**：Editors、Publisher
- **Dissertation**：基本欄位

### API 端點
- `GET /api/publications` - 獲取所有出版物
- `POST /api/publications` - 新增出版物
- `PUT /api/publications/<id>` - 更新出版物
- `DELETE /api/publications/<id>` - 刪除出版物
- `POST /api/publications/reorder` - 重新排序（新增）

---

## 👥 Members 管理

### 基本功能
- ✅ 新增成員
- ✅ 編輯成員資訊
- ✅ 刪除成員
- ✅ 照片上傳與預覽
- ✅ 年份篩選（2025-2010）
- ✅ 狀態篩選（在學中/已畢業）

### 成員資訊
- 英文姓名（必填）
- 中文姓名（選填）
- 學位（MS/PhD）
- 年份
- 狀態（active/graduated）
- 照片（預設：pp.png）

### Contact Person
- 顯示聯絡人資訊
- 包含照片、Email、實驗室資訊

### API 端點
- `GET /api/members` - 獲取所有成員
- `POST /api/members` - 新增成員
- `PUT /api/members/<id>` - 更新成員
- `DELETE /api/members/<id>` - 刪除成員

---

## 📅 Events 管理

### 基本功能
- ✅ 新增活動
- ✅ 編輯活動資訊
- ✅ 刪除活動
- ✅ 活動照片上傳
- ✅ 卡片式網格顯示

### 活動資訊
- 標題
- 日期（YYYY-MM-DD）
- 顯示日期（例如：2024/01/15）
- 描述（選填）
- 分類（選填）
- 照片（必填）

### API 端點
- `GET /api/events` - 獲取所有活動
- `POST /api/events` - 新增活動
- `PUT /api/events/<id>` - 更新活動
- `DELETE /api/events/<id>` - 刪除活動

---

## 📁 檔案上傳

### 支援格式
- JPG、JPEG、PNG、GIF

### 檔案大小限制
- 最大 16MB

### 上傳路徑
- 成員照片：`/asset/member/`
- 活動照片：`/asset/event/`
- 一般照片：`/asset/general/`

### API 端點
- `POST /upload?type=member` - 上傳成員照片
- `POST /upload?type=event` - 上傳活動照片
- `POST /upload?type=general` - 上傳一般照片

---

## 🎨 使用者介面

### 設計特色
- ✅ Bootstrap 5.3.3 響應式設計
- ✅ Font Awesome 6.4.0 圖示
- ✅ jQuery 3.6.4 + jQuery UI 1.13.2
- ✅ 側邊欄導航
- ✅ 模態框表單
- ✅ 即時篩選
- ✅ 拖曳排序（Publications）

### 顏色主題
- 主色：藍色漸層 (#4e73df → #224abe)
- 成功：綠色 (#1cc88a)
- 警告：黃色 (#f6c23e)
- 危險：紅色 (#e74a3b)

---

## 🔧 技術架構

### 後端
- **Flask 3.0.0** - Web 框架
- **Werkzeug 3.0.1** - WSGI 工具
- **Python 3** - 程式語言

### 前端
- **Bootstrap 5.3.3** - UI 框架
- **jQuery 3.6.4** - JavaScript 函式庫
- **jQuery UI 1.13.2** - 拖曳排序
- **Font Awesome 6.4.0** - 圖示

### 資料儲存
- **JSON** - 資料格式
- **檔案系統** - 照片儲存

---

## 📊 儀表板

### 統計資訊
- 📚 Publications 總數
- 👥 Members 總數
- 🎓 已畢業人數
- 📅 Events 總數

### 快速連結
- 管理 Publications
- 管理 Members
- 管理 Events
- 查看前端網站

### Git 操作指南
- 顯示常用 Git 指令
- 推送變更到 GitHub

---

## 🚀 未來功能規劃

### 可能的增強功能
- [ ] Members 拖曳排序
- [ ] Events 拖曳排序
- [ ] 批次上傳照片
- [ ] 匯入/匯出 CSV
- [ ] 搜尋功能
- [ ] 資料備份/還原
- [ ] 使用者認證
- [ ] 操作歷史記錄
- [ ] 圖片裁切/編輯
- [ ] 多語言支援

---

## 📝 版本歷史

### v1.2.0 (2025-12-04)
- ✨ 新增 Publications Tab 分頁功能
- ✨ 每個類型獨立顯示，包含專屬欄位
- 🎨 優化 Tab 樣式設計
- 🔧 所有 Tab 都支援拖曳排序

### v1.1.0 (2025-12-04)
- ✨ 新增 Publications 拖曳排序功能
- ✨ 新增 `/api/publications/reorder` API
- 🎨 優化拖曳視覺效果
- 📚 新增 SORTABLE_GUIDE.md 文件

### v1.0.0 (2025-12-03)
- 🎉 初始版本
- ✨ Publications 管理
- ✨ Members 管理
- ✨ Events 管理
- ✨ 檔案上傳
- ✨ 儀表板

