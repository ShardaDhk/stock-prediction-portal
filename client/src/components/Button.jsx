import React from 'react'

const Button = (props) => {
  return (
    <>
        <a className={`btn ${props.class}`} href="">{props.btnName}</a>
    </>
  )
}

export default Button