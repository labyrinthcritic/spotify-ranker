type Props = {
  items: number[],
}

export default function Chart(props: Props) {
  const items = props.items

  const itemsMax: number = Math.max(...items)
  const itemsMin: number = Math.min(...items)
  const maxHeight: number = 400
  
  return (
    <div className="flex flex-row items-end w-full px-8">
      {items.map(item => (
        <div
          className="flex-1 w-5 rounded-t-md bg-spotify-green"
          style={{ height: Math.max(0.005, (item - itemsMin) / (itemsMax - itemsMin)) * maxHeight }}
        ></div>
      ))}
    </div>
  )
}
