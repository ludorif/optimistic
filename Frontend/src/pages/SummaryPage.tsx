/*
 * Copyright (c) 2025 Ludovic Riffiod
 */

import React, {useEffect, useState} from "react";
import ExecuteRequest, {GetTodayDateStr} from "../AxiosManager.jsx";
import axios from "axios";
import titleStyle from "../Helper.jsx";

const SummaryPage = () => {
    const [summaryContent, SetSummaryContent] = useState("");


    useEffect(() => {
        ExecuteRequest(axios.get(`summary/`), SetSummaryContent)
    }, []);

    const aws_url = import.meta.env.VITE_AWS_URL;
    return <div>
        <h1 style={titleStyle}>What happened to this planet:</h1>
        <p>{summaryContent}</p>
        <img src={`${aws_url}/output-1.png`}/>
        <img src={`${aws_url}/output-2.png`}/>
        <img src={`${aws_url}/output-3.png`}/>
        <img src={`${aws_url}/output-4.png`}/>
    </div>

}

export default SummaryPage;
