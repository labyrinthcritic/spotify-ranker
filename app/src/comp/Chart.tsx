type Props = {
  items: Array<number>
}

export default function Chart(props: Props) {
  const items = props.items;

  const itemsMax = Math.max(...items);
  const maxHeight = 400;
  
  return (
    <div className="flex flex-row items-end w-full px-8">
      {items.map(item => (
        <div className="flex-1 w-5 bg-spotify-green" style={{ height: (item / itemsMax) * maxHeight }}>
        </div>
      ))}
    </div>
  )
}
