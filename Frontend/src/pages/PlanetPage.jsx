/*
 * Copyright (c) 2025 Ludovic Riffiod
 */


import Planet, {ClickablePlanet, ToggablePlanet} from "../components/Planet.jsx";
import Grid from "@mui/material/Grid";
import mars_surface from '../assets/mars_surface.png';
import lunar_surface from '../assets/lunar_surface.jpg';
import earth_surface from '../assets/earth_surface.jpg';
import titleStyle from "../Helper.jsx";
import React, {useRef} from "react";
import {TextField, ToggleButton, ToggleButtonGroup} from "@mui/material";
import Button from "@mui/material/Button";

const PlanetPage = () => {
    

    const ChoosePlanet = () => {
        return <>

            <h1 style={titleStyle}>Check planet story</h1>
            <Grid container justifyContent="center" alignItems="center" spacing={1}
                  sx={{justifyContent: "space-between"}}>
                <ClickablePlanet planetName={"test2"} surfaceImage={lunar_surface}></ClickablePlanet>
                <ClickablePlanet planetName={"test2"} surfaceImage={earth_surface}></ClickablePlanet>
                <ClickablePlanet planetName={"test2"} surfaceImage={mars_surface}></ClickablePlanet>
                <ClickablePlanet planetName={"test2"} surfaceImage={mars_surface}></ClickablePlanet>
                <ClickablePlanet planetName={"test2"} surfaceImage={lunar_surface}></ClickablePlanet>
                <ClickablePlanet planetName={"test2"} surfaceImage={earth_surface}></ClickablePlanet>
            </Grid>
        </>
    }

    const ChangePlanet = () => {
        return <Button onClick={ChangePlanet} variant="contained">Confirm creation</Button>
    }

    const CreateNewPlanet = () => {
        const [alignment, setAlignment] = React.useState('moon');
        const planetNameRef = useRef('')
        const planetStoryRef = useRef('')

        const handleAlignment = (event, newAlignment) => {
            setAlignment(newAlignment);
        };

        function CheckValues() {
            console.log(planetNameRef.current.value + "  " + alignment + "  " + planetStoryRef.current.value);

            const planetName = localStorage.getItem("planetName");
            if (planetName != null) {
                console.log(planetName)
            }

        }


        return <>

            <h1 style={titleStyle}>Create your planet</h1>
            <TextField inputRef={planetNameRef} label="Planet name" variant="outlined"/>
            <p> Choose your planet style:</p>

            <ToggleButtonGroup
                value={alignment}
                exclusive
                onChange={handleAlignment}
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


    return <>
        <CreateNewPlanet/>
    </>
}

export default PlanetPage;
