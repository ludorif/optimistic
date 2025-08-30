//Copyright (c) 2025 Ludovic Riffiod

import OpEvent from "../components/OpEvent.jsx";
import React, {useEffect, useState} from "react";
import ExecuteRequest from "../AxiosManager.jsx";
import axios from "axios";
import Grid from "@mui/material/Grid";


const History = () => {
    const [dates, setDates] = useState(null)
    const [historyPerDate, setHistoryPerDate] = useState(null)
    const [selectedDate, setSelectedDate] = useState("");



    useEffect(() => {
        ExecuteRequest(axios.get('events/dates'), UpdateDates);

        const savedDate = localStorage.getItem('selectedDate');
        if (savedDate) {
            setSelectedDate(savedDate);
        }

    }, []);


    function UpdateDates(datesArray) {
       const datesMap = datesArray.map((item, index) => <option key={index} value={item}>{item}</option>);

        setDates(datesMap)
        const savedDate = localStorage.getItem('selectedDate') || datesArray[0];
        setSelectedDate(savedDate);
        OnDateChanged(savedDate);
    }

    function UpdateHistory(eventsArray) {
        const eventsMap = eventsArray.map(item =>
            (
                <Grid size={4}>
                    <OpEvent key={item._id} event={item}></OpEvent>
                </Grid>
            ));
        setHistoryPerDate(eventsMap);
    }

    function OnDateChanged(newDate)
    {
        localStorage.setItem('selectedDate', newDate);
        setSelectedDate(newDate);


        ExecuteRequest(axios.get(`events/?date=${newDate}`), UpdateHistory);
    }

    return <div>
        <br/>
        <select name="dateSelector" id="dateSelector"
                value={selectedDate}
                onChange={(e) => OnDateChanged(e.target.value)} >
            {dates}
        </select>
        <Grid container spacing={4} justifyContent="center" alignItems="center">{historyPerDate}</Grid>
    </div>
};

export default History;