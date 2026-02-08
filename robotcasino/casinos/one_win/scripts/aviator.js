function querySelector(element) {
    return document.querySelector('iframe').contentWindow.document.body.querySelector(element)
}

function isBlue(multiplier) {
    return multiplier >= 1 && multiplier < 2
}

function isPurple(multiplier) {
    return multiplier >= 2 && multiplier < 10
}

function isPink(multiplier) {
    return multiplier >= 10
}

class SimpleStrategy {

    constructor(controlTab) {
        this.controlTab = controlTab

        this.blueCount = 0
        this.purpleCount = 0
        this.pinkCount = 0

        this.watcher = []
    }

    execute(operation) {
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

class UnionStrategy {

    constructor(controlTab) {
        this.controlTab = controlTab
    }

    execute() {
        console.log('Executing union strategy')
    }
}


class ControlTab {
    constructor(selector) {
        this.control = querySelector(selector)

        if (this.control == null) {
            throw new Error('Control tab not found')
        }

        this.amountInput = this.control.querySelector('input[inputmode="decimal"]')
    }

    setAmount(amount) {
        this._setValue(this.amountInput, amount.toString())
    }

    enableAutoCashout(amount) {
        const autoModeSwitch = this.control.querySelector('.navigation-switcher .tab:nth-child(2)')
        const autoCashoutSwitch = this.control.querySelector('.cash-out-switcher .input-switch')
        const autoCashoutInput = this.control.querySelector('.second-row input[inputmode="decimal"]')

        if (autoModeSwitch == null || autoCashoutSwitch == null || autoCashoutInput == null) {
            throw new Error('Auto cashout elements not found')
        }

        autoModeSwitch.click()

        if (autoCashoutSwitch.classList.contains('off')) {
            autoCashoutSwitch.click()
        }

        this._setValue(autoCashoutInput, amount.toString())
    }

    bet() {
        this.control.querySelector('button.btn.bet.ng-star-inserted').click()
    }

    _setValue(input, value) {
        if (typeof value !== 'string') {
            return
        }

        input.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }))
        input.focus()

        input.value = ''
        input.dispatchEvent(new Event('input', { bubbles: true }))
        input.value = value

        const lastChar = value.slice(-1)
        input.dispatchEvent(new KeyboardEvent('keydown', { key: lastChar, bubbles: true }))
        input.dispatchEvent(new Event('input', { bubbles: true }))
        input.dispatchEvent(new KeyboardEvent('keyup', { key: lastChar, bubbles: true }))
        input.dispatchEvent(new Event('change', { bubbles: true }))
        input.dispatchEvent(new FocusEvent('blur', { bubbles: true }))

        document.body.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }))
        input.blur()
        document.body.focus()
    }
}

(async function () {
    const strategy = [strategy]

    let primaryNode = querySelector('.payouts-block')

    while (primaryNode == null) {
        await new Promise(resolve => setTimeout(resolve, 1000))

        primaryNode = querySelector('.payouts-block')
    }

    const controlTab = new ControlTab('.bet-control.double-bet')
    controlTab.enableAutoCashout(strategy.user.autoWithdrawal)
    controlTab.setAmount(strategy.user.betAmount)

    switch (strategy.method) {
        case 'simple':

            if (strategy.operation == null) {
                window._invokeFatalError()
                return
            }

            new SimpleStrategy(controlTab).execute(strategy.operation)

            break
        case 'union':
            new UnionStrategy(controlTab).execute()

            break
    }
})()