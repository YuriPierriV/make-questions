

function enviarAtualizacao_form(campo, paramName) {
    // Obtém o novo valor do campo de entrada
    var novoValor = campo.value;

    // Envia uma solicitação AJAX para atualizar o valor no backend
    var xhr = new XMLHttpRequest();
    xhr.open('PUT', '/form/' + id_form + '/edit/att_form', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(paramName + '=' + encodeURIComponent(novoValor));
}

function enviarAtualizacao_question(campo, questionId, paramName) {
    // Obtém o novo valor do campo de entrada
    var novoValor = campo.value;

    // Envia uma solicitação AJAX para atualizar o valor no backend
    var xhr = new XMLHttpRequest();
    xhr.open('PUT', '/form/' + id_form + '/edit/att_question='+ questionId , true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(paramName + '=' + encodeURIComponent(novoValor));
}

document.getElementById('nameInput').addEventListener('blur', function() {
    enviarAtualizacao_form(this, 'nome');
});

document.getElementById('tituloInput').addEventListener('blur', function() {
    enviarAtualizacao_form(this, 'titulo');
});

document.getElementById('descricaoInput').addEventListener('blur', function() {
    enviarAtualizacao_form(this, 'descricao');
});


questions.forEach(question => {
    document.getElementById('question_text_'+question.id).addEventListener('blur', function() {
        enviarAtualizacao_question(this,question.id, 'question_text');
    });
    document.getElementById('question_type_'+question.id).addEventListener('click', function() {
        enviarAtualizacao_question(this,question.id, 'question_type');
    });
});

function adicionarQuestao() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/add_question', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            window.location.reload(); // Recarrega a página
        }
    };
    xhr.send('id_form=' + id_form);
}





