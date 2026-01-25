function querySelector(element) {
    return document.querySelector('iframe').contentWindow.document.body.querySelector(element)
}

(async function() {
    const strategy = JSON.parse([strategy]);

    let targetNode = querySelector('.payouts-block');

    while (targetNode == null) {
     await new Promise(resolve => setTimeout(resolve, 1000));    
    
     targetNode = querySelector('.payouts-block');
    }

    
})();