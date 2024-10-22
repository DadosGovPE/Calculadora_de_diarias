document.addEventListener("DOMContentLoaded", function () {
    const startButton = document.getElementById("start-button");
    const imagemAviaoDiv = document.getElementById("imagem-aviao-div");
    const aviacaoDiv = document.getElementById("aviacao-div");
    const aviacaoAnimacao = document.getElementById("aviacao-animacao"); // Seleciona o player da animação

    startButton.addEventListener("click", function () {
        console.log("Botão INICIAR clicado!"); // Log de depuração

        // Verifica se a tela é mobile (menos de 768px)
        if (window.innerWidth < 768) {
            // Para mobile, apenas redireciona sem animação
            window.location.href = "/multi_step_form";
        } else {
            // Desktop: Adiciona a animação

            // Adiciona a classe fade-out para a imagem do avião
            const aviaoImagem = imagemAviaoDiv.querySelector('.aviao-imagem');
            aviaoImagem.classList.add('fade-out');

            console.log("Classe fade-out adicionada:", aviaoImagem.classList.contains('fade-out'));

            // Atrasar a ocultação da imagem para permitir a transição
            setTimeout(() => {
                imagemAviaoDiv.style.display = "none"; // Oculta a imagem do avião
                aviacaoDiv.style.display = "flex"; // Mostra a animação
                console.log("Imagem do avião oculta e animação mostrada."); // Log de depuração

                // Iniciar a animação após torná-la visível
                aviacaoAnimacao.play(); // Começa a animação
            }, 500); // Tempo correspondente à duração da transição

            // Redireciona após a animação
            aviacaoAnimacao.addEventListener('complete', function () {
                window.location.href = "/multi_step_form"; // Redireciona para a página de formulário
            });
        }
    });
});
