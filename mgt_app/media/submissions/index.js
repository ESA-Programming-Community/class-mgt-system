// Menu Show Y Hidden
const navMenu = document.getElementById("nav-menu"),
      navToggle = document.getElementById("nav-toggle"),
      navClose = document.getElementById("nav-close"),
      accordionButton = document.getElementsByClassName("skill__arrow")

//Menu Show
if(navToggle){
    navToggle.addEventListener('click', () => {
        console.log("yah")
        navMenu.classList.add("show-menu")
    })
}

//Menu Close
if(navClose){
    navClose.addEventListener('click', ()=>{
        navMenu.classList.remove("show-menu")
    })
}

//Close Menu After Clicking a Nav Link
const navLink = document.querySelectorAll(".nav__link")

function closeMenuAfterClick(){
    navMenu.classList.remove("show-menu")
}

navLink.forEach(link => link.addEventListener('click', closeMenuAfterClick))

// ACCORDION

var skillContent = document.getElementsByClassName("skill__content")
var skillHeader = document.querySelectorAll(".skill__header")


function toggleSkills(){
    let itemClass = this.parentNode.className

    for(i = 0; i < skillContent.length; i++){
        skillContent[i].className = 'skill__content skill__close'
        
        if (itemClass === 'skill__content skill__close'){
            this.parentNode.className = 'skill__content skill__open'
        }
    }
}

skillHeader.forEach((e) => {
    e.addEventListener('click', toggleSkills)
})

//Qualification
const tabs = document.querySelectorAll('[data-target]'),
      tabsContent = document.querySelectorAll('[data-content')

tabs.forEach(tab => {
    tab.addEventListener('click', ()=>{
        const target = document.querySelector(tab.dataset.target)

        tabsContent.forEach(tabContent => {
            tabContent.classList.remove("qualification__active")
        })

        target.classList.add("qualification__active")

        tabs.forEach(tab => {
            tab.classList.remove("qualification__active")
        })
        tab.classList.add("qualification__active")
    })
})

//Services Modal
const modalViews = document.querySelectorAll(".service__modal"),
      modalBtns = document.querySelectorAll(".service__button"),
      modalExits = document.querySelectorAll(".service__modal-close")

let modal = function(modalClick){
    modalViews[modalClick].classList.add("active-modal")
}

modalBtns.forEach((modalBtn, i) => {
    modalBtn.addEventListener('click', ()=>{
        modal(i)
    })
})

modalExits.forEach((modalExit) => {
    modalExit.addEventListener('click', ()=>{
        modalViews.forEach(modalView => {
            modalView.classList.remove("active-modal")
        })
    })
})

//Portfolio Swiper
let swiperPortfolio = new Swiper(".portfolio__container", {
    cssMode: true,
    loop: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev"
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    keyboard: true
  });

//Testimonial
let swiperTestimonial = new Swiper(".testimonial__container", {
    loop: true,
    grabCursor: true,
    spaceBetween: 48,

    pagination: {
        el: ".swiper-pagination",
        clickable: true,
        dynamicBullets: true,
    },
    
    breakpoints: {
        568: {
            slidesPerView: 2,
        }
    }
  });


  function scrollHeader(){
    const nav = document.getElementById('header')

    if(this.scrollY >= 80) nav.classList.add('scroll-header'); else nav.classList.remove('scroll-header')
  }

  window.addEventListener('scroll', scrollHeader)


function scrollUp(){
    const scrollUp = document.getElementById('scroll_up');
    if(this.scrollY > 560) scrollUp.classList.add('show-scroll'); else scrollUp.classList.remove('show-scroll')
}

window.addEventListener('scroll', scrollUp)

/*==================== DARK LIGHT THEME ====================*/ 
const themeButton = document.getElementById('theme-button')
const darkTheme = 'dark-theme'
const iconTheme = 'uil-sun'

// Previously selected topic (if user selected)
const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

// We obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'uil-moon' : 'uil-sun'

// We validate if the user previously chose a topic
if (selectedTheme) {
  // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark
  document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
  themeButton.classList[selectedIcon === 'uil-moon' ? 'add' : 'remove'](iconTheme)
}

// Activate / deactivate the theme manually with the button
themeButton.addEventListener('click', () => {
    // Add or remove the dark / icon theme
    document.body.classList.toggle(darkTheme)
    themeButton.classList.toggle(iconTheme)
    // We save the theme and the current icon that the user chose
    localStorage.setItem('selected-theme', getCurrentTheme())
    localStorage.setItem('selected-icon', getCurrentIcon())
})