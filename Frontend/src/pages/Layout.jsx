//Copyright (c) 2025 Ludovic Riffiod
import React, { useState } from "react";
import { Outlet, Link } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import MenuIcon from "@mui/icons-material/Menu";

const Layout = () => {
    const navLinks = [
        { path: "/", label: "Home" },
        { path: "/history", label: "History" },
        { path: "/vote", label: "To vote" },
        { path: "/winners", label: "Winners" },
        { path: "/planet", label: "Planet" },
        { path: "/summary", label: "Summary" },
    ];

    const [anchorEl, setAnchorEl] = useState(null);

    const handleMenuOpen = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
    };

    // Custom color palette
    const appBarColor = "#2c7a7b";
    const buttonColor = "#fff";    // white text

    return (
        <>
            <AppBar position="static" sx={{ backgroundColor: appBarColor }}>
                <Toolbar>
                    <Typography variant="h6" sx={{ flexGrow: 1 }}>
                        Optimistic
                    </Typography>

                    {/* Desktop Menu */}
                    <Box sx={{ display: { xs: "none", md: "flex" }, gap: 2 }}>
                        {navLinks.map((link, index) => (
                            <Button
                                key={index}
                                color="inherit"
                                component={Link}
                                to={link.path}
                                sx={{
                                    textTransform: "none",
                                    fontWeight: 500,
                                    color: buttonColor,
                                }}
                            >
                                {link.label}
                            </Button>
                        ))}
                    </Box>

                    {/* Mobile Menu */}
                    <Box sx={{ display: { xs: "flex", md: "none" } }}>
                        <IconButton
                            edge="start"
                            color="inherit"
                            aria-label="menu"
                            onClick={handleMenuOpen}
                        >
                            <MenuIcon />
                        </IconButton>
                        <Menu
                            anchorEl={anchorEl}
                            open={Boolean(anchorEl)}
                            onClose={handleMenuClose}
                            keepMounted
                        >
                            {navLinks.map((link, index) => (
                                <MenuItem
                                    key={index}
                                    component={Link}
                                    to={link.path}
                                    onClick={handleMenuClose}
                                >
                                    {link.label}
                                </MenuItem>
                            ))}
                        </Menu>
                    </Box>
                </Toolbar>
            </AppBar>

            <Box sx={{ p: 3 }}>
                <Outlet />
            </Box>
        </>
    );
};

export default Layout;
