(function () {
    class Cleaner {
        static consoleCleanerID = null;
        static iframe = null;
        static avatarObserver = null;

        static Init() {
            Cleaner.iframe = document.evaluate("//iframe[contains(@src, 'spribelaunch.com/aviator')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
            Cleaner.contentDocument = Cleaner.iframe ? Cleaner.iframe.contentDocument : document

            if (!Cleaner.contentDocument.body) {
                window.Scraper.exitWithMessage('Aviator frame not found. Please make sure you are on the Aviator game page.')
            }

            Cleaner.RemoveOtherBetsPanel()
            Cleaner.RemoveChat()
            Cleaner.RemoveSecondBetPanel()
            Cleaner.DisableAnimations()
            Cleaner.SuppressAvatarRequests()
            Cleaner.FilterConsoleNoise()
            Cleaner.RemoveAirstrip()
            Cleaner.RemoveBetCounting()
            Cleaner.RemoveOneWinSidebar()
            Cleaner.RemoveOneWinNav()
            Cleaner.RemoveOneWinFooter()
        }

        static RemoveOtherBetsPanel() {
            Cleaner.querySelector('app-bets-widget')?.remove()
            Cleaner.querySelector('app-bets-widget .bets-block')?.remove()
        }

        static RemoveChat() {
            Cleaner.querySelector('.chat-bar.ng-star-inserted')?.remove()
        }

        static RemoveSecondBetPanel() {
            Cleaner.querySelector('app-bet-control.double-bet.ng-star-inserted')?.remove()
        }

        static RemoveBetCounting() {
            Cleaner.querySelector('app-active-players-widget')?.remove()
        }

        static RemoveOneWinSidebar() {
            document.querySelector('.common-layout_sleave-V7jCK.variant-1_sleave-Qr2MW')?.remove()
            document.querySelector('.common-layout_sheet-V7jCK')?.remove()
            document.querySelector('.common-layout_space-V7jCK')?.remove()
        }

        static RemoveOneWinNav() {
            document.querySelector('nav.segment-control_root-ehnrM.segment-control_variant-1-ehnrM')?.remove()
        }

        static RemoveOneWinFooter() {
            document.querySelector('.footer-container_root-Xk572')?.remove()
        }

        static StartConsoleCleaning() {
            if (Cleaner.consoleCleanerID) {
                clearInterval(Cleaner.consoleCleanerID)
            }
            Cleaner.consoleCleanerID = setInterval(() => {
                console.clear()
                if (typeof window.gc === 'function') {
                    window.gc()
                }
            }, 10000)
        }

        static RemoveAirstrip() {
            Cleaner.querySelector('.play-board-wrapper')?.remove()
        }

        static DisableAnimations() {
            try {
                const style = Cleaner.contentDocument.createElement('style');
                style.textContent = '* { animation: none !important; transition: none !important; }';
                Cleaner.contentDocument.head?.appendChild(style);
            } catch (error) {

            }
        }

        static SuppressAvatarRequests() {
            const win = Cleaner.iframe?.contentWindow || window
            const doc = Cleaner.contentDocument

            if (!win || !doc) {
                return
            }

            const blockedPattern = 'aviator-next.spribegaming.com/assets/static/avatars/'
            const blankImage = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='

            const isBlockedUrl = (url) => typeof url === 'string' && url.includes(blockedPattern)

            const replaceImgSrc = (img) => {
                const src = img.currentSrc || img.src || ''
                if (isBlockedUrl(src)) {
                    img.src = blankImage
                    img.removeAttribute('srcset')
                }
            }

            const patchImagePrototype = () => {
                const imgProto = win.HTMLImageElement?.prototype
                if (!imgProto) {
                    return
                }

                try {
                    const srcDescriptor = Object.getOwnPropertyDescriptor(imgProto, 'src')
                    if (srcDescriptor?.set && !srcDescriptor.set.__cleanerWrapped__) {
                        const originalSetter = srcDescriptor.set
                        const originalGetter = srcDescriptor.get

                        const wrappedSetter = function (value) {
                            if (isBlockedUrl(value)) {
                                return originalSetter.call(this, blankImage)
                            }
                            return originalSetter.call(this, value)
                        }

                        wrappedSetter.__cleanerWrapped__ = true
                        Object.defineProperty(imgProto, 'src', {
                            get: originalGetter,
                            set: wrappedSetter,
                            configurable: srcDescriptor.configurable,
                            enumerable: srcDescriptor.enumerable
                        })
                    }
                } catch (error) {

                }

                try {
                    const srcsetDescriptor = Object.getOwnPropertyDescriptor(imgProto, 'srcset')
                    if (srcsetDescriptor?.set && !srcsetDescriptor.set.__cleanerWrapped__) {
                        const originalSetter = srcsetDescriptor.set
                        const originalGetter = srcsetDescriptor.get

                        const wrappedSetter = function (value) {
                            if (isBlockedUrl(value)) {
                                return originalSetter.call(this, '')
                            }
                            return originalSetter.call(this, value)
                        }

                        wrappedSetter.__cleanerWrapped__ = true
                        Object.defineProperty(imgProto, 'srcset', {
                            get: originalGetter,
                            set: wrappedSetter,
                            configurable: srcsetDescriptor.configurable,
                            enumerable: srcsetDescriptor.enumerable
                        })
                    }
                } catch (error) {

                }

                try {
                    if (!imgProto.setAttribute.__cleanerWrapped__) {
                        const originalSetAttribute = imgProto.setAttribute

                        imgProto.setAttribute = function (name, value) {
                            const attrName = typeof name === 'string' ? name.toLowerCase() : ''
                            if ((attrName === 'src' || attrName === 'srcset') && isBlockedUrl(value)) {
                                return originalSetAttribute.call(this, attrName, blankImage)
                            }
                            return originalSetAttribute.call(this, name, value)
                        }

                        imgProto.setAttribute.__cleanerWrapped__ = true
                    }
                } catch (error) {

                }
            }

            patchImagePrototype()

            Array.from(doc.images || []).forEach(replaceImgSrc)

            if (Cleaner.avatarObserver) {
                return
            }

            Cleaner.avatarObserver = new MutationObserver((mutations) => {
                for (const mutation of mutations) {
                    if (mutation.type === 'attributes') {
                        if (mutation.target?.tagName === 'IMG') {
                            replaceImgSrc(mutation.target)
                        }
                        continue
                    }

                    for (const node of mutation.addedNodes || []) {
                        if (node?.tagName === 'IMG') {
                            replaceImgSrc(node)
                            continue
                        }

                        if (node?.querySelectorAll) {
                            node.querySelectorAll('img').forEach(replaceImgSrc)
                        }
                    }
                }
            })

            const root = doc.documentElement || doc.body
            if (root) {
                Cleaner.avatarObserver.observe(root, {
                    childList: true,
                    subtree: true,
                    attributes: true,
                    attributeFilter: ['src', 'srcset']
                })
            }
        }

        static FilterConsoleNoise() {
            const win = Cleaner.iframe?.contentWindow || window

            if (!win || !win.fetch) {
                return
            }

            if (!win.fetch.__cleanerWrapped__) {
                const originalFetch = win.fetch.bind(win)

                const wrappedFetch = (...args) => {
                    return originalFetch(...args).catch(() => {
                        const request = args[0]
                        const url = request?.url || request?.toString?.() || 'unknown'
                        console.log(`Safely swallowed blocked fetch: ${url}`)

                        return new Response(JSON.stringify({ intercepted: true, status: 'blocked-but-hidden' }), {
                            status: 200,
                            headers: { 'Content-Type': 'application/json' }
                        })
                    })
                }

                wrappedFetch.__cleanerWrapped__ = true
                win.fetch = wrappedFetch
            }

            if (win.XMLHttpRequest && !win.XMLHttpRequest.__cleanerWrapped__) {
                const OriginalXHR = win.XMLHttpRequest

                function CleanerXHR() {
                    const xhr = new OriginalXHR()
                    const originalSend = xhr.send

                    xhr.send = function (...sendArgs) {
                        try {
                            xhr.addEventListener('error', () => {
                                const url = xhr.responseURL || 'unknown'
                                console.log(`Safely swallowed blocked XHR: ${url}`)
                            }, { once: true })
                        } catch (error) {

                        }

                        return originalSend.apply(xhr, sendArgs)
                    }

                    return xhr
                }

                CleanerXHR.__cleanerWrapped__ = true
                CleanerXHR.prototype = OriginalXHR.prototype
                win.XMLHttpRequest = CleanerXHR
            }
        }

        static querySelector(selector) {
            return Cleaner.contentDocument.querySelector(selector);
        }
    }

    window.Cleaner = Cleaner
})()