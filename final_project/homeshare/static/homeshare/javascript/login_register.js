document.addEventListener('DOMContentLoaded', function () {

  const sign_in_button = document.querySelector('#login-button');
  const sign_up_button = document.querySelector('#register-button');
  document.querySelector('#login-form').style.display = 'block';
  document.querySelector('#register-form').style.display = 'none';
  const container = document.querySelector('.container');

  sign_up_button.addEventListener('click', () => login(container))

  sign_in_button.addEventListener('click', () => register(container))

});

function login(ele){
  document.querySelector('#login-form').style.display = 'none';
  document.querySelector('#register-form').style.display = 'block';
  ele.classList.add('sign-up-mode')
}

function register(ele){
  document.querySelector('#login-form').style.display = 'block';
  document.querySelector('#register-form').style.display = 'none';
  ele.classList.remove('sign-up-mode')
}