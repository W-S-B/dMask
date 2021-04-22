import React, {useState, useEffect} from 'react'
import './VideoStream.css';

function VideoStream() {
  const [initialData, setInitialData] = useState([{}]);

  useEffect(()=> {
    fetch('../api').then(
      response => response.json()
    ).then(data => setInitialData(data))
  }, []);

  return (
    <div className="video">
      <img src='/video_feed'></img>
    </div>
  );
}

export default VideoStream;