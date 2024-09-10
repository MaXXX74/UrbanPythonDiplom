// Получить модальное окно
var modal = document.getElementById("modal");

// Получить элемент <span>, который закрывает модальное окно
var span = document.getElementsByClassName("close")[0];

// Получить кнопку открытия модального окна
var searchButton = document.getElementById("search_button");

// Открыть модальное окно при клике на кнопку
searchButton.onclick = function(event) {
    event.preventDefault();
    modal.style.display = "flex";
}

// Закрыть модальное окно, когда пользователь нажимает на <span> (x)
span.onclick = function() {
    modal.style.display = "none";
}

// Закрыть модальное окно, когда пользователь нажимает за его пределами
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Получить элементы формы
var searchForm = document.getElementById('search_form');
var submitButton = document.getElementById('submit_button');
var clearButton = document.getElementById('clear_button');
var inputs = searchForm.querySelectorAll('input[type="text"]');

// Включение и выключение кнопки "Найти"
searchForm.addEventListener('input', function() {
    let hasInput = false;
    inputs.forEach(function(input) {
        if (input.value.trim() !== '') {
            hasInput = true;
        }
    });
    submitButton.disabled = !hasInput;
});

// Очистить все поля ввода при нажатии кнопки "Очистить"
clearButton.addEventListener('click', function() {
    inputs.forEach(function(input) {
        input.value = '';
    });
    submitButton.disabled = true;
});