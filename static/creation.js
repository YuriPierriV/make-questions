

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

function edicao_habilitar(id){
    
    questions.forEach(question => {
        if (question.id != id){
            questao_out = document.getElementById('question_edit_'+question.id);
            questao_out_menu = document.getElementById('question_controle_'+question.id);
            questao_out_lateral = document.getElementById('card_lateral_'+question.id);
            questao_out.style.display = 'none';
            questao_out_menu.style.borderTop = '0';
            questao_out_lateral.style.borderTop = '0';
        }
        else{
            questao_in = document.getElementById('question_edit_'+question.id);
            questao_in_menu = document.getElementById('question_controle_'+question.id);
            questao_in_lateral = document.getElementById('card_lateral_'+question.id);
            questao_in.style.display = "inline";
            questao_in_menu.style.borderTop = '5px #EDC18D solid';
            questao_in_lateral.style.borderTop = '5px #EDC18D solid';
        }
    })
}

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

function selected_type(id,type){
    
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
    document.getElementById('question_controle_'+question.id).addEventListener('mouseenter', function(){
        edicao_habilitar(question.id);
    });
    document.getElementById('card_lateral_'+question.id).addEventListener('click', function(){
        edicao_habilitar(question.id);
    })
});








document.addEventListener("DOMContentLoaded", function() {
    edicao_habilitar(questions[0].id);
})