// Quando o documento estiver pronto
document.addEventListener("DOMContentLoaded", function() {
    // Obtenha o botão "Entrar" e o menu suspenso
    var loginBtn = document.getElementById("loginBtn");
    var loginDropdown = document.getElementById("loginDropdown");


    const buttons = document.querySelectorAll('.btn-duvidas');


    loginBtn.style.borderColor = '#0733f6b2';

    buttons.forEach(button => {
        button.style.borderColor = '#0733f6b2';


        button.addEventListener('click', () => {
            const textoId = `texto-${button.id}`;
            const textoOculto = document.getElementById(textoId);
            const iconBtn = button.querySelector('.icon-btn');
    
            // Adicione estas linhas para mudar a cor da fonte do botão
            buttons.forEach(b => {
                b.style.color = ''; // Volta à cor padrão para todos os botões
                b.style.backgroundColor = '';
            });
             // Define a cor da fonte do botão clicado
            button.style.color = '#fff';
            button.style.backgroundColor = "#011021";

            if (window.getComputedStyle(textoOculto).getPropertyValue("display") === 'block') {
                textoOculto.style.display = 'none';
                iconBtn.classList.remove('bi-chevron-up');
                iconBtn.classList.add('bi-chevron-down');
                buttons.forEach(b => {
                    b.style.color = ''; // Volta à cor padrão para todos os botões
                    b.style.backgroundColor = '';
                });
            } else {
                document.querySelectorAll('.texto-oculto').forEach(texto => {
                    if (texto.id != textoId) {
                        texto.style.display = 'none';
                        document.querySelectorAll('.bi-chevron-up').forEach(up => {
                            up.classList.replace('bi-chevron-up', 'bi-chevron-down');
                            
                        })
                        
                        
                    }
                });
                textoOculto.style.display = 'block';
                iconBtn.classList.remove('bi-chevron-down');
                iconBtn.classList.add('bi-chevron-up');
            }
            
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


