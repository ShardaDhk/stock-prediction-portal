import React, { use, useEffect, useState } from 'react'
import axiosInstance from '../../axiosInstance'
import { FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import { faSpinner } from '@fortawesome/free-solid-svg-icons'

const Dashboard = () => {
    const [ticker, setTicker] = useState('')
    const [error, setError] = useState()
    const [loading, setLoading] = useState(false)
    const [plot, setPlot] = useState()
    const [ma100, setMA100] = useState()
    const [ma200, setMA200] = useState()
    const [prediction, setPredection] = useState()
    const [mse, setMSE] = useState()
    const [rmse, setRMSE] = useState()
    const [r2, setR2] = useState()
 
    useEffect(() => {
        const fetchProtectedData = async () => {
            try {
              const response = await axiosInstance.get('/protected-view/')
              // console.log('Success', response.data);
            }catch(error){
              console.error('Error fetching data:', error)
            }
        }
        fetchProtectedData();
    }, [])

    const handelSubmit = async (e) => {
      e.preventDefault()
      setLoading(true)
      try {
        const response = await axiosInstance.post('/predict/', {
          ticker: ticker
        })
        // console.log(response.data)
        const banckendRoot = import.meta.env.VITE_BACKEND_ROOT
        const plotUrl = `${banckendRoot}${response.data.plot_img}`
        const ma100Url = `${banckendRoot}${response.data.plot_100_dma}`
        const ma200Url = `${banckendRoot}${response.data.plot_200_dma}`
        const predictionUrl = `${banckendRoot}${response.data.plot_prediction}`
        setMSE(response.data.mse)
        setRMSE(response.data.rmse)
        setR2(response.data.r2)
        
        //Set Plot
        console.log(plotUrl)
        setPlot(plotUrl)
        setMA100(ma100Url)
        setMA200(ma200Url)
        setPredection(predictionUrl)

        if(response.data.error){
            setError(response.data.error)
        }
          
      } catch (error) {
        console.error('There is an error making the API request:', error)
      } finally {
        setLoading(false)
      }
    }

  return (
    <div className='container'>
      <div className='row'>
        <div className='col-md-6 mx-auto'>
          <form onSubmit={handelSubmit}>
            <input type="text" className='form-control' placeholder='Enter Stock Ticker' 
              onChange={(e) => setTicker(e.target.value)} required
            />
            <small>{error && <div className='text-danger'>{error}</div>}</small>
            <button type='submit' className='btn btn-info mt-3'>
              {loading ? <span><FontAwesomeIcon icon={faSpinner} spin/> Please Wait...</span>: 'See Prediction'}
            </button>
          </form>
        </div>

        {/* Print PRediction plot */}
        {prediction && (
          <div className='prediction mt-3'>
            <div className='p-5'>
                {plot && (
                  <img src={plot} style={{ maxWidth: '100%' }}/>
                )}
            </div>

            <div className='p-5'>
                {ma100 && (
                  <img src={ma100} style={{ maxWidth: '100%' }}/>
                )}
            </div>

            <div className='p-5'>
                {ma200 && (
                  <img src={ma200} style={{ maxWidth: '100%' }}/>
                )}
            </div>

            <div className='p-5'>
                {prediction && (
                  <img src={prediction} style={{ maxWidth: '100%' }}/>
                )}
            </div>

            <div className="text-light p-3">
                <h4>Model Evalution</h4>
                <p>Mean Squared Error (MSE) : {mse}</p>
                <p>Root Mean Squared Error (RMSE) : {rmse}</p>
                <p>R-Squared : {r2}</p>
            </div>

          </div>
        )}
        
        
      </div>
    </div>
  )
}

export default Dashboard