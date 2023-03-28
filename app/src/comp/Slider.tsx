import { useState } from 'react'

import './Slider.css'

type Props = {
  count: number,
}

function Slider(props: Props) {
  const [value, setValue] = useState<number>(0);

  const barWidth = Math.floor(100 / props.count).toString() + '%'
  
  return (
    <div className="w-full px-8">
      <input
        type="range"
        value={value}
        onChange={ e => setValue(parseInt(e.target.value)) }
        min="0"
        max={props.count - 1}
        className="w-full bg-spotify-gray drop-shadow-md"
      />
      <style dangerouslySetInnerHTML={{ __html: [
        // html does not allow inline styling of pseudo-elements -- avoid modifying
        'input::-webkit-slider-thumb, input::-moz-range-thumb {',
        '    width: ' + barWidth + ';',
        '}'
        ].join('\n')
      }}/>
    </div>
  )
}

export default Slider