import React from 'react'
import Plot from 'react-plotly.js';
import { useContext } from 'react';
import { DataContext } from '../DataContext';
import { useViewport } from '../ViewPortContext';

export const SimShow = () => {
  const {width,height} = useViewport()
  const {data} = useContext(DataContext)
    return (
        <div >
            <Plot 
        data={data}
        layout={ {title: 'Simulation results'} }
        config={{scrollZoom: true}}
        useResizeHandler={true}
        style={ {width: `${width  }px`, height: `${height/2}px`}}
      />
        </div>
    )
}
