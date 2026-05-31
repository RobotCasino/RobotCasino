(function() {
    class Util {
        static observe(target, callback) {
            const element = document.querySelector(target)

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

    window.Util = Util
})()