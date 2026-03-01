const STATES = Object.freeze({
    WAITING: 'waiting',
    BET_PLACED: 'bet_placed',
    CRASHED: 'crashed',
})

const AviatorDomain = window._AviatorDomain;

class SimpleStrategy {

    constructor() {
        this.strategy = JSON.parse("[strategy]")

        this.blueCount = 0
        this.purpleCount = 0
        this.pinkCount = 0

        this.state = STATES.WAITING

        this.autoWithdrawal = this.strategy.user.autoWithdrawal
        this.amount = this.strategy.user.betAmount
        this.martingaleAttempts = this.strategy.user.martingaleAttempts
        this.martingaleMultiplier = this.strategy.user.martingaleMultiplier

        this.operation = this.strategy.operation
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

    _resetCounts() {
        this.blueCount = 0
        this.purpleCount = 0
        this.pinkCount = 0
    }

    _prunePayouts() {
        const payoutsFullBlock = this.querySelector('.wrapper .payouts-block')
        const payoutsInlineBlock = this.querySelector('.payouts-wrapper .payouts-block')

        Array.from(payoutsFullBlock.children).slice(5).forEach(el => el.remove());
        Array.from(payoutsInlineBlock.children).slice(5).forEach(el => el.remove());
    }

    execute() {
        this._configureControl()

        const payoutsBlock = this.querySelector('.payouts-block')
        const scores = [...this.operation.matchAll(/\[(\w+)\]/g)].map(match => match[1])
        let martingaleAttempts = 0
        let totalLost = 0
        let amount = this.amount

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        const multiplier = parseFloat(node.textContent.trim().replace('x', ''))
                        let multiplierName = null

                        if (this.state == STATES.BET_PLACED) {
                            if (AviatorDomain.getResult(multiplier, this.autoWithdrawal) == 'WON') {
                                this.state = STATES.WAITING
                                window._invokeWaitingMessage()

                                martingaleAttempts = 0
                                totalLost = 0
                                amount = this.amount
                            } else {
                                if (martingaleAttempts >= this.martingaleAttempts) {
                                    this.state = STATES.WAITING
                                    window._invokeWaitingMessage()

                                    totalLost = 0
                                    amount = this.amount
                                    martingaleAttempts = 0
                                } else {

                                    this.state = STATES.CRASHED

                                    totalLost += parseFloat(amount)
                                    amount = totalLost / (parseFloat(this.autoWithdrawal) - 1)
                                    martingaleAttempts++
                                }
                            }

                            this.controlTab.setAmount(amount)
                        }

                        if (this.state == STATES.CRASHED) {

                            this.controlTab.bet()

                            this.state = STATES.BET_PLACED
                            window._invokeBetMessage(amount)

                            return
                        }

                        if (AviatorDomain.isBlue(multiplier)) {
                            this.blueCount++

                            multiplierName = 'blue_count'
                        } else if (AviatorDomain.isPurple(multiplier)) {
                            this.purpleCount++

                            multiplierName = 'purple_count'
                        } else if (AviatorDomain.isPink(multiplier)) {
                            this.pinkCount++

                            multiplierName = 'pink_count'
                        }

                        const parsedOperation = this.operation.replace(/\[(\w+)\]/g, (match, key) => {
                            switch (key) {
                                case 'purple_count': return this.purpleCount
                                case 'blue_count': return this.blueCount
                                case 'pink_count': return this.pinkCount
                                default: return match
                            }
                        })

                        const result = eval(parsedOperation)

                        window._invokeLogMessage(`Operation: ${parsedOperation}`)
                        window._invokeLogMessage(`Operation result: ${result}`)

                        if (!result && !scores.includes(multiplierName)) {
                            this._resetCounts()

                            this.state = STATES.WAITING
                            window._invokeWaitingMessage()
                        } else if (result) {
                            this.controlTab.bet()
                            this._resetCounts()

                            this.state = STATES.BET_PLACED
                            window._invokeBetMessage(amount)
                        }

                        this._prunePayouts(payoutsBlock)
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