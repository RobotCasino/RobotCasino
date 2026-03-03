const STATES = Object.freeze({
    WAITING: 'waiting',
    BET_PLACED: 'bet_placed',
    CRASHED: 'crashed',
})

const AviatorDomain = window.AviatorDomain;

class TendencyStrategy {

    constructor() {
        this.strategy = JSON.parse("[strategy]")

        this.state = STATES.WAITING

        this.autoWithdrawal = this.strategy.user.autoWithdrawal
        this.amount = this.strategy.user.betAmount
        this.martingaleAttempts = this.strategy.user.martingaleAttempts

        this.totalLost = 0
        this.martingaleAttemptsCount = 0
        this.amountToBet = this.amount

        this.history = []
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

        if (payoutsFullBlock) Array.from(payoutsFullBlock.children).slice(5).forEach(el => el.remove());
        if (payoutsInlineBlock) Array.from(payoutsInlineBlock.children).slice(5).forEach(el => el.remove());
    }

    _isGreatPossibility() {
        if (this.history.length < 3) return false;

        const m1 = parseFloat(this.history[0]); // newest
        const m2 = parseFloat(this.history[1]);
        const m3 = parseFloat(this.history[2]); // oldest of the 3

        // 1. Bullish Trend (Higher Highs): each result is getting bigger
        const isBullish = m1 > m2 && m2 > m3;

        // 2. Resistance Breakout (breaks 2.50x resistance)
        const isBreakout = m1 > 2.50 && m2 <= 2.50;

        return isBullish || isBreakout;
    }

    execute() {
        this._configureControl()

        const payoutsBlock = this.querySelector('.payouts-block')

        window.Observer.execute(payoutsBlock, (multiplier) => {
            let canTrigger = true

            this.history.unshift(multiplier)
            if (this.history.length > 20) {
                this.history.pop()
            }

            if (this.state == STATES.BET_PLACED) {
                if (AviatorDomain.getResult(multiplier, this.autoWithdrawal) == 'WON') {
                    this.state = STATES.WAITING

                    this.martingaleAttemptsCount = 0
                    this.totalLost = 0
                    this.amountToBet = this.amount

                    window.invokeLogMessage(`Bet won! Resetting to initial amount.`)

                    canTrigger = false
                } else {
                    if (this.martingaleAttemptsCount >= this.martingaleAttempts) {
                        this.state = STATES.WAITING

                        this.totalLost = 0
                        this.amountToBet = this.amount
                        this.martingaleAttemptsCount = 0

                        window.invokeLogMessage(`Martingale attempts exhausted. Resetting to initial amount.`)
                    } else {
                        // Wait for another tendency trigger to bet to recover losses
                        this.state = STATES.WAITING

                        this.totalLost += parseFloat(this.amountToBet)
                        this.amountToBet = this.totalLost / (parseFloat(this.autoWithdrawal) - 1)
                        this.martingaleAttemptsCount++

                        window.invokeLogMessage(`Martingale attempt ${this.martingaleAttemptsCount}. Waiting for next tendency pattern to bet ${this.amountToBet}`)
                    }
                    canTrigger = false
                }

                this.controlTab.setAmount(this.amountToBet)
            }

            if (this.state == STATES.WAITING && canTrigger) {
                if (this._isGreatPossibility()) {
                    this.controlTab.bet()
                    this.state = STATES.BET_PLACED

                    window.invokeLogMessage(`Tendency pattern detected! Bet placed! Amount: ${this.amountToBet}`)
                }
            }

            this._prunePayouts()
        })
    }
}

window.Strategy = TendencyStrategy
