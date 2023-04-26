import { useState } from "react"

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons"

type Props = {
  onGo: (artistName: string, feature: string, algorithm: string) => void,
}

export const audioFeatures: Array<[string, string]> = [
  ['acousticness', 'Acousticness'],
  ['danceability', 'Danceability'],
  ['duration_ms', 'Duration'],
  ['energy', 'Energy'],
  ['instrumentalness', 'Instrumentalness'],
  ['liveness', 'Liveness'],
  ['loudness', 'Loudness'],
  ['speechiness', 'Speechiness'],
  ['tempo', 'Tempo'],
  ['valence', 'Valence'],
]

const sortingAlgorithms = [
  ['imperative_merge', 'Merge sort'],
  ['functional_merge', 'Merge sort (functional)'],
  ['shell', 'Shell sort'],
]

export default function OrganizeBy(props: Props) {
  const [artistInput, setArtistInput] = useState<string>('')
  const [selectedFeature, setSelectedFeature] = useState<string>(audioFeatures[0][0])
  const [selectedAlgorithm, setSelectedAlgorithm] = useState<string>(sortingAlgorithms[0][0])

  const onGo = () => {
    props.onGo(artistInput, selectedFeature, selectedAlgorithm)
  }

  return (
    <div className="flex flex-col items-center space-y-2">
      <div className="flex flex-row items-center space-x-2">
        <FontAwesomeIcon icon={faMagnifyingGlass} className="h-6 text-spotify-green"/>
        <input
          type="text"
          value={artistInput}
          onChange={ e => setArtistInput(e.target.value) }
          placeholder="Enter artist name..."
          className="p-2 bg-spotify-gray rounded-lg text-white"
        />
      </div>
      <div className="flex flex-row items-center space-x-2">
        <p className="font-sans text-lg text-white">Organize by</p>
        <select
          value={selectedFeature}
          onChange={ e => setSelectedFeature(e.target.value) }
          className="p-2 bg-spotify-gray rounded-lg text-white"
        >
          {audioFeatures.map(i => (
            <option value={i[0]}>{i[1]}</option>
          ))}
        </select>

        <p className="font-sans text-lg text-white">Sort with</p>
        <select
          value={selectedAlgorithm}
          onChange={ e => setSelectedAlgorithm(e.target.value) }
          className="p-2 bg-spotify-gray rounded-lg text-white"
        >
          {sortingAlgorithms.map(i => (
            <option value={i[0]}>{i[1]}</option>
          ))}
        </select>

        <button
          onClick={onGo}
          className="p-2 w-11 rounded-lg bg-spotify-green text-white font-bold"
        >Go</button>
      </div>
    </div>
  )
}
