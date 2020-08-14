import React from 'react'
import Plot from 'react-plotly.js';
import { useContext } from 'react';
import uuid from 'uuid/dist/v1'

import { DataContext } from '../DataContext';
import { useViewport } from '../ViewPortContext';

export const SimShow = () => {
  const { width, height } = useViewport()
  const { data ,dataSetter} = useContext(DataContext)
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
        useResizeHandler={true}
        automargin={true}
        style={{ width: `${width-20}px`, height: `${(height / 2<360)?360:height / 2}px` }}
      />{data.length===0?<div></div>:
      <table className="table  table-dark table-responsive-sm table-sm">
        <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">DeleteButton</th>
          <th scope="col">selected Option</th>
          <th scope="col">Polarization</th>
          <th scope="col">Ratio</th>
          <th scope="col">SpacingThickness</th>
          <th scope="col">Reflected/Transmission</th>
        </tr>
        </thead>
        <tbody>
          {data.map((iter,key1) =>{
            return(<tr key={uuid()}>{iter.name.split("/").map((value,key)=>{
              if(key === 0){
                let temp = []
                temp.push(<th key = {uuid()} scope="col">{key1+1}</th>)
                temp.push(<td key={uuid()}><button className="btn btn-dark btn-sm" onClick={()=>{
                let tempp = [];
                data.map((val,key0)=>{
                  if(key0===key1){

                  }
                  else{
                    tempp.push(val)
                  }
                  return undefined
                })
                dataSetter(tempp)
                }}>Delete this item</button></td>)
                return(temp)
              }else{
                return(<th key={uuid()}>{value}</th>)
              }
            })}</tr>)
          })}
        </tbody>
      </table>}
    </div>
  )
}
