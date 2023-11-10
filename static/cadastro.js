

document.addEventListener("DOMContentLoaded", function() {
    


    var formTel = document.getElementById("validationCustom03");
    

    formTel.addEventListener("input", function(event) {
        var valor = formTel.value;
        const possibles = [0,1,2,3,4,5,6,7,8,9];
        var ultimo = valor.slice(-1);
        

        if(possibles.some(numero => ultimo == numero) && ultimo != ' ' && event.inputType !== "deleteContentBackward"){
            if(valor.length == 1){
                formTel.value = `(${valor}`;
            }
            if(valor.length == 3){
                formTel.value = `${valor}) `;
            }
            if(valor.length == 10){
                formTel.value = `${valor}-`;
            }
            if(valor.length == 16){
                formTel.value = valor.slice(0, -1);
            }
        }
        else if(event.inputType === "deleteContentBackward"){

        }
        else{
            formTel.value = valor.slice(0, -1);
            valor = formTel.value;
        }
        
        
    })

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
});