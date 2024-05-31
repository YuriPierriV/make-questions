





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
        questao_in_lateral.style.borderTop = '2px #EDC18D solid';
        saveOption(questionId, optionId);
    });
});



function checkRequired(id) {
    
}




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