

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
    var novoValor = campo;

    // Envia uma solicitação AJAX para atualizar o valor no backend
    var xhr = new XMLHttpRequest();
    xhr.open('PUT', '/form/' + id_form + '/edit/att_question='+ questionId , true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    if(paramName == 'question_type'){
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                window.location.reload(); // Recarrega a página
            }
        };
    }
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
        enviarAtualizacao_question(this.value,question.id, 'question_text');
    });
    document.getElementById('question_type_'+question.id+'_multi').addEventListener('click', function() {
        document.getElementById('question_type_'+question.id).value = 'mult_escolha';
        console.log(document.getElementById('question_type_'+question.id).value);
        enviarAtualizacao_question('multimult_escolha',question.id, 'question_type');
        
    });
    document.getElementById('question_type_'+question.id+'_text').addEventListener('click', function() {
        document.getElementById('question_type_'+question.id).value = 'texto';
        console.log(document.getElementById('question_type_'+question.id).value);
        enviarAtualizacao_question('text',question.id, 'question_type');
        
    });
    document.getElementById('question_controle_'+question.id).addEventListener('mouseenter', function(){
        edicao_habilitar(question.id);
    });
    document.getElementById('card_lateral_'+question.id).addEventListener('click', function(){
        edicao_habilitar(question.id);
    })
});


var spans = document.querySelectorAll('.inputOption');

    // Adicionando um evento de clique a cada span
    spans.forEach(function(span) {
        span.addEventListener('click', function() {
            // Verificando se o span clicado tem a classe 'editable'
            
            if (this.classList.contains('editable')) {
                // Substituindo o texto do span por um campo de entrada
                span.textContent = ""
                var input = document.createElement('input');
                input.className = 'editableInput';
                input.value = this.textContent;
                this.textContent = '';
                this.appendChild(input);
                setTimeout(function() {
                    input.focus();
                }, 0);
                // Atualizando o tamanho do input conforme o texto é digitado
                input.addEventListener('input', function() {
                    // Ajustando a largura do input com base no tamanho do texto digitado
                    this.style.width = (this.value.length * 10) + 'px'; // Ajuste o valor multiplicador conforme necessário
                });
                
                // Adicionando um evento de mudança ao input para atualizar o span quando o texto for modificado
                input.addEventListener('blur', function() {
                    span.textContent = this.value || "";
                });
                
            }
        });
    });





document.addEventListener("DOMContentLoaded", function() {
    questions.forEach(question => {
        if (question.question_type == 'text'){
            console.log(question.id);
            document.getElementById('question_type_'+question.id).value = 'texto';
        }
        if (question.question_type == 'multimult_escolha'){
            console.log(question.id);
            document.getElementById('question_type_'+question.id).value = 'mult_escolha';
        }

    });
})



