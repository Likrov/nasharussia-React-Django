import {backendLookup} from '../lookup'

export function apiNash_messageCreate(newNash_message, callback){
    backendLookup("POST", "/nash-message/create/", callback, {content: newNash_message})
  }

export function apiNash_messageAction(nash_messageId, action, callback){
    const data = {id: nash_messageId, action: action}
    backendLookup("POST", "/nash-message/action/", callback, data)
}

export function apiNash_messageDetail(nash_messageId, callback) {
    backendLookup("GET", `/nash-message/${nash_messageId}/`, callback)
}

export function apiNash_messageFeed(callback, nextUrl) {
    let endpoint =  "/nash-message/feed/"
    if (nextUrl !== null && nextUrl !== undefined) {
        endpoint = nextUrl.replace("http://localhost:8000/api", "")
    }
    backendLookup("GET", endpoint, callback)
}


export function apiNash_messageList(username, callback, nextUrl) {
    let endpoint =  "/nash-message/"
    if (username){
        endpoint =  `/nash-message/?username=${username}`
    }
    if (nextUrl !== null && nextUrl !== undefined) {
        endpoint = nextUrl.replace("http://localhost:8000/api", "")
    }
    backendLookup("GET", endpoint, callback)
}