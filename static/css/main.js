function firstFunction() {
    let title_products = document.getElementById("titleId")
//    console.log(title_products.innerHTML)
    if (title_products.style.color === 'black') {
        title_products.style.color = 'green'
    }
    else {
        title_products.style.color = 'black'

    }
}
