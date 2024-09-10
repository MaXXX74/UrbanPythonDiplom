// Получить модальное окно
var comment_modal = document.getElementById("comment_window");

// // Получить элемент <span>, который закрывает модальное окно
var comment_span = document.getElementById("comment_span_id");

// Получить кнопку открытия модального окна
var commentButton = document.getElementById("comment_button");

// Открыть модальное окно при клике на кнопку
commentButton.onclick = function(event) {
    event.preventDefault();
    comment_modal.style.display = "flex";
}

// Закрыть модальное окно, когда пользователь нажимает на <span> (x)
comment_span.onclick = function() {
    comment_modal.style.display = "none";
}

// Закрыть модальное окно, когда пользователь нажимает за его пределами
window.onclick = function(event) {
    if (event.target == comment_modal) {
        comment_modal.style.display = "none";
    }
}

// Получить элементы формы
var commentForm = document.getElementById('comment_form');
var commentSubmitButton = document.getElementById('comment_submit_button');
var commentClearButton = document.getElementById('comment_clear_button');
var commentInputs = commentForm.querySelectorAll('input[type="text"]');
var commentTextarea = document.getElementById('comment_text');

// Включение и выключение кнопки "Отправить"
commentForm.addEventListener('input', function() {
    let allFieldsFilled = true; // Изначально считаем, что все поля заполнены
    commentInputs.forEach(function(input) {
        if (input.value.trim() === '') { // Если хотя бы одно поле пустое
            allFieldsFilled = false;
        }
    });
    commentSubmitButton.disabled = !allFieldsFilled; // Кнопка активна, если все поля заполнены
});

// Очистить все поля ввода при нажатии кнопки "Очистить"
commentClearButton.addEventListener('click', function() {
    commentTextarea.value = ''; // Очищаем содержимое textarea
    commentSubmitButton.disabled = true;
});
