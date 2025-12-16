# Catalog Navigation 自訂實作說明

## 📋 概述

取代 Bootstrap 的 scrollspy 功能，使用自訂 JavaScript 實現更穩定的目錄導航系統。

---

## ✅ 完成的功能

### 1. **平滑滾動跳轉**
- 點擊 `catalogIco` 按鈕時，平滑滾動到對應區域
- 滾動時間：600ms（可調整）
- 自動計算偏移量，避免被固定導航欄遮住

### 2. **自動監測當前區域**
- 滾動時自動檢測當前所在區域
- 動態更新對應按鈕的 `active` class
- 使用節流（throttle）優化性能

---

## 📂 檔案說明

### 1. **catalog-navigation.js**
自訂的目錄導航 JavaScript

**位置**：`/catalog-navigation.js`

**功能模組**：
- ✅ 點擊跳轉功能
- ✅ 滾動監測功能
- ✅ Active 狀態更新
- ✅ 節流優化

### 2. **professor/index.html**
已更新的教授個人頁面

**修改內容**：
- ✅ 引入 `catalog-navigation.js`
- ✅ 移除 Bootstrap scrollspy 屬性：
  - `data-bs-spy="scroll"`
  - `data-bs-target="#catalog"`
  - `data-bs-smooth-scroll="true"`
  - `tabindex="0"`

### 3. **test_catalog_navigation.html**
測試頁面

**位置**：`/test_catalog_navigation.html`

**用途**：獨立測試導航功能

---

## ⚙️ 配置參數

在 `catalog-navigation.js` 中可以調整以下參數：

```javascript
const config = {
  // 滾動偏移量（考慮固定導航欄的高度）
  scrollOffset: 120,
  
  // 平滑滾動的動畫時間（毫秒）
  scrollDuration: 600,
  
  // 滾動監測的節流時間（毫秒）
  throttleDelay: 100
};
```

### 參數說明

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `scrollOffset` | 120 | 滾動偏移量（px），避免內容被導航欄遮住 |
| `scrollDuration` | 600 | 平滑滾動動畫時間（ms） |
| `throttleDelay` | 100 | 滾動事件節流延遲（ms），降低 CPU 使用率 |

---

## 🔧 工作原理

### 1. **點擊跳轉**

```javascript
$('.catalogIco').on('click', function(e) {
  e.preventDefault(); // 阻止預設錨點跳轉
  
  const targetId = $(this).attr('href'); // 例如 "#Experience"
  const $target = $(targetId);
  
  // 計算目標位置（減去偏移量）
  const targetPosition = $target.offset().top - config.scrollOffset;
  
  // 平滑滾動
  $('html, body').animate({
    scrollTop: targetPosition
  }, config.scrollDuration);
  
  // 立即更新 active 狀態
  updateActiveButton(targetId);
});
```

### 2. **滾動監測**

```javascript
function detectCurrentSection() {
  const scrollPos = $(window).scrollTop() + config.scrollOffset + 50;
  
  const sections = ['#Research', '#Experience', '#Publications', '#Others'];
  let currentSection = sections[0];
  
  // 從上往下檢查，找到當前滾動到的區域
  for (let i = 0; i < sections.length; i++) {
    const $section = $(sections[i]);
    const sectionTop = $section.offset().top;
    
    if (scrollPos >= sectionTop) {
      currentSection = sections[i];
    }
  }
  
  updateActiveButton(currentSection);
}
```

### 3. **節流優化**

```javascript
function throttle(func, delay) {
  let lastCall = 0;
  return function(...args) {
    const now = new Date().getTime();
    if (now - lastCall < delay) {
      return; // 忽略過於頻繁的調用
    }
    lastCall = now;
    return func(...args);
  };
}

// 使用節流
$(window).on('scroll', throttle(detectCurrentSection, 100));
```

---

## 🧪 測試步驟

### 1. **測試頁面**
訪問：`http://localhost:8888/test_catalog_navigation.html`

**測試項目**：
- ✅ 點擊圓形按鈕是否平滑滾動
- ✅ 滾動時 active 狀態是否正確更新
- ✅ 跳轉後標題是否被遮住
- ✅ 性能是否流暢（無卡頓）

### 2. **實際頁面**
訪問：`http://localhost:8888/professor/`

**測試項目**：
- ✅ 4 個導航按鈕功能正常
- ✅ 手機版和桌面版都正常運作
- ✅ 與其他頁面元素無衝突

---

## 🎯 優勢對比

| 功能 | Bootstrap Scrollspy | 自訂實作 |
|------|---------------------|----------|
| 平滑滾動 | ❌ 有時失效 | ✅ 穩定可靠 |
| Active 更新 | ❌ 有 bug | ✅ 準確無誤 |
| 偏移量控制 | ⚠️ 複雜 | ✅ 簡單直觀 |
| 性能優化 | ⚠️ 一般 | ✅ 節流優化 |
| 可自訂性 | ❌ 受限 | ✅ 完全控制 |
| 調試能力 | ❌ 困難 | ✅ 內建調試 |

---

## 🐛 調試功能

如需啟用調試訊息，在 `catalog-navigation.js` 中取消註解：

```javascript
// 取消註解以啟用調試訊息
$(window).on('scroll', throttle(function() {
  const scrollPos = $(window).scrollTop();
  console.log('Scroll Position:', scrollPos);
  
  $('.catalogIco.active').each(function() {
    console.log('Active Section:', $(this).attr('href'));
  });
}, 500));
```

---

## 📝 注意事項

1. **jQuery 依賴**：需要先載入 jQuery
2. **載入順序**：`catalog-navigation.js` 必須在 `</body>` 前或使用 `$(document).ready()`
3. **區域 ID**：確保頁面中有對應的 `id="Research"` 等元素
4. **偏移量調整**：根據實際導航欄高度調整 `scrollOffset`

---

## 🚀 未來改進

- [ ] 支援 URL hash 同步（例如 `#Experience`）
- [ ] 支援鍵盤導航（上下鍵）
- [ ] 支援觸控手勢（左右滑動）
- [ ] 支援進度條顯示
- [ ] 支援自動隱藏/顯示導航

---

完成！現在你有一個穩定、高效的自訂目錄導航系統！🎉

