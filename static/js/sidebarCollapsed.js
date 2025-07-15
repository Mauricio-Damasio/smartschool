document.addEventListener("DOMContentLoaded", function () {
	const toggleBtn = document.getElementById("sidebarCollapse");
	const sidebar = document.getElementById("sidebar");
	const icon = toggleBtn.querySelector("i");

	toggleBtn.addEventListener("click", function () {
		sidebar.classList.toggle("active");

		// Muda o ícone do botão
		if (sidebar.classList.contains("active")) {
			icon.classList.remove("bi-list");
			icon.classList.add("bi-x-lg");
		} else {
			icon.classList.remove("bi-x-lg");
			icon.classList.add("bi-list");
		}
	});
});
