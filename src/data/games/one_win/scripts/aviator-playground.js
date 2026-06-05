(function () {
    class Playground {
        load() {
            this.STATES = Object.freeze({
                WAITING: 'waiting',
                BET_PLACED: 'bet_placed',
                CRASHED: 'crashed',
            })

            this.iframe = document.evaluate("//iframe[contains(@src, 'spribelaunch.com/aviator')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            this.contentDocument = this.iframe ? this.iframe.contentDocument : document;

            this.payoutsBlock = this.querySelector('.payouts-block')
        
            this.config(1.8)
        }

        bet() {
            this.querySelector('.btn.btn-success.bet.ng-star-inserted')?.click()
        }

        config(autoCashout) {
            const autoTab = this.querySelectorAsxPath("//button[contains(@class,'tab') and contains(text(),'Auto')]")
            
            if (autoTab) autoTab.click()
        }

        querySelector(selector) {
            return this.contentDocument.querySelector(selector)
        }

        querySelectorAsxPath(xpath) {
            return document.evaluate(xpath, this.contentDocument, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }
    }

    window.Playground = new Playground()
})()