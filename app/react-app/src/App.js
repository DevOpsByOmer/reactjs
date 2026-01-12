import { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch(`${window._env_.REACT_APP_API_URL}/message`)
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div style={{ textAlign: 'center', marginTop: '2rem' }}>
      <h1>🌐 Enterprise Full Stack App</h1>
      <p>Backend says: {message}</p>
    </div>
  );
}

export default App;
