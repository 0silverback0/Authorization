//UI controls

const LOGIN_BTN = document.querySelector('.login-btn')
const SIGNUP_BTN = document.querySelector('.signup-btn')
const LOGOUT_BTN = document.querySelector('.logout-btn')
const SIGNUP_FORM = document.querySelector('#signup')
const LOGIN_FORM = document.querySelector('#login')

LOGIN_BTN.addEventListener('click', e => {
    e.preventDefault()
    console.log(e.target)
    LOGIN_FORM.classList.remove('hide')
    SIGNUP_FORM.classList.add('hide')
    LOGIN_BTN.classList.add('hide')
    SIGNUP_BTN.classList.remove('hide')
})

SIGNUP_BTN.addEventListener('click', e => {
    e.preventDefault()
    LOGIN_FORM.classList.add('hide')
    SIGNUP_FORM.classList.remove('hide')
    LOGIN_BTN.classList.remove('hide')
    SIGNUP_BTN.classList.add('hide')
})