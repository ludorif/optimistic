import HistoryPart from "../components/HistoryPart.jsx";
import React, {useState} from "react";
import axios from "axios";



const History = () => {
    const [renderAnimals, setState] = useState(null)


    const handleHistory = () => {

        axios.get(' http://127.0.0.1:5000/history')
            .then(response => {
                const obj = JSON.parse(response.data);
                console.log(obj[0].photoId);

                const lines =[]
                obj.forEach(
                    item => {
                        lines.push(item)
                    }
                )

                const renderAnimals = lines.map(item => (
                    <HistoryPart key={item._id} title={item.title} content={item.content} photoId={item.photoId}></HistoryPart>));
                setState(renderAnimals)



            })
            .catch(error => {
                console.error('There was an error!', error);
            });

    }




    return <div>
        <ul>{renderAnimals}</ul>;
        <button onClick={handleHistory}>History</button>
        <br/>
        <select name="cars" id="cars">
            <option value="2025-08-11">2025-08-11</option>
            <option value="2025-08-10">2025-08-10</option>
        </select>
    </div>;
};

export default History;