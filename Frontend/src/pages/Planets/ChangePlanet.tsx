/*
 * Copyright (c) 2025 Ludovic Riffiod
 */

import Button from "@mui/material/Button";
import React from "react";

interface ChangePlanetProps {
    OnClickFunction: () => void;
}

const ChangePlanet: React.FC<ChangePlanetProps> = ({OnClickFunction}) => {
    return <Button onClick={OnClickFunction} variant="contained">ChangePlanet</Button>
}

export default ChangePlanet;
