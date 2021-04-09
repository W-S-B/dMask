import React, {useState, useEffect} from 'react'
import './Statistics.css';

function Statistics() {
  const [initialData, setInitialData] = useState([{}]);

  useEffect(()=> {
    fetch('../api').then(
      response => response.json()
    ).then(data => setInitialData(data))
  }, []);

  return (
    <div>
        <div className="statistics">
            <h1>Today's</h1>
            <h2>Statistics</h2>
            <p>All:</p>
            <p>With a mask:</p>
            <p>With iMask:</p>
            <p>W/o a mask:</p>
        </div>
    </div>
  );
}

export default Statistics;