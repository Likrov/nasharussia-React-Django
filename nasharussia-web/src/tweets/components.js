import React, {useEffect, useState}  from 'react'

import {Nash_messageCreate} from './create'
import {Nash_message} from './detail'
import {apiNash_messageDetail} from './lookup'
import {FeedList} from './feed'
import {Nash-messageList} from './list'

export function FeedComponent(props) {
  const [newNash-message, setNewNash-message] = useState([])
  const canNash_message = props.canNash_message === "false" ? false : true
  const handleNewNash_message = (newNash_message) =>{
    let tempNewNash-message = [...newNash-message]
    tempNewNash-message.unshift(newNash_message)
    setNewNash-message(tempNewNash-message)
  }
  return <div className={props.className}>
          {canNash_message === true && <Nash_messageCreate didNash_message={handleNewNash_message} className='col-12 mb-3' />}
        <FeedList newNash-message={newNash-message} {...props} />
  </div>
}

export function Nash-messageComponent(props) {
    const [newNash-message, setNewNash-message] = useState([])
    const canNash_message = props.canNash_message === "false" ? false : true
    const handleNewNash_message = (newNash_message) =>{
      let tempNewNash-message = [...newNash-message]
      tempNewNash-message.unshift(newNash_message)
      setNewNash-message(tempNewNash-message)
    }
    return <div className={props.className}>
            {canNash_message === true && <Nash_messageCreate didNash_message={handleNewNash_message} className='col-12 mb-3' />}
          <Nash-messageList newNash-message={newNash-message} {...props} />
    </div>
}


export function Nash_messageDetailComponent(props){
  const {nash_messageId} = props
  const [didLookup, setDidLookup] = useState(false)
  const [nash_message, setNash_message] = useState(null)

  const handleBackendLookup = (response, status) => {
    if (status === 200) {
      setNash_message(response)
    } else {
      alert("There was an error finding your nash_message.")
    }
  }
  useEffect(()=>{
    if (didLookup === false){

      apiNash_messageDetail(nash_messageId, handleBackendLookup)
      setDidLookup(true)
    }
  }, [nash_messageId, didLookup, setDidLookup])

  return nash_message === null ? null : <Nash_message nash_message={nash_message} className={props.className} />
 }