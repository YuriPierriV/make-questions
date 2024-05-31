

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
    xhr.open('PUT', '/form/' + id_form + '/edit/att_question=' + questionId, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    if (paramName == 'question_type') {
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                window.location.reload(); // Recarrega a página
            }
        };
    }
    xhr.send(paramName + '=' + encodeURIComponent(novoValor));
}

function edicao_habilitar(id) {

    questions.forEach(question => {
        if (question.id != id) {
            questao_out = document.getElementById('question_edit_' + question.id);
            questao_out_menu = document.getElementById('question_controle_' + question.id);
            questao_out_lateral = document.getElementById('card_lateral_' + question.id);
            questao_out.style.display = 'none';
            questao_out_menu.style.borderTop = '0';
            questao_out_lateral.style.borderTop = '0';
        }
        else {
            questao_in = document.getElementById('question_edit_' + question.id);
            questao_in_menu = document.getElementById('question_controle_' + question.id);
            questao_in_lateral = document.getElementById('card_lateral_' + question.id);
            questao_in.style.display = "inline";
            questao_in_menu.style.borderTop = '5px #EDC18D solid';
            
            questao_in_lateral.style.borderTop = '2px #EDC18D solid';
        }
    })
}

function adicionarQuestao() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/add_question', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
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
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            window.location.reload(); // Recar  rega a página
        }
    };
    xhr.send('id_question=' + question_id);
}

function obrigatorio(question_id, required) {
    var data = 'question_id=' + encodeURIComponent(question_id) + '&' +
        'is_required=' + encodeURIComponent(required);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/obrigatorio', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            window.location.reload(); // Recar  rega a página
        }
    };
    xhr.send(data);
}

function new_link(form_id) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/new_link', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            window.location.reload(); // Recar  rega a página
        }
    };
    xhr.send('form_id=' + form_id);
}

function copy(link) {
    navigator.clipboard.writeText(link);
  } 


document.getElementById('nameInput').addEventListener('blur', function () {
    enviarAtualizacao_form(this, 'nome');
});

document.getElementById('tituloInput').addEventListener('blur', function () {
    enviarAtualizacao_form(this, 'titulo');
});

document.getElementById('descricaoInput').addEventListener('blur', function () {
    enviarAtualizacao_form(this, 'descricao');
});

document.getElementById('link_click').addEventListener('click', function () {
    abrirMenuLink();
});


questions.forEach(question => {
    document.getElementById('question_text_' + question.id).addEventListener('blur', function () {
        enviarAtualizacao_question(this.value, question.id, 'question_text');
    });
    document.getElementById('question_type_' + question.id + '_multi').addEventListener('click', function () {
        document.getElementById('question_type_' + question.id).value = 'mult_escolha';
        enviarAtualizacao_question('multimult_escolha', question.id, 'question_type');

    });
    document.getElementById('question_type_' + question.id + '_text').addEventListener('click', function () {
        document.getElementById('question_type_' + question.id).value = 'texto';
        console.log(document.getElementById('question_type_' + question.id).value);
        enviarAtualizacao_question('text', question.id, 'question_type');

    });
    document.getElementById('question_controle_' + question.id).addEventListener('mouseenter', function () {
        edicao_habilitar(question.id);
    });
    document.getElementById('card_lateral_' + question.id).addEventListener('click', function () {
        edicao_habilitar(question.id);
        document.getElementById("question_controle_"+question.id).tabIndex = "-1";
        document.getElementById("question_text_"+question.id).focus();
    })


    document.getElementById('button_image_'+question.id).addEventListener('click', function() {
        document.getElementById('image_'+question.id).click();
    });

    document.getElementById('image_'+question.id).addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            uploadFile(file, question.id);
        }
    });

    document.getElementById('required_' + question.id).addEventListener('click', function (e) {
        required = document.getElementById('required_' + question.id);
        if (required.classList.contains("selecionado")) {
            required.classList.remove("selecionado");
            obrigatorio(question.id, "0");
        }
        else {
            required.classList.add("selecionado");
            obrigatorio(question.id, "1");
        }

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
    xhr.onreadystatechange = function () {
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
    xhr.onreadystatechange = function () {
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

spans.forEach(function (span) {

    span.addEventListener('click', function (e) {
        var id = span.id.split("_");

        if (id[0] === 'add') {
            var input = document.createElement('input');
            input.className = 'editableInput';
            input.value = '';
            span.textContent = '';
            span.appendChild(input);
            setTimeout(function () {
                input.focus();
            }, 0);
            input.addEventListener('input', function () {
                // Ajustando a largura do input com base no tamanho do texto digitado
                this.style.width = (this.value.length * 10) + 'px'; // Ajuste o valor multiplicador conforme necessário
            });
            input.addEventListener('blur', function () {
                span.textContent = this.value || "";
                var question_id = id[2];
                add_option(question_id, this.value);
            });
            input.addEventListener('click', function (e) {
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
                setTimeout(function () {
                    input.focus();
                }, 0);
                input.addEventListener('input', function () {
                    // Ajustando a largura do input com base no tamanho do texto digitado
                    this.style.width = (this.value.length * 10) + 'px'; // Ajuste o valor multiplicador conforme necessário
                });
                input.addEventListener('blur', function () {
                    span.textContent = this.value || "";
                    var option_id = id[2];
                    edit_option(option_id, this.value);
                });
                input.addEventListener('click', function (e) {
                    e.stopPropagation();
                });
                input.style.width = Math.max((span.offsetWidth + 10), (input.scrollWidth + 10)) + 'px';
            } else {
                // Desmarca os outros radios da mesma questão e marca o radio clicado
                spans.forEach(function (span_outros) {
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



document.addEventListener("DOMContentLoaded", function () {
    const visible = localStorage.getItem("visible");
    const menu = localStorage.getItem("menu");
    edicao_habilitar(null);

    if (visible === "true") {
        
        loginDropdown.style.display = "block";
        overlay.style.display = "block";
        document.body.style.overflow = "hidden";
        if(menu === "link"){
            var link = document.getElementById('menu_link')
            link.classList.remove('menu_off')
            link.classList.add('menu_selecionado')
        }
    } else {
        loginDropdown.style.display = "none";
        overlay.style.display = "none";
        document.body.style.overflow = "";
    }

    const textareas = document.querySelectorAll('.inputTextquestion');
    const inputTextanswer = document.querySelectorAll('.inputTextanswer');
    
    function autoResize() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    }

    

    textareas.forEach(textarea => {
        autoResize.call(textarea);  
        textarea.addEventListener('input', autoResize);  
    });

    textareas.forEach(textarea => {
        autoResize.call(textarea);  
        textarea.addEventListener('input', autoResize);  
    });

    questions.forEach(question => {
        if (question.question_type == 'text') {
            document.getElementById('question_type_' + question.id).value = 'texto';
        }
        if (question.question_type == 'multimult_escolha') {
            document.getElementById('question_type_' + question.id).value = 'mult_escolha';
        }
        required = document.getElementById('required_' + question.id);
        if (question.required == '0') {
            required.classList.remove("selecionado");
        }
        else {
            required.classList.add("selecionado");
        }

    })
});




var loginDropdown = document.getElementById("loginDropdown");
var xButton = document.getElementById("xButton");
var overlay = document.getElementById("overlay");

function abrirMenuLink(){
    if (loginDropdown.style.display === "none" || loginDropdown.style.display === "") {
        loginDropdown.style.display = "block";
        overlay.style.display = "block";
        document.body.style.overflow = "hidden";
        localStorage.setItem("visible", "true");

    
    } else {
        loginDropdown.style.display = "none";
        overlay.style.display = "none";
        document.body.style.overflow = "";
        localStorage.setItem("visible", "false");
        
    }
}

xButton.addEventListener("click", function (e) {

    loginDropdown.style.display = "none";
    overlay.style.display = "none";
    document.body.style.overflow = "";
    localStorage.setItem("visible", "false");
});


var link = document.getElementById("invite_link")
var email = document.getElementById("invite_email")
var perfil = document.getElementById("invite_perfil")

var options = [link,email,perfil]

options.forEach(option=>{
    option.addEventListener('click', function(e){
        var menu = document.getElementById('menu_'+option.id.split('_')[1])
        menu.classList.remove('menu_off')
        menu.classList.add('menu_selecionado')
        option.classList.add("selecionado")
        localStorage.setItem("menu", option.id.split('_')[1]);
        options.forEach(option_no=>{
            if(option_no.id != option.id){
                var remove_visi = document.getElementById('menu_'+option_no.id.split('_')[1])
                option_no.classList.remove("selecionado")
                remove_visi.classList.remove('menu_selecionado')
                remove_visi.classList.add('menu_off')
            }
        })
    })
})

function uploadFile(file, questionId) {
    var formData = new FormData();
    formData.append('image', file); // 'image' é a chave esperada no lado do servidor

    fetch('/question-image/' + questionId, {
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
        var imgElement = document.querySelector(`img[src="/get-image/{{question.image[0]}}"]`); // Você precisa ajustar este seletor para apontar para o elemento de imagem correto.
        imgElement.src = `/get-image/${data.imageId}`; // Supondo que 'data.imageId' contém o ID da nova imagem
    }).catch(error => {
        console.error('Erro durante o envio do arquivo:', error);
    });
}



