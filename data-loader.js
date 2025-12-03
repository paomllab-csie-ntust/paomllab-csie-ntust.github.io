/**
 * Data Loader - 從 JSON 文件載入資料並渲染到頁面
 */

// ==================== Publications ====================
function loadPublications() {
  fetch('../dataset/publications.json')
    .then(response => response.json())
    .then(data => {
      renderPublications(data.publications);
    })
    .catch(error => console.error('Error loading publications:', error));
}

function renderPublications(publications) {
  // 按類型分組
  const journals = publications.filter(p => p.type === 'journal');
  const conferences = publications.filter(p => p.type === 'conference');
  const books = publications.filter(p => p.type === 'book');
  const dissertations = publications.filter(p => p.type === 'dissertation');

  // 渲染 Journal
  const journalContainer = document.getElementById('nav-journal');
  if (journalContainer) {
    journalContainer.innerHTML = journals.map(pub => renderPublication(pub)).join('');
  }

  // 渲染 Conference
  const conferenceContainer = document.getElementById('nav-conference');
  if (conferenceContainer) {
    conferenceContainer.innerHTML = conferences.map(pub => renderPublication(pub)).join('');
  }

  // 渲染 Book
  const bookContainer = document.getElementById('nav-book');
  if (bookContainer) {
    bookContainer.innerHTML = books.map(pub => renderPublication(pub)).join('');
  }

  // 渲染 Dissertation
  // Note: Dissertation content is static in professor/index.html, so we skip rendering here
  // to avoid overwriting the static content
  const dissertationContainer = document.getElementById('nav-dissertation');
  if (dissertationContainer && dissertations.length > 0) {
    dissertationContainer.innerHTML = dissertations.map(pub => renderPublication(pub)).join('');
  }
}

function renderPublication(pub) {
  let html = '<div class="bookmark mb-1"></div><p class="mb-4 mb-md-5"><font face="Times New Roman">';

  // 處理作者（高亮特定作者）
  // 支援 ", " 和 " and " 兩種分隔符
  let authorsList = [];
  let authorsStr = pub.authors;

  // 先按 " and " 分割
  const andParts = authorsStr.split(' and ');
  andParts.forEach(part => {
    // 再按 ", " 分割
    const commaParts = part.split(', ');
    authorsList = authorsList.concat(commaParts);
  });

  // 高亮特定作者並重新組合
  let processedAuthors = [];
  for (let i = 0; i < authorsList.length; i++) {
    const author = authorsList[i].trim();
    if (author === pub.highlight_author) {
      processedAuthors.push(`<b class="text-primary">${author}</b>`);
    } else {
      processedAuthors.push(author);
    }
  }

  // 重新組合作者字串（保持原始格式）
  const authors = pub.authors.replace(pub.highlight_author, `<b class="text-primary">${pub.highlight_author}</b>`);

  html += `${authors}.<br>`;
  html += `<span class="fw-bolder m-0">${pub.title}</span>,<br>`;
  html += `<i>${pub.venue}</i>,`;
  
  if (pub.type === 'journal') {
    // Journal 格式
    if (pub.volume) html += ` Vol. ${pub.volume}:`;
    if (pub.pages) html += ` pp. ${pub.pages},`;
    html += ` ${pub.year}`;
  } else if (pub.type === 'conference') {
    // Conference 格式
    html += `<br>`;
    if (pub.location) html += `${pub.location}, `;
    if (pub.date) html += `${pub.date}.`;
  } else if (pub.type === 'book') {
    // Book 格式
    html += `<br>`;
    if (pub.editors) html += `${pub.editors}, `;
    if (pub.publisher) html += `${pub.publisher}, `;
    html += `${pub.year}.`;
  }

  html += '</font></p>';
  return html;
}

// ==================== Members ====================
function loadMembers() {
  fetch('../dataset/members.json')
    .then(response => response.json())
    .then(data => {
      renderMembers(data);
    })
    .catch(error => console.error('Error loading members:', error));
}

function renderMembers(data) {
  // 更新聯絡人資訊
  updateContactPerson(data.contact_person, data.lab_info);
  
  // 按年份分組成員
  const membersByYear = {};
  data.members.forEach(member => {
    if (!membersByYear[member.year]) {
      membersByYear[member.year] = [];
    }
    membersByYear[member.year].push(member);
  });
  
  // 渲染成員列表
  const membersContainer = document.getElementById('members-container');
  if (membersContainer) {
    const years = Object.keys(membersByYear).sort((a, b) => b - a); // 降序排列
    membersContainer.innerHTML = years.map(year => {
      return renderMemberYear(year, membersByYear[year]);
    }).join('');
  }
}

function updateContactPerson(contactPerson, labInfo) {
  // 更新聯絡人照片
  const contactPhoto = document.getElementById('contact-person-photo');
  if (contactPhoto) {
    contactPhoto.src = `../${contactPerson.photo}`;
  }
  
  // 更新聯絡人姓名
  const contactNameElements = document.querySelectorAll('.contact-person-name');
  contactNameElements.forEach(el => {
    el.textContent = contactPerson.name;
  });
  
  // 更新聯絡人 Email
  const contactEmailElements = document.querySelectorAll('.contact-person-email');
  contactEmailElements.forEach(el => {
    el.textContent = contactPerson.email;
    el.href = `mailto:${contactPerson.email}`;
  });
}

function renderMemberYear(year, members) {
  let html = `<h4 class="fw-bolder my-2">${year}</h4>`;
  html += '<div class="ps-2 ps-md-3"><div class="border-secondary border-start border-4 pb-2"><div class="row m-0">';
  
  members.forEach(member => {
    html += renderMember(member);
  });
  
  html += '</div></div></div>';
  return html;
}

function renderMember(member) {
  const graduatedIcon = member.status === 'graduated' ? '<i class="fa-solid fa-graduation-cap"></i>' : '';
  const displayName = member.name_zh || member.name;
  
  return `
    <div class="col-6 col-md-4 col-lg-3 col-xl-2">
      <div class="div-square mt-3">
        <img class="div-square-content img-fluid hwAuto rounded-circle my-border" src="../${member.photo}">
      </div>
      <h4 class="mt-1 mb-0 text-center">${displayName}</h4>
      <h4 class="fw-bolder mt-0 mb-3 text-center text-primary">${member.degree}${graduatedIcon}</h4>
    </div>
  `;
}

// ==================== Events ====================
function loadEvents() {
  fetch('../dataset/events.json')
    .then(response => response.json())
    .then(data => {
      renderEvents(data.events);
    })
    .catch(error => console.error('Error loading events:', error));
}

function renderEvents(events) {
  // 按日期降序排列
  events.sort((a, b) => new Date(b.date) - new Date(a.date));

  const eventsContainer = document.querySelector('.waterfall');
  if (eventsContainer) {
    eventsContainer.innerHTML = events.map(event => renderEvent(event)).join('');
  }
}

function renderEvent(event) {
  return `
    <div class="waterfall-item mb-2">
      <img class="waterfall-img rounded-top-4" src="../${event.photo}">
      <div class="p-1 p-md-2 border border-2 border-top-0 rounded-bottom-4">
        <h5 class="fw-bolder text-primary m-0">${event.title}</h5>
        <p class="fw-bolder m-0">${event.date_display}</p>
      </div>
    </div>
  `;
}

// ==================== 初始化 ====================
document.addEventListener('DOMContentLoaded', function() {
  // 根據當前頁面載入對應的資料
  const currentPath = window.location.pathname;

  if (currentPath.includes('/professor/')) {
    loadPublications();
  } else if (currentPath.includes('/laboratory/')) {
    loadMembers();
  } else if (currentPath.includes('/events/')) {
    loadEvents();
  }
});

