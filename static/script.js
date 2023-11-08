// Quando o documento estiver pronto
document.addEventListener("DOMContentLoaded", function() {
    // Obtenha o botão "Entrar" e o menu suspenso
    var loginBtn = document.getElementById("loginBtn");
    var loginDropdown = document.getElementById("loginDropdown");
    var duvidasBtn = document.getElementsByClassName("btn-duvidas");


    for (var i = 0; i < duvidasBtn.length; i++) {
        duvidasBtn[i].addEventListener("click", function(e) {
            // Obter os elementos atualmente abertos
            var openElements = document.querySelectorAll(".texto-oculto:not([style*='display: none'])");
            var icon = this.getElementsByClassName("icon-btn");
    
            // Fechar os elementos atualmente abertos
            
        
            // Abrir os elementos associados a este botão
            var child = this.getElementsByClassName("texto-oculto");
            
    
            for (var j = 0; j < icon.length;j++){
                if(icon[j].classList.contains("bi-chevron-down")){
                    icon[j].classList.replace("bi-chevron-down","bi-chevron-up");
                    continue;
                }
                if(icon[j].classList.contains("bi-chevron-up")){
                    icon[j].classList.replace("bi-chevron-up","bi-chevron-down");
                    continue;
                }
            }
    
        
            for (var j = 0; j < child.length; j++) {
                var currentDisplay = window.getComputedStyle(child[j]).getPropertyValue("display");
            
                if(currentDisplay == "none"){
                    child[j].style.display = "block";
                    continue;
                }
                if(currentDisplay == "block"){
                    child[j].style.display = "none";
                    continue;
                }
            }
        });

        for (var j = 0; j < openElements.length; j++) {
            openElements[j].style.display = "none";
            
        }
    }



    // Adicione um evento de clique ao botão "Entrar"
    loginBtn.addEventListener("click", function() {
        
        // Alternar a visibilidade do menu suspenso
        if (loginDropdown.style.display === "none" || loginDropdown.style.display === "") {
            loginDropdown.style.display = "block";
        } else {
            loginDropdown.style.display = "none";
        }
    });

    // Adicione um ouvinte de clique no documento para fechar o menu suspenso quando clicar em outro lugar na página
    document.addEventListener("click", function(e) {

        if (e.target !== loginBtn && e.target !== loginDropdown) {
            var isChildOfDropdown = isDescendant(loginDropdown, e.target);
            if (!isChildOfDropdown) {
                loginDropdown.style.display = "none";
            }
        }
    });

    function isDescendant(parent, child) {
        var node = child.parentNode;
        while (node != null) {
            if (node === parent) {
                return true;
            }
            node = node.parentNode;
        }
        return false;
    }




});


