// <!-- Platforms script for "show more" button-->
//when clicked, a show more button calls this function with "this.id" as param
function showAllPlatforms(clicked_id) {
  //captures the <li> and <button> of the game, based on the id
  //the id's are ordered by "A + item.id" for <li> and "B + item.id" for <button>
  const platformListItems = document.querySelectorAll(
    `#${clicked_id.replace("A", "B")}`
  );
  const platformButtonShow = document.querySelector(`#${clicked_id}`);

  for (each of platformListItems) each.style.display = "flex";
  platformButtonShow.style.display = "none";

  //creates a new <li> (show-less-button li), appends html to it, gives it an 'onclick' event that reverts the action above and
  const newEl = document.createElement("li");
  newEl.innerHTML = `<button id = 'hide-all-platforms'><i id='plus-sign' class="fi fi-br-plus"></i></button><p class="platform-name">Show less</p> `;
  newEl.onclick = () => {
    for (each of platformListItems) each.style.display = "none";
    platformButtonShow.style.display = "flex";
    newEl.style.display = "none";
  };

  //appends the 'show less button li' to the last <li> of the game.
  platformListItems[platformListItems.length - 1].after(newEl);
}

function showFilters(button) {
  const rating_count_form = document.querySelector("#rating_count_form");
  rating_count_form.style.display = "flex";
  button.blur();
  button.innerText = "Hide filters";
  button.setAttribute("onclick", "hideFilters(this)");
}

function hideFilters(button) {
  const rating_count_form = document.querySelector("#rating_count_form");
  rating_count_form.style.display = "none";
  button.blur();
  button.innerText = "Show filters";
  button.setAttribute("onclick", "showFilters(this)");
}
