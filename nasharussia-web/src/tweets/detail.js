
import React, {useState}  from 'react'

import {ActionBtn} from './buttons'

import {
  UserDisplay,
  UserPicture
} from '../profiles'

export function ParentNash_message(props){
    const {nash_message} = props
    return nash_message.parent ? <Nash_message isRenash renasher={props.renasher} hideActions className={' '} nash_message={nash_message.parent} /> : null
  }
  export function Nash_message(props) {
      const {nash_message, didRenash, hideActions, isRenash, renasher} = props
      const [actionNash_message, setActionNash_message] = useState(props.nash_message ? props.nash_message : null)
      let className = props.className ? props.className : 'col-10 mx-auto col-md-6'
      className = isRenash === true ? `${className} p-2 border rounded` : className
      const path = window.location.pathname
      const match = path.match(/(?<nash_messageid>\d+)/)
      const urlNash_messageId = match ? match.groups.nash_messageid : -1
      const isDetail = `${nash_message.id}` === `${urlNash_messageId}`
      
      const handleLink = (event) => {
        event.preventDefault()
        window.location.href = `/${nash_message.id}`
      }
      const handlePerformAction = (newActionNash_message, status) => {
        if (status === 200){
          setActionNash_message(newActionNash_message)
        } else if (status === 201) {
          if (didRenash){
            didRenash(newActionNash_message)
          }
        }
        
      }
      
      return <div className={className}>
         {isRenash === true && <div className='mb-2'>
          <span className='small text-muted'>Renash via <UserDisplay user={renasher} /></span>
        </div>}
        <div className='d-flex'>
       
          <div className=''>
            <UserPicture user={nash_message.user} />
          </div>
          <div className='col-11'>
              <div>
             
                <p>
                  <UserDisplay includeFullName user={nash_message.user} />
                </p>
                <p>{nash_message.content}</p>
               
                <ParentNash_message nash_message={nash_message} renasher={nash_message.user} />
              </div>
          <div className='btn btn-group px-0'>
          {(actionNash_message && hideActions !== true) && <React.Fragment>
                  <ActionBtn nash_message={actionNash_message} didPerformAction={handlePerformAction} action={{type: "like", display:"Likes"}}/>
                  <ActionBtn nash_message={actionNash_message} didPerformAction={handlePerformAction} action={{type: "unlike", display:"Unlike"}}/>
                  <ActionBtn nash_message={actionNash_message} didPerformAction={handlePerformAction} action={{type: "renash", display:"Renash"}}/>
                </React.Fragment>
          }
                  {isDetail === true ? null : <button className='btn btn-outline-primary btn-sm' onClick={handleLink}>View</button>}
                </div>
                </div>
      </div>
      </div>
    }
  