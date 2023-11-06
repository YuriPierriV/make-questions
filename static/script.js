// Quando o documento estiver pronto
document.addEventListener("DOMContentLoaded", function() {
    // Obtenha o botão "Entrar" e o menu suspenso
    var loginBtn = document.getElementById("loginBtn");
    var loginDropdown = document.getElementById("loginDropdown");

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
