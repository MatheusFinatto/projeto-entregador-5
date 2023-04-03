function addToWishlist(button) {
  if (!button.disabled) {
    // only proceed if button is not disabled
    button.disabled = true; // disable button
    var itemId = button.dataset.gameId;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/add-wishlist");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onload = function () {
      button.disabled = false; // re-enable button
      if (xhr.status === 200) {
        button.setAttribute("onclick", "removeFromWishlist(this)");
        button.setAttribute("data-tooltip", "Remove from wishlist");
        button.innerHTML =
          '<i class="fi fi-rr-check"></i><span class="buttons-tooltip">Remove from wishlist</span>';
      } else {
        alert("Error adding item to wishlist!");
      }
    };
    xhr.send("game_id=" + encodeURIComponent(itemId));
  }
}

function removeFromWishlist(button) {
  if (!button.disabled) {
    // only proceed if button is not disabled
    button.disabled = true; // disable button
    var itemId = button.dataset.gameId;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/remove-wishlist");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onload = function () {
      button.disabled = false; // re-enable button
      if (xhr.status === 200) {
        button.style.color = "#fff"; // set color back to white
        button.setAttribute("onclick", "addToWishlist(this)"); // set original onclick function
        button.setAttribute("data-tooltip", "Add to wishlist"); // set original tooltip text
        button.dataset.action = "add"; // set dataset action back to "add"

        button.innerHTML = `<i class="fi fi-rr-list"></i><span class="buttons-tooltip">Add to wishlist</span>`; // set original button HTML content
      } else {
        alert("Error removing item to wishlist!");
      }
    };
    xhr.send("game_id=" + encodeURIComponent(itemId));
  }
}
