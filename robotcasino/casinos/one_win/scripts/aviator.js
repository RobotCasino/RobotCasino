
function querySelector(element) {
    return document.querySelector('iframe').contentWindow.document.body.querySelector(element)
}

class ControlTab {
    constructor(selector) {
        this.control = querySelector(selector);

        if (this.control == null) {
            throw new Error('Control tab not found');
        }

        this.amountInput = this.control.querySelector('input[inputmode="decimal"]');
    }

    setAmount(amount) {
        this._setValue(this.amountInput, amount.toString());
    }

    enableAutoCashout(amount) {
        const autoModeSwitch = this.control.querySelector('.navigation-switcher .tab:nth-child(2)')
        const autoCashoutSwitch = this.control.querySelector('.cash-out-switcher .input-switch')
        const autoCashoutInput = this.control.querySelector('.second-row input[inputmode="decimal"]');

        if (autoModeSwitch == null || autoCashoutSwitch == null || autoCashoutInput == null) { 
            throw new Error('Auto cashout elements not found');
        }

        autoModeSwitch.click();

        if (autoCashoutSwitch.classList.contains('off')) {
            autoCashoutSwitch.click();
        }

        this._setValue(autoCashoutInput, amount.toString());
    }

    bet() {
        this.control.querySelector('button.btn.bet.ng-star-inserted').click();
    }

    _setValue(input, value) {
        if (typeof value !== 'string') {
            return;
        }

        input.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
        input.focus();

        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.value = value;

        const lastChar = value.slice(-1);
        input.dispatchEvent(new KeyboardEvent('keydown', { key: lastChar, bubbles: true }));
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new KeyboardEvent('keyup', { key: lastChar, bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        input.dispatchEvent(new FocusEvent('blur', { bubbles: true }));

        document.body.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
        input.blur();
        document.body.focus();
    }
}

(async function () {
    const strategy = JSON.parse([strategy]);

    let primaryNode = querySelector('.payouts-block');

    while (primaryNode == null) {
        await new Promise(resolve => setTimeout(resolve, 1000));

        primaryNode = querySelector('.payouts-block');
    }

    controlTab = new ControlTab('.bet-control.double-bet');
    controlTab.enableAutoCashout('1.5');
    controlTab.setAmount('4');
})();