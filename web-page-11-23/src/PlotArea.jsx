import React, { useContext } from "react";
import Plot from 'react-plotly.js';
import { DataContext } from './Datacontext';

export default function PlotArea() {
    const { data, dataSetter } = useContext(DataContext)
    let keys = Object.keys(data)
    return (
        <Plot
            data={data
            }
            layout={{ width: window.innerWidth, height: window.innerHeight / 1.3, title: 'A Fancy Plot' }}
        /> 
    );
}