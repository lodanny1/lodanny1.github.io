function openSite(menu) {
    const url = menu.value;
    if (url) {
        window.open(url, "_blank");
    }
}

function openSiteFromMenu2() {
    const menu = document.getElementById("menu2");
    const url = menu.value;
    if (url) {
        window.open(url, "_blank"); 
    } else {
        alert("Please select an option from the dropdown.");
    }
}
