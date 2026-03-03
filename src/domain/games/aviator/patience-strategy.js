const STATES = Object.freeze({
    WAITING: 'waiting',
    BET_PLACED: 'bet_placed',
    CRASHED: 'crashed',
})

const AviatorDomain = window.AviatorDomain;

class PatienceStrategy {

    constructor() {
        this.strategy = JSON.parse("[strategy]")

        this.state = STATES.WAITING

        this.autoWithdrawal = this.strategy.user.autoWithdrawal
        this.amount = this.strategy.user.betAmount
        this.martingaleAttempts = this.strategy.user.martingaleAttempts

        this.totalLost = 0
        this.martingaleAttemptsCount = 0
        this.amountToBet = this.amount
    }

    setControl(controlTab) {
        this.controlTab = controlTab
    }

    setQuerySelector(querySelector) {
        this.querySelector = querySelector
    }

    _configureControl() {
        this.controlTab.enableAutoCashout(this.strategy.user.autoWithdrawal)
        this.controlTab.setAmount(this.amountToBet)
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

        window.Observer.execute(payoutsBlock, (multiplier) => {
            let canTrigger = true

            if (this.state == STATES.BET_PLACED) {
                if (AviatorDomain.getResult(multiplier, this.autoWithdrawal) == 'WON') {
                    this.state = STATES.WAITING

                    this.martingaleAttemptsCount = 0
                    this.totalLost = 0
                    this.amountToBet = this.amount

                    window.invokeLogMessage(`Bet won! Resetting to initial amount.`)

                    if (AviatorDomain.isPurple(multiplier) || AviatorDomain.isPink(multiplier)) {
                        window.invokeLogMessage(`Won on Purple/Pink! Skipping this multiplier as a trigger.`)
                        canTrigger = false
                    }
                } else {
                    if (this.martingaleAttemptsCount >= this.martingaleAttempts) {
                        this.state = STATES.WAITING

                        this.totalLost = 0
                        this.amountToBet = this.amount
                        this.martingaleAttemptsCount = 0

                        window.invokeLogMessage(`Martingale attempts exhausted. Resetting to initial amount.`)
                    } else {
                        this.state = STATES.WAITING

                        this.totalLost += parseFloat(this.amountToBet)
                        this.amountToBet = this.totalLost / (parseFloat(this.autoWithdrawal) - 1)
                        this.martingaleAttemptsCount++

                        window.invokeLogMessage(`Martingale attempt ${this.martingaleAttemptsCount}. Waiting for next purple to bet ${this.amountToBet}`)
                    }
                    canTrigger = false
                }

                this.controlTab.setAmount(this.amountToBet)
            }

            if (this.state == STATES.WAITING && canTrigger) {
                if (AviatorDomain.isPurple(multiplier)) {
                    this.controlTab.bet()
                    this.state = STATES.BET_PLACED

                    window.invokeLogMessage(`Purple/Pink passed! Bet placed! Amount: ${this.amountToBet}`)
                }
            }

            this._prunePayouts(payoutsBlock)
        })
    }
}

window.Strategy = PatienceStrategy
