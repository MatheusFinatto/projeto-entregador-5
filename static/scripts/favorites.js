function addToFavorites(button) {
  if (!button.disabled) {
    // only proceed if button is not disabled
    button.disabled = true; // disable button
    var itemId = button.dataset.gameId;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/add-favorite");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onload = function () {
      button.disabled = false; // re-enable button
      if (xhr.status === 200) {
        button.setAttribute("onclick", "removeFromFavorites(this)");
        button.setAttribute("data-tooltip", "Remove from favorites");
        button.style.color = "#a12d2d";
        button.innerHTML =
          '<i class="fi fi-sr-heart"></i><span class="buttons-tooltip">Remove from favorites</span>';
      } else {
        alert("Error adding item to favorites!");
      }
    };
    xhr.send("game_id=" + encodeURIComponent(itemId));
  }
}

function removeFromFavorites(button) {
  if (!button.disabled) {
    // only proceed if button is not disabled
    button.disabled = true; // disable button
    var itemId = button.dataset.gameId;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/remove-favorite");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onload = function () {
      button.disabled = false; // re-enable button
      if (xhr.status === 200) {
        button.style.color = "#fff"; // set color back to white
        button.setAttribute("onclick", "addToFavorites(this)"); // set original onclick function
        button.setAttribute("data-tooltip", "Add to favorites"); // set original tooltip text
        button.dataset.action = "add"; // set dataset action back to "add"
        button.innerHTML = `
    <i class="fi fi-rr-heart"></i>
    <span class="buttons-tooltip">Add to favorites</span>
  `; // set original button HTML content
      } else {
        alert("Error removing item to favorites!");
      }
    };
    xhr.send("game_id=" + encodeURIComponent(itemId));
  }
}
