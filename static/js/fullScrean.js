document.addEventListener("DOMContentLoaded", function () {
	const fullscreenToggle = document.getElementById("fullscreen-toggle");
	const iconMax = document.getElementById("icon-maximize");
	const iconMin = document.getElementById("icon-minimize");

	fullscreenToggle.addEventListener("click", function (e) {
		e.preventDefault();

		if (!document.fullscreenElement && !document.webkitFullscreenElement) {
			// Entrar em tela cheia
			const el = document.body; // ou outro elemento que queira colocar em fullscreen
			if (el.requestFullscreen) {
				el.requestFullscreen();
			} else if (el.webkitRequestFullscreen) {
				el.webkitRequestFullscreen(); // Safari
			}

			iconMax.style.display = "none";
			iconMin.style.display = "inline";
		} else {
			// Sair da tela cheia
			if (document.exitFullscreen) {
				document.exitFullscreen();
			} else if (document.webkitExitFullscreen) {
				document.webkitExitFullscreen(); // Safari
			}

			iconMax.style.display = "inline";
			iconMin.style.display = "none";
		}
	});
});
