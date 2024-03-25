document.addEventListener("DOMContentLoaded", function() {
    const lateral = document.querySelectorAll(".lateral");
    const inicio = document.getElementById('painel');
    inicio.style.color = '#EDC18D';

    lateral.forEach(botoes => {
        
        botoes.addEventListener("click",function(){
            lateral.forEach(botoes =>{
                const section = document.getElementById(`${botoes.id}-section`);
                section.style.display = 'none';
                botoes.style.color = '';
            })
            const section = document.getElementById(`${botoes.id}-section`);
            section.style.display = 'block';
            botoes.style.color = '#EDC18D';
        })
    });

    
    const iconNotificacao = document.querySelector('.icon-notificacao');
    const barraLateral = document.getElementById('barra-lateral');
    const notificacoesContainer = document.getElementById('notificacoes');

    iconNotificacao.addEventListener('click', () => {
        // Alternar classe para expandir ou minimizar a barra lateral
        barraLateral.classList.toggle('barra-lateral-fechada');
        
        // Limpar notificações ao minimizar
        notificacoesContainer.innerHTML = '';

        // Atualiza o número de notificações para zero após exibir
        iconNotificacao.dataset.number = '0';
    });

});

function confirmDelete(url) {
    if (confirm('Tem certeza de que deseja excluir este formulário?')) {
        window.location.href = url;
    }
}

window.addEventListener("load", function() {
    const loginDropdownVisible = localStorage.getItem("page");

    if (loginDropdownVisible === "true") {
        loginDropdown.style.display = "block";
        overlay.style.display = "block";
        document.body.style.overflow = "hidden";
    } else {
        loginDropdown.style.display = "none";
        overlay.style.display = "none";
        document.body.style.overflow = "";
    }
});