$(document).ready(function() {
    const rating = $('#game-rating').val() ? $('#game-rating').val() : 0;
    updateRating(rating);
});

function updateStars(event) {
    const stars = document.getElementById('ratingStars');
    const rect = stars.getBoundingClientRect();
    const starWidth = rect.width / 5;
    const mouseX = event.clientX - rect.left;
    const rating = Math.ceil(mouseX / starWidth);

    $('#game-rating').val(rating);

    updateRating(rating);
}

function updateRating(rating) {
    const stars = document.getElementById('ratingStars');

    const starEmpty = "../static/img/Star_empty.svg.png";
    const starFull = "../static/img/Star_full.svg.png";

    const starImages = stars.getElementsByTagName('img');

    for (let i = 0; i < starImages.length; i++) {
      if (i < rating) {
        starImages[i].src = starFull;
      } else {
        starImages[i].src = starEmpty;
      }
    }

    return;
}