/*
 * Copyright (c) 2025 Ludovic Riffiod
 */

import {useEffect, useState} from "react";
import ExecuteRequest, {GetTodayDateStr} from "../AxiosManager.jsx";
import axios from "axios";

const SummaryPage = () => {
    const [summaryContent, SetSummaryContent] = useState("");


    useEffect(() => {
        ExecuteRequest(axios.get(`summary/`), SetSummaryContent)
    }, []);

    const aws_url = import.meta.env.VITE_AWS_URL;
    return <div>
        <p>{summaryContent}</p>
        <img src={`${aws_url}/output-1.png`}/>
        <img src={`${aws_url}/output-2.png`}/>
        <img src={`${aws_url}/output-3.png`}/>
        <img src={`${aws_url}/output-4.png`}/>
    </div>

}

export default SummaryPage;
