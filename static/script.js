// Quando o documento estiver pronto
document.addEventListener("DOMContentLoaded", function() {
    // Obtenha o botão "Entrar" e o menu suspenso
    var loginBtn = document.getElementById("loginBtn");
    var loginDropdown = document.getElementById("loginDropdown");


    const buttons = document.querySelectorAll('.btn-duvidas');

        buttons.forEach(button => {
            button.addEventListener('click', () => {
                // Fecha todos os textos ocultos
                const textoId = `texto-${button.id}`;
                const textoOculto = document.getElementById(textoId);
                const iconBtn = button.querySelector('.icon-btn');

                if (window.getComputedStyle(textoOculto).getPropertyValue("display") === 'block') {
                    console.log(window.getComputedStyle(textoOculto).getPropertyValue("display"));
                    textoOculto.style.display = 'none';
                    iconBtn.classList.remove('bi-chevron-up');
                    iconBtn.classList.add('bi-chevron-down');
                    document.querySelectorAll('.texto-oculto').forEach(texto => {
                        texto.style.display = 'none';
                    });
                } else {
                    document.querySelectorAll('.texto-oculto').forEach(texto => {
                        if(texto.id != textoId){
                            texto.style.display = 'none';
                            console.log(window.getComputedStyle(textoOculto).getPropertyValue("display"));
                        }
                        
                    });
                    console.log(window.getComputedStyle(textoOculto).getPropertyValue("display"));
                    textoOculto.style.display = 'block';
                    iconBtn.classList.remove('bi-chevron-down');
                    console.log(window.getComputedStyle(textoOculto).getPropertyValue("display"));
                    iconBtn.classList.add('bi-chevron-up');
                    

                }

                

                // Redefine todos os ícones para baixo
                document.querySelectorAll('.icon-btn').forEach(icon => {
                    icon.classList.remove('bi-chevron-up');
                    icon.classList.add('bi-chevron-down');
                });

                

                
            });
        });



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


