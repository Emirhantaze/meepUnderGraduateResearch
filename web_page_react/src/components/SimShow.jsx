import React from 'react'
import Plot from 'react-plotly.js';
import { useContext } from 'react';
import { DataContext } from '../DataContext';
import { useViewport } from '../ViewPortContext';

export const SimShow = () => {
  const { width, height } = useViewport()
  const { data } = useContext(DataContext)
  return (
    <div >
      <Plot
        data={data}
        layout={{ title: 'Simulation results' ,showlegend: true,margin: {
          l: 40,
          r: 10,
          b: 40,
          t: 80,
          pad: 4
        },legend:{
          "yanchor":"bottom",
          "y":0,
          "xanchor":"right",
          "x":1
        },}}
        config={{ scrollZoom: true }}
        useResizeHandler={true}
        automargin={true}
        style={{ width: `${width-20}px`, height: `${(height / 2<360)?360:height / 2}px` }}
      />
    </div>
  )
}
