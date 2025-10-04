//Copyright (c) 2025 Ludovic Riffiod
import { Outlet, Link } from "react-router-dom";
import Grid from "@mui/material/Grid";
import React from "react";

const Layout = () => {
    return (
        <>
        <Grid container spacing={4} justifyContent="center" alignItems="center">
            <Grid size={2}>
                        <Link to="/">Home</Link>
                    </Grid>
            <Grid size={2}>
                        <Link to="/history">History</Link>
            </Grid>
            <Grid size={2}>
                        <Link to="/vote">To vote</Link>
            </Grid>
            <Grid size={2}>
                        <Link to="/winners">Winners</Link>
            </Grid>
            <Grid size={2}>
                <Link to="/planet">Planet</Link>
            </Grid>
        </Grid>
            <Outlet />
        </>
    )
};

export default Layout;
