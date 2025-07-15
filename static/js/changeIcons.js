document.addEventListener("DOMContentLoaded", function () {
	const arrows = document.querySelectorAll("[data-arrow]");

	arrows.forEach((icon) => {
		const targetId = icon.getAttribute("data-arrow");
		const collapseElement = document.getElementById(targetId);

		collapseElement.addEventListener("show.bs.collapse", () => {
			icon.classList.remove("bi-chevron-down");
			icon.classList.add("bi-chevron-right");
		});

		collapseElement.addEventListener("hide.bs.collapse", () => {
			icon.classList.remove("bi-chevron-right");
			icon.classList.add("bi-chevron-down");
		});
	});
});
