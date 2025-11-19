/*
 * Copyright (c) 2025 Ludovic Riffiod
 */


import Planet, {ClickablePlanet, ToggablePlanet} from "../components/Planet.jsx";
import Grid from "@mui/material/Grid";
import mars_surface from "../assets/mars_surface.png";
import lunar_surface from '../assets/lunar_surface.jpg';
import earth_surface from '../assets/earth_surface.jpg';
import titleStyle from "../Helper.jsx";
import React, {useEffect, useRef} from "react";
import {TextField, ToggleButton, ToggleButtonGroup} from "@mui/material";
import Button from "@mui/material/Button";
import ExecuteRequest from "../AxiosManager.jsx";
import axios from "axios";

const PlanetPage = () => {

    enum UserState {
        None,
        PlanetSelected,
        NewPlanet
    }

    const [State, setState] = React.useState(UserState.None);
    const [Planets, setPlanets] = React.useState([]);

    function SwitchToNewPlanet() {
        setState(UserState.NewPlanet)
    }

    function SwitchToChangePlanet(){
        setState(UserState.None)
        localStorage.removeItem("planetName")
    }


    const ChoosePlanet = () => {
        return <>

            <h1 style={titleStyle}>Check planet story</h1>
            <Button onClick={SwitchToNewPlanet} variant="contained">New Planet</Button>
            <Grid container justifyContent="center" alignItems="center" spacing={1}
                  sx={{justifyContent: "space-between"}}>
                {Planets}
            </Grid>

        </>
    }

    const ChangePlanet = () => {
        return <Button onClick={SwitchToChangePlanet} variant="contained">ChangePlanet</Button>
    }

    const CreateNewPlanet = () => {
        const [planetType, setPlanetType] = React.useState('moon');
        const planetNameRef = useRef<HTMLInputElement>(null);
        const planetStoryRef = useRef<HTMLInputElement>(null);


        const handlePlanetType = (event, newPlanetType) => {
            setPlanetType(newPlanetType);
        };

        function CheckValues() {

            ExecuteRequest(axios.post('planets/', {name: planetNameRef.current.value, type: planetType}));

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
                <ToggablePlanet value="mars" surfaceImage={mars_surface}></ToggablePlanet>
                <ToggablePlanet value="moon" surfaceImage={lunar_surface}></ToggablePlanet>
                <ToggablePlanet value="earth" surfaceImage={earth_surface}></ToggablePlanet>

            </ToggleButtonGroup>

            <TextField inputRef={planetStoryRef} label="Starting story" variant="outlined"/>
            <Button onClick={CheckValues} variant="contained">Confirm creation</Button>
        </>
    }

    function UpdatePlanets(planetsArray) {
        const planetsMap = planetsArray.map((item, index) =>
            <ClickablePlanet planetName={item.planet_name} type={item.planet_type}></ClickablePlanet>);

        setPlanets(planetsMap);
    }

    useEffect(()=> {
            ExecuteRequest(axios.get('planets/'), UpdatePlanets);
            const planetName = localStorage.getItem("planetName");
            if (planetName != null) {
                setState(UserState.PlanetSelected)
            }
        }, []
    )



    switch (State) {
        case UserState.None:
            return <ChoosePlanet/>
        case UserState.PlanetSelected:
            return <ChangePlanet/>
        case UserState.NewPlanet:
            return <CreateNewPlanet/>
    }
}

export default PlanetPage;
