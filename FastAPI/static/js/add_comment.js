        // Получить модальное окно
        var comment_modal = document.getElementById("add_comment");

        // Получить элемент <span>, который закрывает модальное окно
        var span = document.getElementsByClassName("close")[0];

        // Получить кнопку открытия модального окна
        var addCommentButton = document.getElementById("add_comment_button");

        // Открыть модальное окно при клике на кнопку
        searchButton.onclick = function(event) {
            event.preventDefault();
            comment_modal.style.display = "flex";
        }

        // Закрыть модальное окно, когда пользователь нажимает на <span> (x)
        span.onclick = function() {
            comment_modal.style.display = "none";
        }
        
        // Закрыть модальное окно, когда пользователь нажимает за его пределами
        window.onclick = function(event) {
            if (event.target == comment_modal) {
                comment_modal.style.display = "none";
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