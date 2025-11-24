/*
 * Copyright (c) 2025 Ludovic Riffiod
 */

import { Grid } from "@mui/material";
import Button from "@mui/material/Button";
import React, {JSX} from "react";
import titleStyle from "../../Helper";

interface ChoosePlanetProps {
    OnClickFunction: () => void;  // Type for your onClick function
    Planets: JSX.Element[];       // Type for the Planets array (array of JSX elements)
}

const ChoosePlanet : React.FC<ChoosePlanetProps> = ({ OnClickFunction, Planets }) => {
    return (<>
        <h1 style={titleStyle}>Check planet story</h1>
        <Button onClick={OnClickFunction} variant="contained">New Planet</Button>
        <Grid container justifyContent="center" alignItems="center" spacing={1}
              sx={{justifyContent: "space-between"}}>
            {Planets}
        </Grid>
    </>)
}

export default ChoosePlanet;
