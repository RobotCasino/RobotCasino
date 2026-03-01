class SimpleStrategy extends Strategy {

    constructor() {
        this.controlTab = null
        this.querySelector = null

        this.strategy = JSON.parse("[strategy]")

        this.AviatorDomain = window._AviatorDomain;

        this.blueCount = 0
        this.purpleCount = 0
        this.pinkCount = 0

        this.watcher = []

        this.states = Object.freeze({
            WAITING: 'waiting',
            BET_PLACED: 'bet_placed',
            CRASHED: 'crashed',
        })
    }

    setControl(controlTab) {
        this.controlTab = controlTab
    }

    setQuerySelector(querySelector) {
        this.querySelector = querySelector
    }

    _configureControl() {
        this.controlTab.enableAutoCashout(this.strategy.user.autoWithdrawal)
        this.controlTab.setAmount(this.strategy.user.betAmount)
    }

    execute() {
        let state = this.states.WAITING

        const payoutsBlock = this.querySelector('.payouts-block')
        const watcher = [...this.strategy.operation.matchAll(/\[(\w+)\]/g)].map(match => match[1])

        if (payoutsBlock == null) {
            throw new Error('Payouts block not found')
        }

        this._configureControl()

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        const content = node.textContent.trim()
                        const multiplier = content.replace('x', '')

                        const parsedMultiplier = parseFloat(multiplier)
                        let multiplierName = null

                        if (state == this.states.BET_PLACED && this.AviatorDomain) {
                        }

                        if (this.AviatorDomain.isBlue(parsedMultiplier)) {
                            this.blueCount++

                            multiplierName = 'blue_count'
                        } else if (this.AviatorDomain.isPurple(parsedMultiplier)) {
                            this.purpleCount++

                            multiplierName = 'purple_count'
                        } else if (this.AviatorDomain.isPink(parsedMultiplier)) {
                            this.pinkCount++

                            multiplierName = 'pink_count'
                        }

                        const parsedOperation = this.strategy.operation.replace(/\[(\w+)\]/g, (match, key) => {
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

                        state = this.states.BET_PLACED

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

window._Strategy = SimpleStrategy