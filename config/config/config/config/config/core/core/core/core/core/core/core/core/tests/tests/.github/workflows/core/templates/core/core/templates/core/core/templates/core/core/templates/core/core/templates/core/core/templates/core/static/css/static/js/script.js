document.addEventListener("DOMContentLoaded", function () {

    // Confirmação antes de excluir um registro
    const botoesExcluir = document.querySelectorAll("[data-confirmar-exclusao]");

    botoesExcluir.forEach(function (botao) {
        botao.addEventListener("click", function (evento) {
            const confirmar = window.confirm(
                "Tem certeza de que deseja excluir este registro?"
            );

            if (!confirmar) {
                evento.preventDefault();
            }
        });
    });

    // Fecha mensagens automaticamente após alguns segundos
    const mensagens = document.querySelectorAll(".alert");

    mensagens.forEach(function (mensagem) {
        setTimeout(function () {
            if (mensagem.classList.contains("show")) {
                mensagem.classList.remove("show");
            }

            mensagem.style.transition = "opacity 0.5s ease";
            mensagem.style.opacity = "0";

            setTimeout(function () {
                mensagem.remove();
            }, 500);

        }, 5000);
    });

    // Impede o envio de formulários com campos obrigatórios vazios
    const formularios = document.querySelectorAll("form");

    formularios.forEach(function (formulario) {
        formulario.addEventListener("submit", function (evento) {
            if (!formulario.checkValidity()) {
                evento.preventDefault();
                formulario.reportValidity();
            }
        });
    });

});
