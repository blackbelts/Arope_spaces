menuItem = null
window.addEventListener('locationchange', function () {
    var url = window.location.hash,
        action = url.indexOf("action="),
        split = url.indexOf('&', action),
        actionId = url.substring(action + 7, split)
    if (menuItem == null) {
        console.log("if 1")
        console.log(action)
        if (action != -1) {
            menuItem = document.querySelector('[data-action-id="' + actionId + '"]')
            if(menuItem != null){
                menuItem.style.backgroundColor = "#073e89"
                menuItem.style.color = "white"
            }
        }
    }
    /*  console.log(menuItem) */
    if (menuItem != null) {
        console.log("if 2")
       if(action!=-1){
        menuItem.style.backgroundColor = "transparent"
        menuItem.style.color = "black"
        menuItem = document.querySelector('[data-action-id="' + actionId + '"]')
        if(menuItem != null){
            menuItem.style.backgroundColor = "#073e89"
            menuItem.style.color = "white"
        }
       }
        /*         console.log("if")
         */

    }


})
history.pushState = (f => function pushState() {
    var ret = f.apply(this, arguments);
    window.dispatchEvent(new Event('pushstate'));
    window.dispatchEvent(new Event('locationchange'));
    return ret;
})(history.pushState);

history.replaceState = (f => function replaceState() {
    var ret = f.apply(this, arguments);
    window.dispatchEvent(new Event('replacestate'));
    window.dispatchEvent(new Event('locationchange'));
    return ret;
})(history.replaceState);
window.addEventListener('popstate', () => {
    window.dispatchEvent(new Event('locationchange'))
});