$(document).ready(function(){
  $('.carousel').carousel();
});

$("#edit-images").click(function () {
  console.log($("#input-file").val())
  executar()
  return
});

function executar(e){
  console.log('CLICK')
  $('#input-file').trigger('click');
  return
}

const profileImage = document.querySelector('.profile-image');
const imageInput = document.querySelector('#input-file');
profileImage.addEventListener('change', function(evt) {
  if (!(evt.target && evt.target.files && evt.target.files.length > 0)) {
    return;
  }

  // Inicia o file-reader:
  var r = new FileReader();
  // Define o que ocorre quando concluir:
  r.onload = function() {
     // Define o `src` do elemento para o resultado:
     profileImage.src = r.result;
  }
  // Lê o arquivo e cria um link (o resultado vai ser enviado para o onload.
  r.readAsDataURL(evt.target.files[0]);
  
  // Define o texto (coisa que já tava fazendo, ~estou ignorando problema de segurança~):
  document.querySelector('#meme-text').innerHTML = textInsert.value;
});