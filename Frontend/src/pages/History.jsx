import OpEvent from "../components/OpEvent.jsx";
import React, {useEffect, useState} from "react";
import ExecuteRequest from "../AxiosManager.jsx";
import axios from "axios";


const History = () => {
    const [dates, setDates] = useState(null)
    const [historyPerDate, setHistoryPerDate] = useState(null)

    useEffect(
        ()=>{
            ExecuteRequest(axios.get('events/dates'), UpdateDates);
        }, []
    )

    function UpdateDates(datesArray) {
       const datesMap = datesArray.map(item =>
            <option key={self.crypto.randomUUID()} value={item}>{item}</option>);

        setDates(datesMap)
        dateChanged(datesArray[0])
    }

    function UpdateHistory(eventsArray)
    {
        const eventsMap = eventsArray.map(item =>
            (<OpEvent key={item._id} title={item.title} content={item.content} photoId={item.photoId}></OpEvent>));
        setHistoryPerDate(eventsMap);
    }

    function dateChanged(newDate)
    {
        if (!(typeof newDate === 'string' || newDate instanceof String))
        {
            newDate = newDate.target.value;
        }

        ExecuteRequest(axios.get(`events/?date=${newDate}`), UpdateHistory);
    }

    return <div>
        <br/>
        <select name="dateSelector" id="dateSelector" onChange={dateChanged}>
            {dates}
        </select>
        <ul>{historyPerDate}</ul>
    </div>
};

export default History;