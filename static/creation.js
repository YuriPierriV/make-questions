

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
            window.location.reload(); // Recar  rega a página
        }
    };
    xhr.send('id_form=' + id_form);
}

function deletarQuestao(question_id) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/del_question', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            window.location.reload(); // Recar  rega a página
        }
    };
    xhr.send('id_question=' + question_id);
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




function add_option(questionId, novoValor) {
    // Formate os dados para enviar no formato correto
    var data = 'questionId=' + encodeURIComponent(questionId) + '&' + 
               'novoValor=' + encodeURIComponent(novoValor);

    // Envia uma solicitação AJAX para atualizar o valor no backend
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/add_options', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(data); // Envie os dados formatados
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                window.location.reload(); // Recarrega a página se a solicitação for bem-sucedida
            } else {
                console.error('Erro na solicitação:', xhr.status); // Registre o erro, se houver
            }
        }
    };
}

function edit_option(optionId, novoValor) {
    // Formate os dados para enviar no formato correto
    var data = 'optionId=' + encodeURIComponent(optionId) + '&' + 
               'novoValor=' + encodeURIComponent(novoValor);

    // Envia uma solicitação AJAX para atualizar o valor no backend
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/edit_options', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(data); // Envie os dados formatados
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                window.location.reload(); // Recarrega a página se a solicitação for bem-sucedida
            } else {
                console.error('Erro na solicitação:', xhr.status); // Registre o erro, se houver
            }
        }
    };
}

var spans = document.querySelectorAll('.inputOption');

spans.forEach(function(span) {

    span.addEventListener('click', function(e) {
        var id = span.id.split("_");
        
        if (id[0] === 'add') {
            var input = document.createElement('input');
            input.className = 'editableInput';
            input.value = '';
            span.textContent = '';
            span.appendChild(input);
            setTimeout(function() {
                input.focus();
            }, 0);
            input.addEventListener('input', function() {
                // Ajustando a largura do input com base no tamanho do texto digitado
                this.style.width = (this.value.length * 10) + 'px'; // Ajuste o valor multiplicador conforme necessário
            });
            input.addEventListener('blur', function() {
                span.textContent = this.value || "";
                var question_id = id[2];
                add_option(question_id, this.value);
            });
            input.addEventListener('click', function(e) {
                e.stopPropagation();
            });
            input.style.width = (span.offsetWidth + 10) + 'px';
        } else if (id[0] === 'edit') {
            if (span.classList.contains('second_click')) {
                var input = document.createElement('input');
                input.className = 'editableInput';
                input.value = span.textContent;
                span.textContent = '';
                span.appendChild(input);
                setTimeout(function() {
                    input.focus();
                }, 0);
                input.addEventListener('input', function() {
                    // Ajustando a largura do input com base no tamanho do texto digitado
                    this.style.width = (this.value.length * 10) + 'px'; // Ajuste o valor multiplicador conforme necessário
                });
                input.addEventListener('blur', function() {
                    span.textContent = this.value || "";
                    var option_id = id[2];
                    edit_option(option_id, this.value);
                });
                input.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
                input.style.width = Math.max((span.offsetWidth + 10), (input.scrollWidth + 10)) + 'px';
            } else {
                // Desmarca os outros radios da mesma questão e marca o radio clicado
                spans.forEach(function(span_outros) {
                    var id_outros = span_outros.id.split("_");
                    if (id[4] === id_outros[4] && id[2] !== id_outros[2]) {
                        span_outros.classList.remove('second_click');
                    }
                });
                span.classList.add('second_click');
            }
        }
    });
});



document.addEventListener("DOMContentLoaded", function() {
    questions.forEach(question => {
        if (question.question_type == 'text'){
            document.getElementById('question_type_'+question.id).value = 'texto';
            console.log(question.id+'texto');
        }
        if (question.question_type == 'multimult_escolha'){
            document.getElementById('question_type_'+question.id).value = 'mult_escolha';
            console.log(question.id+'multi');
        }

    });
})



