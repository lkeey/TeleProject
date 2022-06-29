function Raising() {
    const graphs = document.querySelectorAll(".item .col");
    console.log("ALL:", graphs)

    for (var graph in graphs) {
        graph.setAttribute("height", 100)
    }
}