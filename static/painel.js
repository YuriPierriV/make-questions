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

function uploadImage(userId) {
    var fileInput = document.getElementById('image_input_' + userId);
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('image', file);

    fetch('/user-image/' + userId, {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            window.location.reload();
            return response.json(); // Processa a resposta JSON se o status for OK
        }
        throw new Error('Falha ao enviar arquivo! Status: ' + response.status);
    }).then(data => {
        console.log('Sucesso:', data);
        var imgElement = document.querySelector(`img[src="/get-image/{{usuario.image[0]}}"]`); // Você precisa ajustar este seletor para apontar para o elemento de imagem correto.
        imgElement.src = `/get-image/${data.imageId}`; // Supondo que 'data.imageId' contém o ID da nova imagem
    }).catch(error => {
        console.error('Erro durante o envio do arquivo:', error);
    });
}