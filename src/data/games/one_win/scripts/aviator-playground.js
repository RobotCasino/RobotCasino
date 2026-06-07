(function () {
    class Playground {
        constructor() {
            this.iframe = this.querySelectorAsxPath("//iframe[contains(@src, 'spribelaunch.com/aviator')]", document);

            this.iframeDocument = this.iframe.contentDocument;
        }

        load() {
            this.STATES = Object.freeze({
                WAITING: 'waiting',
                BET_PLACED: 'bet_placed',
                CRASHED: 'crashed',
            })

            this.payoutsBlock = this.querySelector('.payouts-block', this.iframeDocument)
        
            this.config(1.8)
        }

        bet() {
            this.querySelector('.btn.btn-success.bet.ng-star-inserted', this.iframeDocument)?.click()
        }

        config(autoCashout) {
            const autoTab = this.querySelectorAsxPath("//button[contains(@class,'tab') and contains(text(),'Auto')]", this.iframeDocument)
            
            if (autoTab) autoTab.click()
        }

        querySelector(selector, contextNode) {
            return contextNode.querySelector(selector)
        }

        querySelectorAsxPath(xpath, contextNode) {
            return document.evaluate(xpath, contextNode, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }
    }

    window.Playground = new Playground()
})()