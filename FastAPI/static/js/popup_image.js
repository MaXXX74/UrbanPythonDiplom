function openImagePopup(src) {
    var popup = document.getElementById('image-popup');
    var popupImage = document.getElementById('popup-image');
    popupImage.src = src;
    popup.style.display = "block";
    document.addEventListener('keydown', closeOnEsc);
}

function closeImagePopup() {
    var popup = document.getElementById('image-popup');
    popup.style.display = "none";
    document.removeEventListener('keydown', closeOnEsc);
}

function closeOnEsc(event) {
    if (event.key === 'Escape') {
        closeImagePopup();
    }
}
