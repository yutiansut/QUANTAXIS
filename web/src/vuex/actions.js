/*主页面涉及到的actions*/
let noop = () => {}
/*显示浮层alert*/
export const showAlert = ({dispatch}, message = '') => {
    if(!message) {
        return false
    }
    dispatch('SHOW_ALERT', {
        type: 'alert',
        message: message,
        onClose: noop
    })
}
/*显示浮层confirm*/
export const showConfirm = ({dispatch}, data = {}) => {
    if(!data.message) {
        return false
    }
    data.type = 'confirm'
    if(typeof data.onClose != 'function') {
        data.onClose = noop
    }
    if(typeof data.onConfirm != 'function') {
        data.onConfirm = noop
    }
    dispatch('SHOW_ALERT', data)
}
/*隐藏浮层*/
export const hideAlert = ({dispatch}) => dispatch('HIDE_ALERT')