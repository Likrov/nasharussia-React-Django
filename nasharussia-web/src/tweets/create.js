import React from 'react'
import {apiNash_messageCreate} from './lookup'


export function Nash_messageCreate(props){
  const textAreaRef = React.createRef()
  const {didNash_message} = props
    const handleBackendUpdate = (response, status) =>{
      if (status === 201){
        didNash_message(response)
      } else {
        console.log(response)
        alert("An error occured please try again")
      }
    }

    const handleSubmit = (event) => {
      event.preventDefault()
      const newVal = textAreaRef.current.value
      // backend api request
      apiNash_messageCreate(newVal, handleBackendUpdate)
      textAreaRef.current.value = ''
    }
    return <div className={props.className}>
          <form onSubmit={handleSubmit}>
            <textarea ref={textAreaRef} required={true} className='form-control' name='nash_message'>

            </textarea>
            <button type='submit' className='btn btn-primary my-3'>Nash_message</button>
        </form>
  </div>
}