import React from 'react'
import './App.css';

import VideoSteram from './components/VideoStream'
import Statistics from './components/Statistics'
import History from './components/History'

function App() {
  return (
    <div className="App">
      <div className='row' id='top-row'>
        <div className='sidebar'>
          <Statistics />
          <History />
        </div>
        <VideoSteram />
      </div>
      <div className='row' id='bottom-row'>

      </div>
    </div>
  );
}

export default App;
