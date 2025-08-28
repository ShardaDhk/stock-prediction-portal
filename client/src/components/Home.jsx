import React from 'react'
import Button from './Button'

const Home = () => {
  return (
    <>
        <div className='container'>
            <div className='p-5 text-center bg-light-dark rounded'>
                <h2 className='text-light'>Stock Prediction Portal</h2>
                <p className='text-light lead'> Stock Prediction Portal
This portal uses cutting-edge artificial intelligence to forecast stock trends, providing investors with valuable insights to make informed decisions. By analyzing vast datasets, our platform helps identify potential market movements, though it's important to remember that all predictions are based on historical data and not guarantees of future performance. </p>
                <Button btnName='Login' class='btn-outline-info'/>
            </div>

        </div>
    </>
  )
}

export default Home