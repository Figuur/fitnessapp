document.addEventListener("DOMContentLoaded", () => {
    // Voeg 4 lege placeholders toe aan elke gallery-container
    const containers = document.querySelectorAll(".gallery-container");
    containers.forEach((container) => {
        for (let i = 0; i < 4; i++) {
            const emptyTile = document.createElement("div");
            emptyTile.className = "card-container empty-tile";
            emptyTile.setAttribute("draggable", "true");
            container.appendChild(emptyTile);
        }
    });

    // Initialiseer drag & drop voor alle items
    const items = document.querySelectorAll(".card-container");
    let draggedItem = null;

    items.forEach((item) => {
        // Drag start event
        item.addEventListener("dragstart", function (e) {
            draggedItem = this;
            setTimeout(() => this.classList.add("dragging"), 0);
        });

        // Drag end event
        item.addEventListener("dragend", function () {
            this.classList.remove("dragging");
            draggedItem = null;
        });

        // Drag over event
        item.addEventListener("dragover", function (e) {
            e.preventDefault();
        });

        // Drop event
        item.addEventListener("drop", function (e) {
            e.preventDefault();
            if (this !== draggedItem) {
                let allItems = [
                    ...document.querySelectorAll(".card-container"),
                ];
                let draggedIndex = allItems.indexOf(draggedItem);
                let droppedIndex = allItems.indexOf(this);

                if (draggedIndex < droppedIndex) {
                    this.parentNode.insertBefore(draggedItem, this.nextSibling);
                } else {
                    this.parentNode.insertBefore(draggedItem, this);
                }
            }
        });
    });
});
