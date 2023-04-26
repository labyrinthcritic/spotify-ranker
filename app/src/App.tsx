import { useState } from 'react'

import Chart from './comp/Chart'
import SearchOptions, { audioFeatures } from './comp/SearchOptions'
import Slider from './comp/Slider'

import './App.css'

const API = 'https://spotify-ranker-production.up.railway.app'

type Results = {
  time_to_sort: number,
  tracks: Track[],
}

type Track = {
  name: string,
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
  const [results, setResults] = useState<Results | null>(null)
  const [sortBy, setSortBy] = useState<string>('acousticness')
  const [selected, setSelected] = useState<number | null>(null)

  const onGo = async (artist: string, feature: string, algorithm: string) => {
    console.log('making api request...')

    let response = await fetch(API + '/all_tracks_by/' + artist + '/' + feature + '/' + algorithm)

    let results: Results = await response.json()
    
    setResults(results)
    setSortBy(feature)
  }
  
  return (
    <div className="w-screen h-screen bg-spotify-dark-gray">
      <div className="flex flex-row items-center w-full h-16 bg-spotify-green drop-shadow-md">
        <p className="m-6 text-2xl text-white font-bold font-sans">Spotify Ranker</p>
      </div>
      
      {/* main area */}
      <div className="my-4">
        <SearchOptions onGo={onGo}/>
        { results !== null ? (
          <div>
            <div className="flex flex-col items-center my-4 space-y-4">
              <p className="text-md text-white font-sans"><span className="font-bold">Results:</span> Sorted {results.tracks.length} tracks in {Math.round(results.time_to_sort * 10000) / 10000} seconds.</p>
              <Chart items={results.tracks.map(track => (track.features as any)[sortBy])}/>
              <Slider count={results.tracks.length} onUpdate={setSelected}/>
            </div>

            { selected !== null ? (
              <div className="mx-8">
                <p className="text-xl text-white font-bold font-sans">{results.tracks[selected].name}</p>
                <div className="">
                  <table className="border-separate ml-4 text-xl text-white font-sans">
                  { audioFeatures.map(([id, name]) => (
                    <tr className="space-x-16">
                      <td className="text-right">{name}</td>
                      <td>{(results.tracks[selected].features as any)[id]}</td>
                    </tr>
                  )) }
                  </table>
                </div>
              </div>
            ) : <></> }
          </div>
        ) : <></> }
      </div>
      
    </div>
  )
}
