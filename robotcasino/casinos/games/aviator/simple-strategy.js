const AviatorDomain = window.AviatorDomain;

class SimpleStrategy {

    constructor(strategy) {
        this.controlTab = null
        this.strategy = JSON.parse(strategy)

        this.blueCount = 0
        this.purpleCount = 0
        this.pinkCount = 0

        this.watcher = []
    }

    setControl(controlTab) {
        this.controlTab = controlTab
    }

    _configureControl() {
        this.controlTab.enableAutoCashout(this.strategy.user.autoWithdrawal)
        this.controlTab.setAmount(this.strategy.user.betAmount)
    }

    execute(operation) {
        if (this.controlTab == null) {
            
        }

        const payoutsBlock = querySelector('.payouts-block')
        const watcher = [...operation.matchAll(/\[(\w+)\]/g)].map(match => match[1])

        if (payoutsBlock == null) {
            throw new Error('Payouts block not found')
        }

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        const content = node.textContent.trim()
                        const multiplier = content.replace('x', '')

                        const parsedMultiplier = parseFloat(multiplier)
                        let multiplierName = null

                        if (isBlue(parsedMultiplier)) {
                            this.blueCount++

                            multiplierName = 'blue_count'
                        } else if (isPurple(parsedMultiplier)) {
                            this.purpleCount++

                            multiplierName = 'purple_count'
                        } else if (isPink(parsedMultiplier)) {
                            this.pinkCount++

                            multiplierName = 'pink_count'
                        }

                        const parsedOperation = operation.replace(/\[(\w+)\]/g, (match, key) => {
                            switch (key) {
                                case 'purple_count': return this.purpleCount
                                case 'blue_count': return this.blueCount
                                case 'pink_count': return this.pinkCount
                                default: return match
                            }
                        })

                        const result = eval(parsedOperation)

                        if (!result && !watcher.includes(multiplierName)) {                         
                            this.blueCount = 0
                            this.purpleCount = 0
                            this.pinkCount = 0

                            return
                        } else if (!result) {
                            return
                        }

                        this.controlTab.bet()
                        this.blueCount = 0
                        this.purpleCount = 0
                        this.pinkCount = 0

                        window._invokeLogMessage(`Bet placed!`)
                    }
                })
            })
        })

        observer.observe(payoutsBlock, {
            childList: true,
            subtree: false
        })
    }
}