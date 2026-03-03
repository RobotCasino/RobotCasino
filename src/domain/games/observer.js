class Observer {
    /**
     * Observes a DOM element for added child element nodes.
     * For each new element, it parses a multiplier from the node's text
     * (stripping the trailing 'x') and invokes the provided callback.
     *
     * @param {Element} element - The DOM element to observe.
     * @param {function(number): void} callback - Called with the parsed multiplier.
     */
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