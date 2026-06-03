(function() {
    class Util {
        observe(element, callback) {
            if (!element) {
                return null
            }

            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            callback(node, mutation)
                        }
                    })
                })
            })

            observer.observe(element, {
                attributes: true,
                childList: true,
                characterData: true,
                subtree: true,
            })
        }
    }

    window.Util = new Util()
})()