import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import './App.css';

function App() {
  const [isLedOn, setIsLedOn] = useState(false);

  const { mutateAsync: toggleLed } = useMutation({
    mutationFn: () => fetch(
      '/api/leds',
      {
        body: JSON.stringify({ on: !isLedOn }),
        method: 'PUT',
        headers: { 'content-type': 'application/json' },
      },
    ).then((res) => res.json()),
  });

  const onClick = async () => {
    const resp = await toggleLed();
    setIsLedOn(resp.on);
  };

  return (
    <>
      <h1 className="title">Camera</h1>
      <img src="/api/camera" alt="webcam" />
      <h1 className="title">Led is {isLedOn ? 'On' : 'Off'}</h1>
      <button className="button" onClick={onClick}>
        Toggle
      </button>
    </>
  )
}

export default App
