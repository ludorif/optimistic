/*
 * Copyright (c) 2025 Ludovic Riffiod
 */

import React, {useRef} from "react";
import ExecuteRequest from "../../AxiosManager";
import axios from "axios";
import titleStyle from "../../Helper";
import {TextField, ToggleButtonGroup} from "@mui/material";
import {ToggablePlanet} from "../../components/Planet";
import mars_surface from "../../assets/mars_surface.png";
import lunar_surface from "../../assets/lunar_surface.jpg";
import earth_surface from "../../assets/earth_surface.jpg";
import Button from "@mui/material/Button";

const CreateNewPlanet = () => {
    const [planetType, setPlanetType] = React.useState('moon');
    const planetNameRef = useRef<HTMLInputElement>(null);
    const planetStoryRef = useRef<HTMLInputElement>(null);


    const handlePlanetType = (event, newPlanetType) => {
        setPlanetType(newPlanetType);
    };

    function OnPlanetCreated(response){
        console.log(response);
        localStorage.setItem("planetId", response.planet_id);
    }

    function CheckValues() {

        ExecuteRequest(axios.post('planets/', {name: planetNameRef.current!.value, type: planetType, first_story: planetStoryRef.current!.value }), OnPlanetCreated);

    }


    return <>

        <h1 style={titleStyle}>Create your planet</h1>
        <TextField inputRef={planetNameRef} label="Planet name" variant="outlined"/>
        <p> Choose your planet style:</p>

        <ToggleButtonGroup
            value={planetType}
            exclusive
            onChange={handlePlanetType}
            aria-label="text alignment"
        >
            <ToggablePlanet value="mars" planetType="mars"></ToggablePlanet>
            <ToggablePlanet value="moon" planetType="moon"></ToggablePlanet>
            <ToggablePlanet value="earth" planetType="earth"></ToggablePlanet>

        </ToggleButtonGroup>

        <TextField inputRef={planetStoryRef} label="Starting story" variant="outlined"/>
        <Button onClick={CheckValues} variant="contained">Confirm creation</Button>
    </>
}

export default CreateNewPlanet;
