import React, {useState, useEffect} from 'react'

function History(){
    const [initialData, setInitialData] = useState([{}]);

    useEffect(()=> {
      fetch('/history').then(
        response => response.json()
      ).then(data => setInitialData(data))
    }, []);

    return (
        <div className='History'>
            <h1>History</h1>
            <p>{initialData.messages}</p>
        </div>
    );
}

export default History;