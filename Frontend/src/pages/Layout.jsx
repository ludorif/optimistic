//Copyright (c) 2025 Ludovic Riffiod
import { Outlet, Link } from "react-router-dom";

const Layout = () => {
    return (
        <>
            <nav>
                <ul>
                    <li>
                        <Link to="/">Home</Link>
                    </li>
                    <li>
                        <Link to="/history">History</Link>
                    </li>
                    <li>
                        <Link to="/vote">To vote</Link>
                    </li>
                    <li>
                        <Link to="/winners">Winners</Link>
                    </li>
                </ul>
            </nav>

            <Outlet />
        </>
    )
};

export default Layout;