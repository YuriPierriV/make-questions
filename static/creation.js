function enviarAtualizacao(campo, formId, paramName) {
    // Obtém o novo valor do campo de entrada
    var novoValor = campo.value;

    // Envia uma solicitação AJAX para atualizar o valor no backend
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/form/' + formId + '/edit', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(paramName + '=' + encodeURIComponent(novoValor));
}

document.getElementById('nameInput').addEventListener('blur', function() {
    enviarAtualizacao(this, form.id, 'nome');
});

document.getElementById('tituloInput').addEventListener('blur', function() {
    enviarAtualizacao(this, form.id, 'titulo');
});

document.getElementById('descricaoInput').addEventListener('blur', function() {
    enviarAtualizacao(this, form.id, 'descricao');
});


