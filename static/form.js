





// Função para salvar a resposta no Local Storage
function saveResponse(questionId, answer) {
    localStorage.setItem('question_' + questionId, answer);
    
}

// Função para salvar a opção selecionada no Local Storage
function saveOption(questionId, optionId) {
    localStorage.setItem('option_' + questionId, optionId);
}

// Função para recuperar as respostas do Local Storage
function loadResponses() {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const questionId = textarea.id.split('_').pop();
        const savedAnswer = localStorage.getItem('question_' + questionId);
        questao_in_lateral = document.getElementById('card_lateral_' + questionId);
        
        if (savedAnswer) {
            questao_in_lateral.style.borderTop = '2px #EDC18D solid';
            textarea.value = savedAnswer;
        }
    });

    const radioButtons = document.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(radio => {
        const ids = radio.id.split('_');
        const questionId = ids[3];
        const optionId = ids[1];
        const savedOption = localStorage.getItem('option_' + questionId);
        questao_in_lateral = document.getElementById('card_lateral_' + questionId);
        
        if (savedOption && savedOption === optionId) {
            questao_in_lateral.style.borderTop = '2px #EDC18D solid';
            radio.checked = true;
        }
    });
}

// Adiciona event listener para salvar a resposta quando o usuário digitar
const textareas = document.querySelectorAll('textarea');
textareas.forEach(textarea => {
    textarea.addEventListener('input', function () {
        const questionId = this.id.split('_').pop();
        saveResponse(questionId, this.value);
        if(this.value == ''){
            questao_out_lateral = document.getElementById('card_lateral_' + questionId);
            questao_out_lateral.style.borderTop = '0';
        }
        else{
            questao_in_lateral = document.getElementById('card_lateral_' + questionId);
            questao_in_lateral.style.borderTop = '2px #EDC18D solid';
            const quest = document.getElementById("question_controle_" + questionId);
            quest.style.borderTop = '5px #EDC18D solid';
        }
    });
});





// Adiciona event listener para salvar a opção selecionada quando o usuário clicar
const radioButtons = document.querySelectorAll('input[type="radio"]');
radioButtons.forEach(radio => {
    radio.addEventListener('change', function () {
        const ids = this.id.split('_');
        const questionId = ids[3];
        const optionId = ids[1];
        questao_in_lateral = document.getElementById('card_lateral_' + questionId);
        const quest = document.getElementById("question_controle_" + questionId);
        quest.style.borderTop = '5px #EDC18D solid';
        questao_in_lateral.style.borderTop = '2px #EDC18D solid';
        saveOption(questionId, optionId);
    });
});



function checkRequired() {
    let allRequiredFilled = true;

    questions.forEach(question => {
        if (question.required) {
            if (question.question_type == "multimult_escolha") {
                const form = document.getElementById('form_question_' + question.id);
                const inputs = form.querySelectorAll('input');
                const isAnyChecked = Array.from(inputs).some(input => input.checked);

                if (!isAnyChecked) {
                    
                    allRequiredFilled = false;
                }
                
            }

            if (question.question_type == "text") {
                const textArea = document.getElementById('answer_text_' + question.id);
                if (textArea.value.trim() === "") {
                    
                    allRequiredFilled = false;
                }
                
            }
        }
    });

    return allRequiredFilled;
}


function markQuestion() {
    questions.forEach(question => {
        if (question.required) {
            if (question.question_type == "multimult_escolha") {
                const form = document.getElementById('form_question_' + question.id);
                const inputs = form.querySelectorAll('input');                        
                const isAnyChecked = Array.from(inputs).some(input => input.checked);
                if (!isAnyChecked) {
                    
                    const quest = document.getElementById("question_controle_" + question.id);
                    quest.tabIndex = "-1";
                    quest.style.borderTop = '5px #aa341c solid';
                    quest.focus();
                    quest.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
    
            if (question.question_type == "text") {
                const textArea = document.getElementById('answer_text_' + question.id);
                if (textArea.value.trim() === "") {
                    const quest = document.getElementById("question_controle_" + question.id);
                    quest.tabIndex = "-1";
                    quest.style.borderTop = '5px #aa341c solid';
                    quest.focus();
                    quest.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        }
    });

}


function answer(question_id, selected_id, response_text) {
    var data = 'question_id=' + encodeURIComponent(question_id) + '&' +
        'selected_id=' + encodeURIComponent(selected_id)+ '&' +'response_text=' + encodeURIComponent(response_text);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/send_answer', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            
        }
    };
    xhr.send(data);
}


function enviarResposta() {
    
    questions.forEach(question => {
        if (question.question_type == "multimult_escolha") {
            const form = document.getElementById('form_question_' + question.id);
            const inputs = form.querySelectorAll('input');                        
            inputs.forEach(input =>{
                if(input.checked){
                    split_input = input.id.split('_');
                    const selected_id = split_input[1];
                    answer(question.id, selected_id, null)
                }
            })
            
        }

        if (question.question_type == "text") {
            const textArea = document.getElementById('answer_text_' + question.id);
            answer(question.id, 0, textArea.value)
        }
    });

}




const botaoEnviar = document.getElementById('enviarRespostas');
const btnLoading = document.querySelector('#btn-loading');

botaoEnviar.addEventListener('click', function () {
    const allRequiredFilled = checkRequired();
    if(allRequiredFilled){
        // Desabilita o botão e adiciona a animação de loading
        btnLoading.style.display = 'block';
        botaoEnviar.style.display = 'none';
        enviarResposta();
        // Espera 5 segundos antes de enviar a resposta
        setTimeout(function() {
            window.location.href = "/";    
        }, 500);
    }
    else{
        markQuestion();
    }
});



document.addEventListener("DOMContentLoaded", function () {
    // Carrega as respostas salvas ao carregar a página
    loadResponses();
    

    const inputTextanswer = document.querySelectorAll('.inputTextanswer');
    
    
    function autoResize() {
        this.style.height = 'auto'; 
        this.style.height = (this.scrollHeight) + 'px'; 
    }

    inputTextanswer.forEach(textarea => {
        autoResize.call(textarea); 
        textarea.addEventListener('input', autoResize); 
    });


});




questions.forEach(question => {
    document.getElementById('card_lateral_' + question.id).addEventListener('click', function () {
        document.getElementById("question_controle_"+question.id).tabIndex = "-1";
        document.getElementById("question_text_" + question.id).focus();
        document.getElementById("question_text_" + question.id).scrollIntoView({ behavior: 'smooth', block: 'center' });
        
    })
    //marcar se foi feita
});