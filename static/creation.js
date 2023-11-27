document.getElementById('titleInput').addEventListener('blur', function() {
    // Obtém o novo valor do campo de entrada
    var novoTitulo = this.value;

    // Envia uma solicitação AJAX para atualizar o título no backend
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/form/' + form.id + '/edit', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('title=' + encodeURIComponent(novoTitulo));
});
