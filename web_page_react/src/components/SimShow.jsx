import React from 'react'
import Plot from 'react-plotly.js';
import { useContext } from 'react';
import { DataContext } from '../DataContext';

export const SimShow = () => {
  const {data} = useContext(DataContext)
    return (
        <div >
            <Plot 
        data={data}
        layout={ {title: 'Simulation results'} }
        config={{scrollZoom: true}}
      />
        </div>
    )
}
