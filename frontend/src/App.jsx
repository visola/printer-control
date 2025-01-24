import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import './App.css';

const LED_STATE_KEY = ['leds'];

function App() {
  const queryClient = useQueryClient();

  const { data: ledState } = useQuery({
    queryKey: LED_STATE_KEY,
    queryFn: () => fetch('/api/leds').then((res) => res.json()),
  });

  const { mutateAsync: toggleLed } = useMutation({
    mutationFn: () => fetch(
      '/api/leds',
      {
        body: JSON.stringify({ on: !ledState.on }),
        method: 'PUT',
        headers: { 'content-type': 'application/json' },
      },
    ).then((res) => res.json()),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: LED_STATE_KEY })
    }
  });

  return (
    <>
      <h1 className="title">Camera</h1>
      <img src="/api/camera" alt="webcam" width="1200px" />
      <h1 className="title">Led is {ledState && ledState.on ? 'On' : 'Off'}</h1>
      <button className="button" onClick={() => toggleLed()}>
        Toggle
      </button>
    </>
  )
}

export default App
