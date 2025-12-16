/**
 * Catalog Navigation System
 * 自訂的目錄導航系統，取代 Bootstrap 的 scrollspy
 * 
 * 功能：
 * 1. 點擊 catalogIco 時平滑滾動到對應區域
 * 2. 滾動時自動監測當前區域，並更新 active class
 */

$(document).ready(function() {

  // ==================== 配置 ====================
  const config = {
    // 滾動監測的節流時間（毫秒）
    throttleDelay: 100,
    // 滾動結束判定時間（毫秒）
    scrollEndDelay: 150,
    // 桌面版偏移量（>= 768px）
    desktopOffset: 80,
    // 手機版使用 catalog-out 的高度
    getMobileOffset: function() {
      const catalogOutHeight = $('#catalog-out').outerHeight()+60 || 0;
      return catalogOutHeight;
    }
  };

  // 點擊跳轉標記（用於暫停滾動監測）
  let isClickJumping = false;
  let scrollEndTimer = null;

  /**
   * 根據螢幕尺寸獲取當前的 scrollOffset
   */
  function getScrollOffset() {
    // Bootstrap 的 md 斷點是 768px
    if ($(window).width() >= 768) {
      return config.desktopOffset; // 桌面版：80px
    } else {
      return config.getMobileOffset(); // 手機版：catalog-out 的高度
    }
  }

  // ==================== 1. 點擊跳轉功能 ====================

  /**
   * 快速跳轉到目標區域（無動畫）
   */
  $('.catalogIco').on('click', function(e) {
    e.preventDefault(); // 阻止預設的錨點跳轉

    const targetId = $(this).attr('href'); // 例如 "#Experience"
    const $target = $(targetId);

    if ($target.length) {
      // 設定點擊跳轉標記，暫停滾動監測
      isClickJumping = true;

      // 立即更新 active 狀態
      updateActiveButton(targetId);

      // 計算目標位置（減去動態偏移量）
      const scrollOffset = getScrollOffset();
      const targetPosition = $target.offset().top - scrollOffset;

      // 直接跳轉（無動畫）
      $(window).scrollTop(targetPosition);

      // 注意：不在這裡恢復監測，而是在滾動結束後恢復
    }
  });

  // ==================== 2. 滾動監測功能 ====================
  
  /**
   * 更新 active 按鈕
   */
  function updateActiveButton(activeId) {
    // 移除所有 active class
    $('.catalogIco').removeClass('active');
    
    // 為對應的按鈕加上 active class
    $(`.catalogIco[href="${activeId}"]`).addClass('active');
  }

  /**
   * 檢測當前滾動位置對應的區域
   */
  function detectCurrentSection() {
    const scrollOffset = getScrollOffset();
    const scrollPos = $(window).scrollTop() + scrollOffset + 50;
    
    // 所有區域的 ID
    const sections = ['#Research', '#Experience', '#Publications', '#Others'];
    
    // 從下往上檢查，找到第一個已經滾動過的區域
    let currentSection = sections[0]; // 預設為第一個
    
    for (let i = 0; i < sections.length; i++) {
      const $section = $(sections[i]);
      
      if ($section.length) {
        const sectionTop = $section.offset().top;
        
        // 如果滾動位置已經超過這個區域的頂部
        if (scrollPos >= sectionTop) {
          currentSection = sections[i];
        }
      }
    }
    
    // 更新 active 狀態
    updateActiveButton(currentSection);
  }

  /**
   * 節流函數 - 限制函數執行頻率
   */
  function throttle(func, delay) {
    let lastCall = 0;
    return function(...args) {
      const now = new Date().getTime();
      if (now - lastCall < delay) {
        return;
      }
      lastCall = now;
      return func(...args);
    };
  }

  // ==================== 3. 事件監聽 ====================

  // 滾動事件（使用節流優化性能）
  $(window).on('scroll', throttle(function() {
    // 如果正在點擊跳轉，檢測滾動是否結束
    if (isClickJumping) {
      // 清除之前的計時器
      if (scrollEndTimer) {
        clearTimeout(scrollEndTimer);
      }

      // 設定新的計時器：如果 150ms 內沒有新的滾動事件，視為滾動結束
      scrollEndTimer = setTimeout(function() {
        isClickJumping = false;
        scrollEndTimer = null;
        // 滾動結束後立即檢測一次當前區域
        detectCurrentSection();
      }, config.scrollEndDelay);

      return; // 滾動期間不執行監測
    }

    // 正常滾動時的監測
    detectCurrentSection();
  }, config.throttleDelay));

  // 頁面載入時執行一次（設定初始 active 狀態）
  detectCurrentSection();

  // 視窗大小改變時重新檢測（因為區域位置可能改變）
  $(window).on('resize', throttle(function() {
    detectCurrentSection();
  }, config.throttleDelay));

  // ==================== 4. 調試功能（可選） ====================
  
  // 取消註解以啟用調試訊息
  /*
  $(window).on('scroll', throttle(function() {
    const scrollPos = $(window).scrollTop();
    console.log('Scroll Position:', scrollPos);
    
    $('.catalogIco.active').each(function() {
      console.log('Active Section:', $(this).attr('href'));
    });
  }, 500));
  */

});

