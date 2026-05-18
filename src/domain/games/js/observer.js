class Observer {

    static execute(element, callback) {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        const multiplier = parseFloat(node.textContent.trim().replace('x', ''))
                        callback(multiplier)
                    }
                })
            })
        })

        observer.observe(element, {
            childList: true,
            subtree: false
        })

        return observer
    }
}

window.Observer = Observer;