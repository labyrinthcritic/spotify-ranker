import { useState } from 'react'

import Chart from './comp/Chart'
import SearchOptions from './comp/SearchOptions'
import Slider from './comp/Slider'

import './App.css'

type Track = {
  features: Features,
}

type Features = {
  acousticness: number,
  danceability: number,
  duration_ms: number,
  energy: number,
  instrumentalness: number,
  liveness: number,
  loudness: number,
  speechiness: number,
  tempo: number,
  valence: number,
}

export default function App() {
  const [tracks, setTracks] = useState<Array<Track> | null>(null)
  
  return (
    <div className="w-screen h-screen bg-spotify-dark-gray">
      <div className="flex flex-row items-center w-full h-16 bg-spotify-green drop-shadow-md">
        <p className="m-6 text-2xl text-white font-bold font-sans">Spotify Ranker</p>
      </div>
      {/* main area */}
      <div className="my-4">
        <SearchOptions organizeSettings={{}}/>
        { tracks !== null ? (
          <div className="flex flex-col items-center my-4 space-y-4">
            <Chart items={Array.from({length: 500}, () => Math.random() * 8)}/>
            <Slider count={500}/>
          </div>
        ) : <div></div> }
      </div>
    </div>
  )
}
