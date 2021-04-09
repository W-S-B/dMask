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
      <img src='http://192.168.0.148:5000/video_feed'></img>
    </div>
  );
}

export default VideoStream;