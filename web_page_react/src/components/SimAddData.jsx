import React, { useContext, useState } from 'react'
import { DataContext } from '../DataContext'
import uuid from 'uuid/dist/v1'
import result from "../results.json"
import {divideTwoArray as divide,square} from "../lib/MathOperations"
import { useViewport } from '../ViewPortContext'

export const SimAddData = () => {
	const {width} = useViewport()
	const [state, setstate] = useState({
		selectedOption:"",
		selectedPolarization:"",
		selectedRatio:"",
		selectedST:"",
		selectedDataType:""
	})
	const {data,dataSetter} = useContext(DataContext)
	let ratioTypeCount = Object.keys(Object.entries(result)[0][1])
	let spacingTypeCount = Object.keys(Object.entries(Object.entries(result)[0][1])[0][1])
	let text = result.Other_Params.split(",")
	let ttext = text.map(value=>{
		return value+"\n"
	})
	return 890 < width?(
		<div>
					<div className="card text-center">
			
			<div className="card-header rounded text-center" >
			<h2>Other Simulation Parameters</h2>
	  {ttext}
	</div></div>
        <div className="card text-center">
        <div className="card-header rounded">
          Select right to left Simulation Specs to add appropriate data to the chart 
        </div>
        <div className="card-body">
	<div className="container-fluid m-auto p-auto">

	<div className="row align-middle">

		<div className="col my-auto">
			<div className="list-group">
				<button type="button" className="list-group-item list-group-item-action"
				onClick={()=>{setstate({
					...state,
					selectedOption:"PolarizationR"
				})}}
				>Polarization R.</button>
				<button type="button" className="list-group-item list-group-item-action"
							onClick={()=>{setstate({
								...state,
								selectedOption:"Normal"
							})}}>Direct data</button>
			</div>
		</div>
		<div className="my-auto" >
	<img alt="" className="" src="https://image.flaticon.com/icons/svg/109/109617.svg" style={{height:"25px",width:"25px"}}></img></div>
		<div className="col my-auto">
		<div className="list-group">
		<button type="button" className="list-group-item list-group-item-action"				
				onClick={()=>{setstate({
					...state,
					selectedPolarization:"EZ"
				})}}>Ez</button>
		<button type="button" className="list-group-item list-group-item-action"
		onClick={()=>{setstate({
			...state,
			selectedPolarization:"EY"
		})}}>Ey</button>
		</div>
	
    </div><div className="my-auto" >
	<img alt="" className="" src="https://image.flaticon.com/icons/svg/109/109617.svg" style={{height:"25px",width:"25px"}}></img></div>
		<div className="col my-auto">
			<div className="list-group">
				 {ratioTypeCount.map(value => {
					 return <button key={uuid()} type="button" className="list-group-item list-group-item-action"
					 onClick={()=>{
						setstate({
							...state,
							selectedRatio: value
						})
					 }}
					 >{value}</button>
				 })}
			</div>
			
		</div>
		<div className="my-auto" >
	<img alt="" className="" src="https://image.flaticon.com/icons/svg/109/109617.svg" style={{height:"25px",width:"25px"}}></img></div>
	<div className="col my-auto">
			<div className="list-group">
				 {spacingTypeCount.map(value => {
					 return <button key={uuid()} type="button" className="list-group-item list-group-item-action"
					 onClick={()=>{
						setstate({
							...state,
							selectedST: value
						})
					 }}
					 >{value}</button>
				 })}
			</div>
			
		</div>
		<div className="my-auto" >
	<img alt="" className="" src="https://image.flaticon.com/icons/svg/109/109617.svg" style={{height:"25px",width:"25px"}}></img></div>
	<div className="col my-auto"  >
		<div className="list-group">
		<button type="button" className="list-group-item list-group-item-action"
		onClick={
			()=>{
				setstate({
					...state,
					selectedDataType: "Transmission"
				})
			}
		}>Transmission</button>
		<button type="button" className="list-group-item list-group-item-action"
				onClick={
					()=>{
						setstate({
							...state,
							selectedDataType: "Reflected"
						})
					}
				}>Reflected</button>
		</div>
	</div>
  </div>
</div>
            </div>
	<div className="card-header rounded">Selected Simulation Specs: {Object.entries(state).map(iter =>{
		return `/${iter[1]}`
	})}</div>

      </div>
	  <div className="text-center">
	  <button type="button" className=" btn btn-primary mr-3" 
		  onClick={()=>{
			  let check = true;
			  Object.entries(state).map(iter=>{
				  if(iter[1]==="")
					check = false;
					return undefined
			  })
			  if(check){
				let  name = Object.entries(state).map(iter => `/${iter[1]}`)
				name = name.join("")
				  if(state.selectedOption==="Normal"){

				dataSetter([...data,{
					type:"line",
					x:result.Wavelengths,
					y:divide(result[state.selectedPolarization][state.selectedRatio][state.selectedST][state.selectedDataType],result[state.selectedPolarization][state.selectedRatio][state.selectedST]["Incident"])
					,name : name
				}])}else{
					dataSetter([...data,{
						type:"line",
						x:result.Wavelengths,
						y:divide(square(divide(result["EY"][state.selectedRatio][state.selectedST][state.selectedDataType],result["EY"][state.selectedRatio][state.selectedST]["Incident"])),square(divide(result["EZ"][state.selectedRatio][state.selectedST][state.selectedDataType],result["EZ"][state.selectedRatio][state.selectedST]["Incident"])))
						,name:name
					}])					
				}
			  }else{
				  alert("please select from every part!!!")
			  } 
		  }}> Add data to Chart</button>
	  	<button type="button" className=" btn btn-secondary mr-3" 
		  onClick={()=>{setstate({
			  selectedOption:"",
			  selectedPolarization:"",
			  selectedRatio:"",
			  selectedST:"",
			  selectedDataType:""
		  })}}> Clear changes</button>
		  <button type="button" className=" btn btn-secondary " onClick={()=>{
			  dataSetter([])
		  }}>Clear Graph</button>
		  </div>
		  </div>
	):
	
	
	
	
	/**
	 * mobile page
	 */
	
	
	
	
	
	
	(<div className="p-3 mb-2 bg-info text-dark">
		<div className="card text-center text-black">
			
		        <div className="card-header rounded text-center" >
				<h1>Other Simulation Parameters</h1>
          {ttext}
        </div></div>
        <div className="card text-center">
        <div className="card-header rounded text-dark">
          Select Simulation Specs to add appropriate data to the chart 
        </div>
        <div className="card-body">
	<div className="container-fluid m-auto p-auto">

		<div className="container-fluid">
			<div className="button-group">
				<button type="button" className="btn btn-secondary disabled"
				onClick={()=>{setstate({
					...state,
					selectedOption:"PolarizationR"
				})}}
				>Polarization R.</button>
				<button type="button" className="btn btn-secondary "
							onClick={()=>{setstate({
								...state,
								selectedOption:"Normal"
							})}}>Direct data</button>
			</div>
		</div>
		<div className="my-2" >
	<img alt="" className="" src="https://image.flaticon.com/icons/svg/109/109617.svg" style={{height:"25px",width:"25px",transform: "rotate(90deg)"}}></img></div>
		<div className="">
		<div className="row">
		<button type="button" className="col btn btn-secondary m-1 p-auto"				
				onClick={()=>{setstate({
					...state,
					selectedPolarization:"EZ"
				})}}>Ez</button>
		<button type="button" className="col btn btn-secondary m-1 p-auto"
		onClick={()=>{setstate({
			...state,
			selectedPolarization:"EY"
		})}}>Ey</button>
		</div>
	
    </div><div className="my-2" >
	<img alt="" className="" src="https://image.flaticon.com/icons/svg/109/109617.svg" style={{height:"25px",width:"25px",transform: "rotate(90deg)"}}></img></div>
		<div className="">
			<div className=" row">
				 {ratioTypeCount.map(value => {
					 return <button key={uuid()} type="button" className=" col btn btn-secondary m-1 p-auto"
					 onClick={()=>{
						setstate({
							...state,
							selectedRatio: value
						})
					 }}
					 >{value}</button>
				 })}
			</div>
			
		</div>
		<div className="my-2" >
	<img alt="" className="" src="https://image.flaticon.com/icons/svg/109/109617.svg" style={{height:"25px",width:"25px",transform: "rotate(90deg)"}}></img></div>
	<div className="">
			<div className="row">
				 {spacingTypeCount.map(value => {
					 return <button key={uuid()} type="button" className="col btn btn-secondary m-1 p-auto"
					 onClick={()=>{
						setstate({
							...state,
							selectedST: value
						})
					 }}
					 >{value}</button>
				 })}
			</div>
			
		</div>
		<div className="my-2" >
	<img alt="" className="" src="https://image.flaticon.com/icons/svg/109/109617.svg" style={{height:"25px",width:"25px",transform: "rotate(90deg)"}}></img></div>
	<div className=""  >
		<div className="list-group">
		<button type="button" className="col btn btn-secondary m-1 p-auto"
		onClick={
			()=>{
				setstate({
					...state,
					selectedDataType: "Transmission"
				})
			}
		}>Transmission</button>
		<button type="button" className="col btn btn-secondary m-1 p-auto"
				onClick={
					()=>{
						setstate({
							...state,
							selectedDataType: "Reflected"
						})
					}
				}>Reflected</button>
		</div>
	</div>

</div>
            </div>
	<div className="card-header rounded">Selected Simulation Specs: {Object.entries(state).map(iter =>{
		return `/${iter[1]}`
	})}</div>

      </div>
	  <div className="text-center">
	  <button type="button" className=" btn btn-primary mr-1" 
		  onClick={()=>{
			  let check = true;
			  Object.entries(state).map(iter=>{
				  if(iter[1]==="")
					check = false;
					return true
			  })
			  if(check){
				let  name = Object.entries(state).map(iter => `/${iter[1]}`)
				name = name.join("")
				  if(state.selectedOption==="Normal"){
				dataSetter([...data,{
					type:"line",
					x:result.Wavelengths,
					y:divide(result[state.selectedPolarization][state.selectedRatio][state.selectedST][state.selectedDataType],result[state.selectedPolarization][state.selectedRatio][state.selectedST]["Incident"])
					,name
				}])}else{
					dataSetter([...data,{
						type:"line",
						x:result.Wavelengths,
						y:divide(square(result["EY"][state.selectedRatio][state.selectedST][state.selectedDataType]),square(result["EZ"][state.selectedRatio][state.selectedST]["Incident"]))
					,name
					}])					
				}
			  }else{
				  alert("please select from every part!!!")
			  } 
		  }}> Add data to Chart</button>
	  	<button type="button" className=" btn btn-light mr-1" 
		  onClick={()=>{setstate({
			  selectedOption:"",
			  selectedPolarization:"",
			  selectedRatio:"",
			  selectedST:"",
			  selectedDataType:""
		  })}}> Clear changes</button>
		  <button type="button" className=" btn btn-light " onClick={()=>{
			  dataSetter([])
		  }}>Clear Graph</button>
		  </div>
		  </div>
	)
}

