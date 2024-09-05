// Скрипт для нажатия кнопки Комментарии
document.addEventListener('DOMContentLoaded', () => {
    // Получаем все ссылки с классом toggleLink
    const toggleLinks = document.querySelectorAll('.toggleLink');

    toggleLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault(); // Предотвращаем переход по ссылке

            // Получаем идентификатор блока из атрибута data-target
            const targetId = link.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);

            // Переключаем видимость блока
            if (targetElement.classList.contains('hidden')) {
                targetElement.classList.remove('hidden');
                targetElement.classList.add('visible');
            } else {
                targetElement.classList.remove('visible');
                targetElement.classList.add('hidden');
            }
        });
    });
});