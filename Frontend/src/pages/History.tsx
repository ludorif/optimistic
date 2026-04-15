//Copyright (c) 2025 Ludovic Riffiod

import OpEvent from "../components/OpEvent";
import React, {useEffect, useState} from "react";
import ExecuteRequest from "../AxiosManager";
import axios from "axios";
import Grid from "@mui/material/Grid";
import {useNavigate} from "react-router-dom";


const History = () => {
    const [dates, setDates] = useState<React.JSX.Element[]>([])
    const [historyPerDate, setHistoryPerDate] = useState<React.JSX.Element[]>([])
    const [selectedDate, setSelectedDate] = useState("");
    const navigate = useNavigate();


    useEffect(() => {
        const planetId = localStorage.getItem('planetId');
        if (!planetId || planetId === "undefined")
        {
            navigate('/Planet');
            return
        }

        ExecuteRequest(axios.get(`events/dates/?planet_id=${planetId}`), UpdateDates);

        const savedDate = localStorage.getItem('selectedDate');
        if (savedDate) {
            setSelectedDate(savedDate);
        }

    }, []);


    function UpdateDates(datesArray: ODate[]) {


       const datesMap = datesArray.map((item, index) => <option key={index} value={item.created_at}>{new Date(item.created_at).toDateString()}</option>);

        setDates(datesMap)
        const savedDate = localStorage.getItem('selectedDate') || datesArray[0].created_at;
        setSelectedDate(savedDate);
        OnDateChanged(savedDate);
    }

    function UpdateHistory(eventsArray: OEvent[]) {
        const eventsMap = eventsArray.map(item =>
            (
                <Grid size={4}>
                    <OpEvent key={item.id} event={item}></OpEvent>
                </Grid>
            ));
        setHistoryPerDate(eventsMap);
    }

    function OnDateChanged(newDate: string)
    {
        localStorage.setItem('selectedDate', newDate);
        setSelectedDate(newDate);
        ExecuteRequest(axios.get(`events/?planet_id=${localStorage.getItem('planetId')}&date=${newDate}`), UpdateHistory);
    }


    return <div>
        <br/>
        <h2>History</h2>
        <select name="dateSelector" id="dateSelector"
                value={selectedDate}
                onChange={(e) => OnDateChanged(e.target.value)} >
            {dates}
        </select>
        <Grid container spacing={4} justifyContent="center" alignItems="center">{historyPerDate}</Grid>
    </div>
};

export default History;
