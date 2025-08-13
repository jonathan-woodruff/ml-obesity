import * as bootstrap from 'bootstrap'; //js

const submitButton = document.getElementById('submit');

const submitContent = (event) => {
  event.preventDefault();
  alert('hi');
}

submitButton.addEventListener('click', submitContent);