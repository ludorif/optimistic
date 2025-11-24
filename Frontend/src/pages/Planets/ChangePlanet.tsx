/*
 * Copyright (c) 2025 Ludovic Riffiod
 */

import Button from "@mui/material/Button";
import React, {useEffect, useState} from "react";
import ExecuteRequest from "../../AxiosManager";
import axios from "axios";
import {TypedPlanet} from "../../components/Planet";

interface ChangePlanetProps {
    OnClickFunction: () => void;
}

const ChangePlanet: React.FC<ChangePlanetProps> = ({OnClickFunction}) => {
    const [PlanetName, SetPlanetName] = useState("");
    const [PlanetType, SetPlanetType] = useState("");

    useEffect(()=> {
            const planetName = localStorage.getItem("planetName");
            if (planetName != null) {
                SetPlanetName(planetName);
                SetPlanetType(localStorage.getItem("planetType") as string);
            }
        }, []
    )

    return <>
        <p>Current Planet : {PlanetName}</p>
        <TypedPlanet planetType={PlanetType}></TypedPlanet>
        <Button onClick={OnClickFunction} variant="contained">ChangePlanet</Button>
        </>
}

export default ChangePlanet;
