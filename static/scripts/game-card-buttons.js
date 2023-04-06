$(document).ready(function() {
// TODO aplicar a logica para todos os botões de favoritos e wishlist
    $("#addFavoriteMask").click(function() {
        console.log("click")
        if ($("#addFavorite").is(":disabled")) {
            alert('You must login first')
        }
    })
});