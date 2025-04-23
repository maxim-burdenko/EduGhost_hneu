const warningSvg = '<svg class="profile__form-icon profile__form-icon--hidden" xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="m40-120 440-760 440 760H40Zm138-80h604L480-720 178-200Zm302-40q17 0 28.5-11.5T520-280q0-17-11.5-28.5T480-320q-17 0-28.5 11.5T440-280q0 17 11.5 28.5T480-240Zm-40-120h80v-200h-80v200Zm40-100Z"/></svg>';

const regexPersonalSchedule = /^http:\/\/www\.rozklad\.hneu\.edu\.ua\/schedule\/schedule\?group=\d{5}&student=\d{6}$/;
// const regexAttendanceLink = /^https:\/\/pns\.hneu\.edu\.ua\/mod\/attendance\/view\.php\?id=\d{6}$/;
// const regexZoomLink = /^https:\/\/us02web\.zoom\.us\/j\/\d{11}\?pwd=.+$/;

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function generateLinks() {
  const nodeLinks = document.querySelector('.data__items');
  nodeLinks.innerHTML = '';
  
  const editSvg = '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M200-200h57l391-391-57-57-391 391v57Zm-80 80v-170l528-527q12-11 26.5-17t30.5-6q16 0 31 6t26 18l55 56q12 11 17.5 26t5.5 30q0 16-5.5 30.5T817-647L290-120H120Zm640-584-56-56 56 56Zm-141 85-28-29 57 57-29-28Z"/></svg>';

  const deleteSvg = '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/></svg>';

  let data = await eel.get_links()();

  if (!data){nodeLinks.innerHTML='Ще не додано пар. Додати пари можна на вкладці "Посилання"'}

  for(const lesson in data){
    const li = document.createElement('li');
    li.classList.add('data__item');

    const h2 = document.createElement('h2');
    h2.classList.add('data__item-name');
    h2.textContent = lesson;

    const btnContainer = document.createElement('div');
    btnContainer.classList.add('data__item-btns');

    const editBtn = document.createElement('button');
    editBtn.classList.add('data__item-btn', 'data__item-btn-edit');
    editBtn.type = 'button';
    editBtn.innerHTML = editSvg;

    const deleteBtn = document.createElement('button');
    deleteBtn.classList.add('data__item-btn', 'data__item-btn-delete');
    deleteBtn.type = 'button';
    deleteBtn.innerHTML = deleteSvg;

    btnContainer.appendChild(editBtn);
    btnContainer.appendChild(deleteBtn);


    li.appendChild(h2);
    li.appendChild(btnContainer);

    nodeLinks.appendChild(li)

    editBtn.addEventListener('click', () => editLesson(lesson, data[lesson]))
    deleteBtn.addEventListener('click', () => deleteLesson(lesson, li))
  }
}

async function deleteLesson(lesson, element) {
  const userResponse = confirm(`Ви впевнені що хочите видалити ${lesson}?`);
  
  if (userResponse) {
    await eel.delete_lesson(lesson)();
    sendMessageToUser(`${lesson} було видалено`);
    element.remove();
  }
}

async function editLesson(lesson, lessonData) {
  const tabs = document.querySelectorAll('.tab')
  const sections = document.querySelectorAll('section')

  const tabLinks = document.querySelector('#tab-links');
  const sectionLinks = document.querySelector('#section-links')

  tabs.forEach(tab=>tab.classList.remove('active'));
  sections.forEach(section=>section.classList.add('section-hidden'));

  tabLinks.classList.add('active');
  sectionLinks.classList.remove('section-hidden');

  const nameField = document.getElementById('links-name');
  nameField.value = lesson;
  nameField.disabled = true;

  // Заполняем поля для лекции
  document.getElementById('links-zoom-lecture').value = lessonData.lecture.zoom || '';
  document.getElementById('links-attendance-lecture').value = lessonData.lecture.visiting || '';

  // Заполняем поля для практики
  document.getElementById('links-zoom-practice').value = lessonData.practice.zoom || '';
  document.getElementById('links-attendance-practice').value = lessonData.practice.visiting || '';
  
  // Заполняем поля для лабораторной работы
  document.getElementById('links-zoom-laboratory').value = lessonData.laboratory.zoom || '';
  document.getElementById('links-attendance-laboratory').value = lessonData.laboratory.visiting || '';

}

async function removeMessage(messageBox, timeOut) {
  messageBox.style.opacity = '1';  
  messageBox.classList.remove('fade-in');
  await new Promise(resolve => setTimeout(resolve, timeOut));
  messageBox.classList.add('fade-out');
  messageBox.style.removeProperty('opacity');
  await new Promise(resolve => setTimeout(resolve, 2000));
  messageBox.remove();
}

eel.expose(sendMessageToUser);
function sendMessageToUser(message, timeOut = 3000, unicId = undefined) {
  const containerMessages = document.querySelector('.messages');
  const closeSvg = '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/></svg>';

  const messageBox = document.createElement('div');
  messageBox.classList.add('message', 'active');
  messageBox.innerHTML = message;

  if (unicId) {messageBox.id = unicId};

  const messageBoxCloseBtn = document.createElement('button');
  messageBoxCloseBtn.classList.add('message-close');
  messageBoxCloseBtn.type = 'button';
  messageBoxCloseBtn.innerHTML = closeSvg;

  messageBox.appendChild(messageBoxCloseBtn);
  containerMessages?.appendChild(messageBox);

  messageBoxCloseBtn.addEventListener('click', function() {
    messageBox.remove();
  });

  new Promise(resolve => setTimeout(resolve, 4000));
  removeMessage(messageBox, timeOut);
}

eel.expose(changeStatus);
function changeStatus(newStr, color) {
  const icon = document.querySelector('.status__icon');
  const text = document.querySelector('.status__text');

  icon.style.backgroundColor = color;
  text.textContent = newStr;
}


function changeTab() {
  const tabs = document.querySelectorAll('.tab')
  const contents = document.querySelectorAll('.section')

  tabs.forEach((tab, index)=>{
    tab.addEventListener('click', function () {
      const formLinks = document.querySelector('.links__form');
      formLinks.reset();
      const nameField = document.getElementById('links-name');
      nameField.disabled = false;

      tabs.forEach(tab => tab.classList.remove('active'));
      contents.forEach(content=> content.classList.add('section-hidden'));

      tab.classList.add('active');
      contents[index].classList.remove('section-hidden');
    });
  });
};

function getPersonalData() {
  const profileForm = document.querySelector('.profile__form');

  profileForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    const errorBlockUrl = document.getElementById('profile-link-error-text');
    const iconUrl = document.getElementById('profile-link-error-icon');


    const formData = new FormData(event.target);
    const url = formData.get("profile-link");
    const check_exist_url = await eel.get_personal_schedule_url()();

    if (!regexPersonalSchedule.test(url) && !check_exist_url){      
      iconUrl.classList.remove('profile__form-icon--hidden');
      errorBlockUrl.textContent = 'посилання не вірного формату. має бути щось таке: http://www.rozklad.hneu.edu.ua/schedule/schedule?group=12345&student=123456';
      sendMessageToUser('Інформацію не було додано');
      profileForm.reset();
      return
    }


    const login = formData.get("profile-login");
    const password = formData.get("profile-password");

    const autorun = formData.get("profile-autorun")
    const shutdown = formData.get("profile-shutdown")
    let promises = [];

    if (url) {
      promises.push(eel.set_personal_schedule_url(url)());
      errorBlockUrl.textContent = '';
      iconUrl.classList.add('profile__form-icon--hidden');

      sendMessageToUser('Посилання було додано')
    }
    if (login) {
      promises.push(eel.set_pns_login(login)());
      sendMessageToUser('Логін до PNS було додано')
    }
    if (password) {
      promises.push(eel.set_pns_password(password)());
      sendMessageToUser('Пароль до PNS було додано')
    }

    if (autorun) {
      promises.push(eel.set_autorun_value(true)());
      sendMessageToUser('Було увімкненно автозавантаження')
    }else{
      promises.push(eel.set_autorun_value(false)());
      sendMessageToUser('Було вимкнено автозавантаження')
    }

    if (shutdown){
      promises.push(eel.set_shutdown_value(true)());
      sendMessageToUser('Було увімкненно автозавершення')
    }else{
      promises.push(eel.set_shutdown_value(false)());
      sendMessageToUser('Було вимкнено автозавершення')
    }

    if (promises.length > 0) {
      await Promise.all(promises);
    }

    getSetCurrentPersonalData();
    profileForm.reset();
  });
}

async function getSetCurrentPersonalData() {
  let link =  document.querySelector('.profile__check-rozklad');
  let login = document.querySelector('.profile__check-login');
  let password = document.querySelector('.profile__check-password');
  let autorun = document.querySelector('#profile-autorun');
  let shutdown = document.querySelector('#profile-shutdown');

  const successSvg = '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="m424-296 282-282-56-56-226 226-114-114-56 56 170 170Zm56 216q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q134 0 227-93t93-227q0-134-93-227t-227-93q-134 0-227 93t-93 227q0 134 93 227t227 93Zm0-320Z"/></svg>';

  const get_url = await eel.get_personal_schedule_url()();
  const get_login = await eel.get_pns_login()();
  const check_pwd = await eel.check_password()();

  const check_autorun = await eel.check_autorun_py()();
  const check_shutdown = await eel.check_shutdown_py()();

  if (get_url){
    link.innerHTML = successSvg + " " + get_url;
    link.href = get_url;
  }else{
    link.innerHTML = 'особистого посилання не було додано'
    link.href = "https:\\";
  }

  if (get_login) {
    login.innerHTML = successSvg + " " + get_login;
  }else{
    login.innerHTML = warningSvg + " поточного логіну немає";
  }

  if(check_pwd){
    password.innerHTML = successSvg + " Пароль збережений";
  }else{
    password.innerHTML = warningSvg + " поточного паролю немає";
  }

  if(check_autorun){
    autorun.checked = true;
  }else{
    autorun.checked = false;
  }

  if(check_shutdown){
    shutdown.checked = true;
  }else{
    shutdown.checked = false;
  }
}

async function addLessonToList() {
  const addLinkForm = document.querySelector('.links__form');

  addLinkForm?.addEventListener('submit', async function(event) {
    event.preventDefault();

    const nameField = document.getElementById('links-name');
    nameField.disabled = false;

    const formData = new FormData(event.target);

    const lessonName = formData.get('links-name');
    const zoomLecture = formData.get("links-zoom-lecture") || "";
    const attendanceLecture = formData.get("links-attendance-lecture") || "";
    const zoomPractice = formData.get("links-zoom-practice") || "";
    const attendancePractice = formData.get("links-attendance-practice") || "";
    const zoomLaboratory = formData.get("links-zoom-laboratory") || "";
    const attendanceLaboratory = formData.get("links-attendance-laboratory") || "";

    const regexAttendanceLink = /^https:\/\/pns\.hneu\.edu\.ua\/mod\/attendance\/view\.php\?id=\d{6}$/;
    const regexZoomLink = /^https:\/\/us02web\.zoom\.us\/j\/\d{11}\?pwd=.+$/;

    // Валидация
    const fieldsToValidate = [
      { value: zoomLecture, regex: regexZoomLink, name: 'Zoom, лекція' },
      { value: attendanceLecture, regex: regexAttendanceLink, name: 'Відмітка, лекція' },
      { value: zoomPractice, regex: regexZoomLink, name: 'Zoom, практична' },
      { value: attendancePractice, regex: regexAttendanceLink, name: 'Відмітка, практична' },
      { value: zoomLaboratory, regex: regexZoomLink, name: 'Zoom, лабораторна' },
      { value: attendanceLaboratory, regex: regexAttendanceLink, name: 'Відмітка, лабораторна' }
    ];

    for (let field of fieldsToValidate) {
      if (field.value.trim() !== "" && !field.regex.test(field.value)) {
        sendMessageToUser(`Поле "${field.name}" має неправильний формат.`);
        return; 
      }
    }

    const data = {
      [lessonName]: {
        lecture: {
          visiting: attendanceLecture,
          zoom: zoomLecture
        },
        practice: {
          visiting: attendancePractice,
          zoom: zoomPractice
        },
        laboratory: {
          visiting: attendanceLaboratory,
          zoom: zoomLaboratory
        }
      }
    };

    await eel.insert_link(data)();
    event.target.reset();
    sendMessageToUser(`"${lessonName}" було додано до списку`);
    generateLinks();
  });
}

async function startScript() {
  const url = await eel.get_personal_schedule_url()();
  const login = await eel.get_pns_login()();
  const pass = await eel.check_password()();
  const links = await eel.get_links()();

  if (!url) {
    alert('Немає особистого розкладу\nВідміна запуску...');
    sendMessageToUser('Додати особисте посилання можна на вкладці "Профіль"');
    return
  }

  if((!login && !links) || (!pass && !links)){
    alert('Немає посилань та особистого профілю ХНЕУ\nВідміна запуску...');
    sendMessageToUser('Додати логін та пароль можна на вкладці "Профіль"\nа також додати посилання на вкладці "Посилання"');
    return
  }

  if(!login){
    sendMessageToUser('Увага, логіна немає, проставляння відвідування неможливе');
  }

  if(!pass){
    sendMessageToUser('Увага, пароля немає, проставляння відвідування неможливе');
  }

  if(!links){
    sendMessageToUser('Увага, посилань немає. Заходити на Zoom-зустрічі неможливо');
  }

  changeStatus('в процесі', '#fcfcfc')
  sendMessageToUser('Спроба запуску скрипта...');
  await eel.start_script()();
}

async function startScriptAuto() {
  const isAutorun = await eel.check_autorun_py()();
  let countdown = 15;

  if (isAutorun){
    sessionStorage.setItem('runNow', 'true'); // Для отслеживания попытки прервать автозапуск
    sendMessageToUser('Увімкнено автозапуск скрипта');
    sendMessageToUser('Скрипт буде запущено через <span id="timer">15</span> секунд', 15000, 'message-timer');

    changeStatus('в процесі', '#fcfcfc')

    const timerElement = document.querySelector('#timer');
    let timer = setInterval(async () => {
      timerElement.textContent = countdown;
      countdown--;

      const stopAutorun = sessionStorage.getItem('stopAutorun') === 'true';
      if (stopAutorun) {
        const messageTimer = document.getElementById('message-timer');
        sendMessageToUser('Було прервано автозапуск.')

        removeMessage(messageTimer, 2000);
        changeStatus('не активний', '#ff2d15');

        clearInterval(timer);
        return
      }

      if (countdown < 0) {
        clearInterval(timer);
        sendMessageToUser('Спроба запуску скрипта...');
        await eel.start_script()();
      }
    }, 1000);
  }
}

async function generateCustomSchedule(){
  const container = document.querySelector('.custom__form-items');
  const details = container?.querySelectorAll('.custom__form-details')
  let days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
  schedule = {};

  for (let dayIndex = 0; dayIndex < details.length; dayIndex++) {
    const detail = details[dayIndex];
    const boxes = detail?.querySelectorAll('.custom__forn-box');
  
    const dayData = getDataCustomSchedule(boxes, dayIndex, days);
  
    if (!dayData || dayData.length === 0) {
      console.debug(`[Info]: данных на ${days[dayIndex]} не было, скипаем`);
      continue;
    }
  
    const dayName = days[dayIndex];
    const capitalizedDay = dayName.charAt(0).toUpperCase() + dayName.slice(1);
  
    schedule[capitalizedDay] = dayData;
  }
  

  // закинуть в питон
  await eel.update_custom_schedule(schedule)();
}

function getDataCustomSchedule(boxes, dayIndex, days) {

  data = [];

  for (let index = 0; index < boxes.length; index++) {
    const box = boxes[index];
    
    let mask_subject = `custom-${days[dayIndex]}-subject-${index + 1}`;
    let mask_type = `custom-${days[dayIndex]}-type-${index + 1}`;
    let mask_start = `custom-${days[dayIndex]}-start-${index + 1}`;
    let mask_end = `custom-${days[dayIndex]}-end-${index + 1}`;
  
    const inputSubject = box?.querySelector(`#${mask_subject}`)?.value;
    const inputType = box?.querySelector(`#${mask_type}`)?.value;
    const inputStart = box?.querySelector(`#${mask_start}`)?.value;
    const inputEnd = box?.querySelector(`#${mask_end}`)?.value;
  
    if (!inputSubject || !inputType || !inputStart || !inputEnd) {
      console.debug("[Info]: пустой блок, скипаем");
      continue;
    }
  
    const dict = {
      subject: inputSubject,
      type: inputType,
      start: inputStart,
      end: inputEnd
    };
  
    data.push(dict);
  }

  return data
}

document.getElementById('custom-send-btn')?.addEventListener('click', generateCustomSchedule);

document.querySelector('.data__header-btn--start')?.addEventListener('click', async function () {
  const runNow = sessionStorage.getItem('runNow') === 'true';

  if (runNow){
    sessionStorage.setItem('stopAutorun', 'true');
  }

  startScript();
  await sleep(1000);
});

document.querySelector('.data__header-btn--stop')?.addEventListener('click', async function () {
  const runNow = sessionStorage.getItem('runNow') === 'true';

  if (runNow){
    sessionStorage.setItem('stopAutorun', 'true');
    return
  }
})

generateLinks();
changeTab();
getPersonalData();
getSetCurrentPersonalData();
addLessonToList();

startScriptAuto();