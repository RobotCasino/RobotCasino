window.invokeFatalError = () => {
    console.log('[stop]')
}

window.invokeLogMessage = (msg) => {
    console.log(`[log] ${msg}`)
}

window.invokeBetMessage = (amount) => {
    console.log(`[bet] ${amount}`)
}

window.invokeWaitingMessage = () => {
    console.log(`[waiting]`)
}