import React, {useEffect, useState}  from 'react'

import {apiNash_messageFeed} from './lookup'

import {Nash_message} from './detail'

export function FeedList(props) {
    const [nash-messageInit, setNash-messageInit] = useState([])
    const [nash-message, setNash-message] = useState([])
    const [nextUrl, setNextUrl] = useState(null)
    const [nash-messageDidSet, setNash-messageDidSet] = useState(false)
    useEffect(()=>{
      const final = [...props.newNash-message].concat(nash-messageInit)
      if (final.length !== nash-message.length) {
        setNash-message(final)
      }
    }, [props.newNash-message, nash-message, nash-messageInit])

    useEffect(() => {
      if (nash-messageDidSet === false){
        const handleNash_messageListLookup = (response, status) => {
          if (status === 200){
            setNextUrl(response.next)
            setNash-messageInit(response.results)
            setNash-messageDidSet(true)
          }
        }
        apiNash_messageFeed(handleNash_messageListLookup)
      }
    }, [nash-messageInit, nash-messageDidSet, setNash-messageDidSet, props.username])


    const handleDidRenash = (newNash_message) => {
      const updateNash-messageInit = [...nash-messageInit]
      updateNash-messageInit.unshift(newNash_message)
      setNash-messageInit(updateNash-messageInit)
      const updateFinalNash-message = [...nash-message]
      updateFinalNash-message.unshift(nash-message)
      setNash-message(updateFinalNash-message)
    }
    const handleLoadNext = (event) => {
      event.preventDefault()
      if (nextUrl !== null) {
        const handleLoadNextResponse = (response, status) =>{
          if (status === 200){
            setNextUrl(response.next)
            const newNash-message = [...nash-message].concat(response.results)
            setNash-messageInit(newNash-message)
            setNash-message(newNash-message)
          }
        }
        apiNash_messageFeed(handleLoadNextResponse, nextUrl)
      }
    }

    return <React.Fragment>{nash-message.map((item, index)=>{
      return <Nash_message  
        nash_message={item} 
        didRenash={handleDidRenash}
        className='my-5 py-5 border bg-white text-dark' 
        key={`${index}-{item.id}`} />
    })}
    {nextUrl !== null && <button onClick={handleLoadNext} className='btn btn-outline-primary'>Load next</button>}
    </React.Fragment>
  }


