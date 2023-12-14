function enviarAtualizacao_form(campo, formId, paramName) {
    // Obtém o novo valor do campo de entrada
    var novoValor = campo.value;

    // Envia uma solicitação AJAX para atualizar o valor no backend
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/form/' + formId + '/edit' + '/att_form', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(paramName + '=' + encodeURIComponent(novoValor));
}

function enviarAtualizacao_question(campo,formId, questionId, paramName) {
    // Obtém o novo valor do campo de entrada
    var novoValor = campo.value;

    // Envia uma solicitação AJAX para atualizar o valor no backend
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/form/' + formId + '/edit' + '/att_question='+ questionId, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(paramName + '=' + encodeURIComponent(novoValor));
}

document.getElementById('nameInput').addEventListener('blur', function() {
    enviarAtualizacao_form(this, form.id, 'nome');
});

document.getElementById('tituloInput').addEventListener('blur', function() {
    enviarAtualizacao_form(this, form.id, 'titulo');
});

document.getElementById('descricaoInput').addEventListener('blur', function() {
    enviarAtualizacao_form(this, form.id, 'descricao');
});

questions.forEach(question => {
    document.getElementById('question_text_'+question.id).addEventListener('blur', function() {
        enviarAtualizacao_question(this, form.id,question.id, 'question_text');
    });
});





