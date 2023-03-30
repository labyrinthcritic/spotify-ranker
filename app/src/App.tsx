import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons'

import Chart from './comp/Chart'
import OrganizeBy from './comp/OrganizeBy'
import Slider from './comp/Slider'

import './App.css'

export default function App() {
  const [artistInput, setArtistInput] = useState<string>()

  const onArtistFind = () => {
    console.log('Find Artist')
  }
  
  return (
    <div className="w-screen h-screen bg-spotify-dark-gray">
      <div className="flex flex-row items-center w-full h-16 bg-spotify-green drop-shadow-md">
        <p className="m-6 text-2xl text-white font-bold font-sans">Spotify Ranker</p>
      </div>
      {/* main area */}
      <div className="flex flex-col items-center my-4 space-y-4">
        <div className="flex flex-row items-center space-x-2">
          <FontAwesomeIcon icon={faMagnifyingGlass} className="h-6 text-spotify-green"/>
          <input
            type="text"
            value={artistInput}
            onChange={ e => setArtistInput(e.target.value) }
            placeholder="Enter artist name..."
            className="p-2 bg-spotify-gray rounded-lg text-white"
          />
          <button
            onClick={onArtistFind}
            className="p-2 rounded-lg bg-spotify-green text-white font-bold"
          >
            Find
          </button>
        </div>

        <OrganizeBy organizeSettings={{}}/>
        <Chart items={Array.from({length: 75}, () => Math.random() * 8)}/>
        <Slider count={75}/>
      </div>
    </div>
  )
}
