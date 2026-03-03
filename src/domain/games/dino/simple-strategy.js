const STATES = Object.freeze({
    WAITING: 'waiting',
    BET_PLACED: 'bet_placed',
    CRASHED: 'crashed',
})

const AviatorDomain = window.AviatorDomain;

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

    _prunePayouts(container, maxChildren = 5) {
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
        let amount = this.amount

        window.Observer.execute(payoutsBlock, (multiplier) => {
            let multiplierName = null

            if (this.state == STATES.BET_PLACED) {
                if (AviatorDomain.getResult(multiplier, this.autoWithdrawal) == 'WON') {
                    this.state = STATES.WAITING

                    martingaleAttempts = 0
                    amount = this.amount

                    window.invokeLogMessage(`Bet won! Resetting to initial amount.`)
                } else {
                    if (martingaleAttempts >= this.martingaleAttempts) {
                        this.state = STATES.WAITING

                        amount = this.amount
                        martingaleAttempts = 0

                        window.invokeLogMessage(`Martingale attempts exhausted. Resetting to initial amount.`)
                    } else {

                        this.state = STATES.CRASHED

                        amount *= this.martingaleMultiplier
                        martingaleAttempts++

                        window.invokeLogMessage(`Martingale attempt ${martingaleAttempts}`)
                    }
                }

                this.controlTab.setAmount(amount)
            }

            if (this.state == STATES.CRASHED) {
                window.invokeLogMessage(`Bet placed in Martingale state! Amount: ${amount}`)

                this.controlTab.bet()

                this.state = STATES.BET_PLACED

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

            window.invokeLogMessage(`Operation: ${parsedOperation}`)
            window.invokeLogMessage(`Operation result: ${result}`)

            if (!result && !scores.includes(multiplierName)) {
                this._resetCounts()

                window.invokeLogMessage(`Resetting counts!`)

                this.state = STATES.WAITING
            } else if (result) {
                this.controlTab.bet()
                this._resetCounts()

                this.state = STATES.BET_PLACED

                window.invokeLogMessage(`Bet placed!`)
            }

            this._prunePayouts(payoutsBlock)
        })
    }
}

window.Strategy = SimpleStrategy