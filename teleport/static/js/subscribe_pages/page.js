function timer() {
  let strip = document.querySelector('.timer-block .timer-progress'),
    sec = document.querySelector('.timer-block .sec'),
    min = document.querySelector('.timer-content .time'),
    sec_val,
    min_val,
    time;

  let page_slug = document.querySelector('input[name=page_slug]').value,
    page_options = JSON.parse(localStorage.getItem(`page_${ page_slug }_timer`)),
    timer_time;

  if (page_options) {
    timer_time = page_options.timer_time
  }

  if (timer_time) {
    sec_val = timer_time
  } else {
    sec_val = document.getElementById('timer-time').getAttribute('value')
  }

  min_val = `<span id="timer-minutes">${
    Math.floor(sec_val / 60) < 10 ?
      '0' + Math.floor(sec_val / 60)
      :
      Math.floor(sec_val / 60)
  }</span> : <span id="timer-seconds">${
    Math.floor(sec_val % 60) < 10 ?
      '0' + Math.floor(sec_val % 60)
      :
      Math.floor(sec_val % 60) }</span>`
  sec.innerHTML = sec_val
  min.innerHTML = min_val


  let display = document.querySelector('.timer-block .sec'),
    timeLeft = parseInt(display.innerHTML)

  setInterval(function () {
    if (--timeLeft >= 0) {

      time = `<span id="timer-minutes">${
        Math.floor(timeLeft / 60) < 10 ?
          '0' + Math.floor(timeLeft / 60)
          :
          Math.floor(timeLeft / 60)
      }</span> : <span id="timer-seconds">${
        Math.floor(timeLeft % 60) < 10 ?
          '0' + Math.floor(timeLeft % 60)
          :
          Math.floor(timeLeft % 60) }</span>`

      let a = sec_val - timeLeft,
        b = sec_val - a,
        c = sec_val * .01,
        d = b / c + '%',
        e = 'calc(' + d + ' - 8px)'

      localStorage.setItem(`page_${ page_slug }_timer`, JSON.stringify({ timer_time: timeLeft }))
      min.innerHTML = time
      strip.style.width = e
    } else {
      // по истичению таймера
    }
  }, 1000)
}

if (document.querySelector('.timer')) {
  timer()
}

// console.log(document.querySelector('main').classList[0])

// switch (document.querySelector('main').classList[0]) {
//   case 'profile-page': {
//     document.getElementById('go-subscribe').addEventListener('click', (e) => {
//       document.getElementById("form-block1").style.display = "none";
//       document.getElementById("form-block2").style.display = "block";
//       e.preventDefault()
//       document.getElementById('modal-return-back').classList.add('open')
//       bodyFixPosition()
//       setTimeout(async () => {
//         bodyUnfixPosition()
//         document.getElementById('modal-return-back').classList.remove('open')
//         // window.open('https://vk.com/')
//         // window.location.href = '/check-subscribe'
//       }, 1000)
//     })
//     document.getElementById('subscribed-check').addEventListener('click', (e) => {
//       e.preventDefault()
//       document.getElementById('modal-loading').classList.add('open')
//       bodyFixPosition()
//       setTimeout(() => {
//         bodyUnfixPosition()
//         document.getElementById('modal-loading').classList.remove('open')
//         // window.location.pathname = '/check-subscribe'
//       }, 3000)
//     })
//     document.getElementById('already-subscribe').addEventListener('click', (e) => {
//       document.getElementById("form-block1").style.display = "none";
//       document.getElementById("form-block2").style.display = "block";
//       e.preventDefault()
//     })
//     break;
//   }
//   case 'promo-page': {
//     document.getElementById('next-step').addEventListener('click', (e) => {
//       // e.preventDefault()
//       // window.location.pathname = '/check-subscribe'
//     })
//     break;
//   }
// }

// console.log(document.getElementById('subscribed-check'))


function bodyFixPosition() {

  setTimeout(function () {
    /* Ставим необходимую задержку, чтобы не было «конфликта» в случае, если функция фиксации вызывается сразу после расфиксации (расфиксация отменяет действия расфиксации из-за одновременного действия) */

    if (!document.body.hasAttribute('data-body-scroll-fix')) {

      // Получаем позицию прокрутки
      let scrollPosition = window.pageYOffset || document.documentElement.scrollTop

      // Ставим нужные стили
      document.body.setAttribute('data-body-scroll-fix', scrollPosition) // Cтавим атрибут со значением прокрутки
      document.body.style.overflow = 'hidden'
      document.body.style.position = 'fixed'
      document.body.style.top = '-' + scrollPosition + 'px'
      document.body.style.left = '0'
      document.body.style.width = '100%'

    }

  }, 15) /* Можно задержку ещё меньше, но у меня работало хорошо именно с этим значением на всех устройствах и браузерах */

}

// 2. Расфиксация <body>
function bodyUnfixPosition() {

  if (document.body.hasAttribute('data-body-scroll-fix')) {

    // Получаем позицию прокрутки из атрибута
    let scrollPosition = document.body.getAttribute('data-body-scroll-fix')

    // Удаляем атрибут
    document.body.removeAttribute('data-body-scroll-fix')

    // Удаляем ненужные стили
    document.body.style.overflow = ''
    document.body.style.position = ''
    document.body.style.top = ''
    document.body.style.left = ''
    document.body.style.width = ''

    // Прокручиваем страницу на полученное из атрибута значение
    window.scroll(0, scrollPosition)

  }

}

// if ($('.single_page').val() === 'true'){
//     window.location.replace($("#next-step").attr('href'));
//     }

$(() => {
  if ($('h4.user-title').first().text()) {
    $.ajax({
      type: 'GET',
      dataType: 'json',
      data: {
       'username': $('h4.user-title').first().text()
      },
      headers: {
       'Content-Type': 'application/json'
      },
      url: '/api/v1/get-instagram-profile-data/',
      success: (data) => {
        console.log(data.media_count, data.follower_count, data.following_count)
        $('.profile-amount_numb:eq(0)').text(data.media_count)
        $('.profile-amount_numb:eq(1)').text(data.follower_count)
        $('.profile-amount_numb:eq(2)').text(data.following_count)
      }
    })
  }
})