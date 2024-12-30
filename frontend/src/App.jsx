import { useQuery } from '@tanstack/react-query';
import './App.css';

function App() {
  const { data, isPending } = useQuery({
    queryKey: ['items'],
    queryFn: () => fetch('/api/items').then((res) => res.json()),
  });

  if (isPending) {
    return <p>isPending...</p>;
  }

  console.log(isPending, data);

  return (
    <>
      <p>This is a Banana.</p>
      <ul>
        {
          data.map((item) => (<li key={item.id}>{ item.name }</li>))
        }
      </ul>
    </>
  )
}

export default App
