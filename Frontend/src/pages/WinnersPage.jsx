import React, {useEffect, useRef, useState} from "react";
import axios from "axios";
import OpWinnerEvent from "../components/OpWinnerEvent.jsx";
import styles from "../css/mystyle.module.css";
import ExecuteRequest from "../AxiosManager.jsx";
import Grid from "@mui/material/Grid";
//Copyright (c) 2025 Ludovic Riffiod
import ArcherContainer from '../LocalPackage/react-archer-feature-react-19-migration/src/ArcherContainer/ArcherContainer';
import titleStyle from "../Helper.jsx";




function WinnersPage () {
    const [allEvents, setAllEvents] = useState([])
    const [winners, setWinners] = useState([])
    const itemsRef = useRef(null);
    let count = 0;

    function UpdateWinners(winnersArray) {
        setWinners(winnersArray);
    }

    function GenerateNewOpEvent(event) {
        const isWinner = winners.find((item) => item._id === event._id) != null;


        if (isWinner) {
            ++count;
        }

        return <Grid  size={4}   >
        <OpWinnerEvent  key={event._id} event={event}  count={count} isWinner={isWinner}></OpWinnerEvent>
        </Grid>;

    }

    function GenerateNewLine(lineContent, lineIndex) {
    return <Grid height={750} container justifyContent="center" alignItems="center" spacing={1} ref={itemsRef} size={10} key={lineIndex} className={styles.customUl}>{lineContent}</Grid>
    }

    function UpdateAllEvents(eventsArray) {
        let localAllEvents = []
        let lineContent = [];
        let date = Date.parse(eventsArray[0].date);
        let lineIndex = 0;

        for (let event of eventsArray) {
            const parsedDate = Date.parse(event.date)
            if (parsedDate > date)
            {
                localAllEvents.push(GenerateNewLine(lineContent, lineIndex));
                date = parsedDate;
                lineContent = []
                ++ lineIndex;
            }

            lineContent.push(GenerateNewOpEvent(event));
        }

        localAllEvents.push(GenerateNewLine(lineContent, lineIndex));
        setAllEvents(localAllEvents)
    }

    useEffect(()=>{
        ExecuteRequest(axios.get("winners/"), UpdateWinners);
    },[])

    useEffect(() => {
        if(winners.length === 0){
            return;
        }
        ExecuteRequest(axios.get("events/"), UpdateAllEvents);
        }, [winners])


    return (
        <div >
            <h1 style={titleStyle}>Events that won:</h1>

            <ArcherContainer strokeColor="gray">
            {allEvents}
            </ArcherContainer>
        </div>

    );
}

export default WinnersPage;
