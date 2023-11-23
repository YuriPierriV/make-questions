document.addEventListener("DOMContentLoaded", function() {
    const lateral = document.querySelectorAll(".lateral");
    const inicio = document.getElementById('painel');
    inicio.style.color = '#EDC18D';

    lateral.forEach(botoes => {
        
        botoes.addEventListener("click",function(){
            lateral.forEach(botoes =>{
                const section = document.getElementById(`${botoes.id}-section`);
                section.style.display = 'none';
                botoes.style.color = '';
            })
            const section = document.getElementById(`${botoes.id}-section`);
            section.style.display = 'block';
            botoes.style.color = '#EDC18D';
        })
    });


});