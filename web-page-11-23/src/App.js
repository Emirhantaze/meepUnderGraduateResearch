import DropdownUs from "./Dropdown";
import { DataContext } from "./Datacontext";
import { Selectioncontext, typenames, selectSpacing } from "./Selectionconcext";
import d from "./sample.json"
import { useContext } from "react";
import { SimShow } from './SimShow';
import { abso, addition, divide, reduceDimention } from "./MathOperations";
import { minussign } from "./MathOperations";

Number.prototype.toFloatString = function () {
  return this.toLocaleString("en-US", {
    minimumFractionDigits: 1,
    maximumFractionDigits: 20 // the default is 3 if min < 3
  });
};


export default function App() {
  window.data = d
  const { data, dataSetter } = useContext(DataContext)
  const { selection, selectionSetter } = useContext(Selectioncontext)
  const spaces = selectSpacing(d)
  return (

    < div className="App" >
      <div> Simulation Results</div>

      {/* this part is for showing the selected parameters */}
      <div className="container row">
        <div className="col">ratio(g,s,pdms) :[{selection["GoldRatio"]},{selection["SilverRatio"]},{selection["PDMSRatio"]}]</div>
        <div className="col">Polarization :{selection["Polarization"]}</div>
        <div className="col">Spacing :{selection["Spacing"]}</div>
        <div className="col">Type of the result: {selection["type"]}</div>
      </div>


      <div className="container"><div className="row ">
        <DropdownUs title={"Ratio of PDMS"} names={selection["PDMSRatios"]} selection_id="pdms" />
        <DropdownUs title={"Ratio of Silver"} names={selection["SilverRatios"]} selection_id="silver" />
        <DropdownUs title={"Ratio of Gold"} names={selection["GoldRatios"]} selection_id="gold" />
        <DropdownUs title={"Polarization"} names={["Ey", "Ez"]} selection_id="polarization" />
        <DropdownUs title={"Spacing"} names={spaces} selection_id="spacing" />
        <DropdownUs title={"Type of the Result"} names={typenames} selection_id="type" />
      </div>

      </div>


      <button onClick={() => {
        let name = `{"Ratio": [${(selection['GoldRatio']).toFloatString()}, ${(selection['SilverRatio']).toFloatString()}, ${(selection['PDMSRatio']).toFloatString()}], "X_span": 2e-08, "Y_span": 5e-07, "Spacing": 7.5e-07}`
        let result = d[name]
        let y = null;
        
        // this part is for selecting the correct data to plot
        if (selection.type === typenames[0]) {//Transmission
          if (selection.Polarization === "Ey") {
            y = result["EY polarization"]
          } else if (selection.Polarization === "Ez") {
            y = result["Ez polarization"]
          }
        }
        else if(selection.type === typenames[1]){ // reflection
          if (selection.Polarization === "Ey") {
            y = minussign(result["EY polarization (back)"])
          } else if (selection.Polarization === "Ez") {
            y = minussign(result["Ez polarization (back)"])
          }
        }
        else if (selection.type === typenames[2]){ // polarizaton ratio transmisson
          y = divide(abso(addition(result["EY polarization"],minussign(result["Ez polarization"]))),addition(result["EY polarization"],result["Ez polarization"]));
        }
        else if (selection.type === typenames[3]){ // polarizaton ratio transmisson
          y = divide(abso(addition(result["EY polarization (back)"],minussign(result["Ez polarization (back)"]))),addition(result["EY polarization (back)"],result["Ez polarization (back)"]));
        }


        ////////////////////////////////////////////////////////
        if (y === null) {
          alert("Select all required simulation parameters")
        }
        dataSetter([...data, {
          type: "line",
          x: reduceDimention(result["Lambda"]),
          y: y,
          keygen: `/${result["Ratio"]}/${selection.type}/${selection["Spacing"]}`
        }].map((val,key) => { val.name=key+1;return val}))



      }}>Draw Selected Result</button>

      <SimShow />
    </div >
  );
}
