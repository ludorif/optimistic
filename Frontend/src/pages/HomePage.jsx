import React from 'react'
import '../App.css'
import Grid from '@mui/material/Grid';
import styled from "styled-components";
import {Paper} from "@mui/material";

const HomePage = () =>{
    const Item = styled(Paper)(({ theme }) => ({
        backgroundColor: '#fff',
        textAlign: 'center'
    }));

    return (
        <div>
            <p> List of worlds swipe</p>
            <Grid container spacing={2}>
                <Grid size={8}>
                    <Item>size=8</Item>
                </Grid>
                <Grid size={4}>
                    <Item>size=4</Item>
                </Grid>
                <Grid size={4}>
                    <Item>size=4</Item>
                </Grid>
                <Grid size={8}>
                    <Item>size=8</Item>
                </Grid>
            </Grid>
        </div>);
}


export default HomePage
