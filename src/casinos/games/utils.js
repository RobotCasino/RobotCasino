window._invokeFatalError = () => {
    console.log('[stop]')
}

window._invokeLogMessage = (msg) => {
    console.log(`[log] ${msg}`)
}

window._invokeBetMessage = (amount) => {
    console.log(`[bet] ${amount}`)
}

window._invokeWaitingMessage = () => {
    console.log(`[waiting]`)
}