

document.addEventListener("DOMContentLoaded", function() {
    window.addEventListener('load', function() {
        // Pega todos os formulários que nós queremos aplicar estilos de validação Bootstrap personalizados.
        var forms = document.getElementsByClassName('needs-validation');
        // Faz um loop neles e evita o envio
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
                }, false);
            });    
    }, false);


    var formTel = document.getElementById("validationCustom03");
    

    

    formTel.addEventListener("input", function() {
        const tamanho = formTel.value;
        console.log(tamanho.length);
        if(tamanho.length == 1){
            formTel.value = `(${tamanho}`;
        }
        if(tamanho.length == 3){
            formTel.value = `${tamanho}) `;
        }
    })


});