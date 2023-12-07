const actualBtn = document.getElementById('chooseFile');
const fileChosen = document.getElementById('noFile');
console.log(fileChosen)

actualBtn.addEventListener('change', function(){
    fileChosen.textContent = this.files[0].name
  })