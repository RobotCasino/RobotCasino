(function() {
    class CasinoCleaner {
        start() {
            this.removeSidebar()
            this.removeNav()
            this.removeFooter()
        }

        removeSidebar() {
            document.querySelector('.common-layout_sleave-V7jCK.variant-1_sleave-Qr2MW')?.remove()
            document.querySelector('.common-layout_sheet-V7jCK')?.remove()
            document.querySelector('.common-layout_space-V7jCK')?.remove()
        }

        removeNav() {
            document.querySelector('nav.segment-control_root-ehnrM.segment-control_variant-1-ehnrM')?.remove()
        }

        removeFooter() {
            document.querySelector('.footer-container_root-Xk572')?.remove()
        }
    }

    window.CasinoCleaner = new CasinoCleaner()
})()